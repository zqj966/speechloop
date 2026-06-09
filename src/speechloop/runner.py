"""执行引擎：把一个 ``Suite`` 跑成 ``SuiteResult``。"""
from __future__ import annotations

import concurrent.futures
import os
import tempfile
import time
from collections.abc import Iterable
from pathlib import Path

from .adapters import get_adapter
from .audio import read_wav, write_wav
from .case import Case
from .errors import CaseTimeoutError, TransientError
from .metrics.aggregate import aggregate_metrics
from .metrics.thresholds import evaluate_thresholds
from .perturb import Perturbation
from .result import CaseResult, StepRecord, SuiteResult
from .suite import Suite


def _step(name: str, fn):
    t0 = time.monotonic()
    try:
        result = fn()
        return StepRecord(name=name, latency_ms=(time.monotonic() - t0) * 1000.0, ok=True), result
    except Exception as exc:  # noqa: BLE001
        return StepRecord(
            name=name, latency_ms=(time.monotonic() - t0) * 1000.0,
            ok=False, error=f"{type(exc).__name__}: {exc}",
        ), None


def _run_one(case: Case, defaults: dict, perturb: Perturbation,
             artifacts_dir: Path | None, seed: int) -> CaseResult:
    name = f"{case.name}[{perturb.id}]" if perturb.id != "none" else case.name
    cr = CaseResult(name=name, tags=list(case.tags) + ([perturb.id] if perturb.id != "none" else []))

    # 应用扰动
    audio = read_wav(case.audio)
    if perturb.id != "none":
        audio = perturb.apply(audio, seed=seed)
        if artifacts_dir is not None:
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            perturbed_path = artifacts_dir / f"{name}.input.wav"
            write_wav(perturbed_path, audio)
        else:
            fd, name = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            perturbed_path = Path(name)
            write_wav(perturbed_path, audio)
    else:
        perturbed_path = Path(case.audio)

    asr = get_adapter("ASR", defaults.get("asr", "dummy"))
    llm = get_adapter("LLM", defaults.get("llm", "echo"))
    tts = get_adapter("TTS", defaults.get("tts", "quiet"))

    s1, transcript = _step("asr", lambda: asr.transcribe(str(perturbed_path)))
    cr.steps.append(s1)
    cr.transcript = transcript or ""

    s2, response = _step("llm", lambda: llm.respond(cr.transcript))
    cr.steps.append(s2)
    cr.response = response or ""

    out_wav = (artifacts_dir or Path(tempfile.gettempdir())) / f"{name}.out.wav"
    s3, _ = _step("tts", lambda: tts.synthesize(cr.response, str(out_wav)))
    cr.steps.append(s3)
    cr.synthesized_path = str(out_wav)

    cr.metrics = aggregate_metrics(case, cr)
    cr.passed = all(s.ok for s in cr.steps)
    if case.expected_response_contains:
        for needle in case.expected_response_contains:
            if needle not in cr.response:
                cr.passed = False
                cr.failures.append(f"response missing '{needle}'")
    return cr


def _run_with_timeout(case: Case, defaults, perturb, artifacts, seed, timeout_s):
    if timeout_s is None or timeout_s <= 0:
        return _run_one(case, defaults, perturb, artifacts, seed)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(_run_one, case, defaults, perturb, artifacts, seed)
        try:
            return fut.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError as exc:
            raise CaseTimeoutError(f"case '{case.name}' timed out") from exc


def run_suite(
    suite: Suite,
    *,
    workers: int = 1,
    timeout_s: float | None = None,
    artifacts_dir: str | Path | None = None,
    retries: int = 1,
    seed: int = 0,
    progress=None,
) -> SuiteResult:
    artifacts = Path(artifacts_dir) if artifacts_dir else None
    cases = suite.filter_cases()
    perturbations = suite.perturbations or [Perturbation(kind="none", params={}, id="none")]

    tasks: list[tuple[Case, Perturbation]] = [(c, p) for c in cases for p in perturbations]
    results: list[CaseResult] = []

    def _do(task):
        case, perturb = task
        last_exc = None
        for attempt in range(max(1, retries)):
            try:
                return _run_with_timeout(case, suite.defaults, perturb, artifacts,
                                         seed + attempt, case.timeout_s or timeout_s)
            except TransientError as exc:
                last_exc = exc
                continue
            except CaseTimeoutError as exc:
                last_exc = exc
                break
        cr = CaseResult(name=case.name, tags=list(case.tags))
        cr.passed = False
        cr.failures.append(str(last_exc))
        return cr

    if workers and workers > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            for r in ex.map(_do, tasks):
                results.append(r)
                if progress:
                    progress(r)
    else:
        for t in tasks:
            r = _do(t)
            results.append(r)
            if progress:
                progress(r)

    sr = SuiteResult(suite_name=suite.name, cases=results)
    sr.summary = _summarize(sr)
    threshold_failures = evaluate_thresholds(sr, suite.thresholds)
    sr.summary["threshold_failures"] = threshold_failures
    return sr


def _summarize(sr: SuiteResult) -> dict:
    total = len(sr.cases)
    passed = sum(1 for c in sr.cases if c.passed)
    wer_vals = [c.metrics.get("wer") for c in sr.cases if "wer" in c.metrics]
    cer_vals = [c.metrics.get("cer") for c in sr.cases if "cer" in c.metrics]
    lat = sorted(c.total_latency_ms for c in sr.cases)
    p95 = lat[int(0.95 * (len(lat) - 1))] if lat else 0.0
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "wer_mean": sum(wer_vals) / len(wer_vals) if wer_vals else None,
        "cer_mean": sum(cer_vals) / len(cer_vals) if cer_vals else None,
        "latency_p95_ms": p95,
    }


def by_tag(sr: SuiteResult) -> dict[str, dict]:
    out: dict[str, list[CaseResult]] = {}
    for c in sr.cases:
        for t in c.tags:
            out.setdefault(t, []).append(c)
    return {
        tag: {"total": len(cs), "passed": sum(1 for c in cs if c.passed)}
        for tag, cs in out.items()
    }


def iter_artifacts(sr: SuiteResult) -> Iterable[str]:
    for c in sr.cases:
        if c.synthesized_path and os.path.exists(c.synthesized_path):
            yield c.synthesized_path

# end of runner module
