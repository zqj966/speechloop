"""runner — single-case happy path."""
from __future__ import annotations
import time
from pathlib import Path

from .adapters import get_adapter
from .case import Case
from .result import CaseResult, StepRecord, SuiteResult
from .suite import Suite


def _step(name, fn):
    t0 = time.monotonic()
    try:
        r = fn()
        return StepRecord(name, (time.monotonic() - t0) * 1000.0, True), r
    except Exception as exc:
        return StepRecord(name, (time.monotonic() - t0) * 1000.0, False,
                          f"{type(exc).__name__}: {exc}"), None


def run_suite(suite: Suite, *, workers=1, timeout_s=None, artifacts_dir=None,
              retries=1, seed=0, progress=None) -> SuiteResult:
    cases = list(suite.cases)
    results = []
    asr = get_adapter("ASR", suite.defaults.get("asr", "dummy"))
    llm = get_adapter("LLM", suite.defaults.get("llm", "echo"))
    tts = get_adapter("TTS", suite.defaults.get("tts", "quiet"))
    for case in cases:
        cr = CaseResult(name=case.name, tags=list(case.tags))
        s1, transcript = _step("asr", lambda: asr.transcribe(str(case.audio)))
        cr.steps.append(s1); cr.transcript = transcript or ""
        s2, resp = _step("llm", lambda: llm.respond(cr.transcript))
        cr.steps.append(s2); cr.response = resp or ""
        s3, _ = _step("tts", lambda t=cr.response: tts.synthesize(t, "/tmp/o.wav"))
        cr.steps.append(s3)
        cr.passed = all(s.ok for s in cr.steps)
        results.append(cr)
    sr = SuiteResult(suite_name=suite.name, cases=results,
                     summary={"total": len(results),
                              "passed": sum(1 for c in results if c.passed),
                              "failed": sum(1 for c in results if not c.passed),
                              "wer_mean": None, "cer_mean": None,
                              "latency_p95_ms": 0.0})
    return sr
