"""speechloop 命令行入口。"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .errors import SpeechloopError, SuiteLoadError
from .pipeline import Pipeline
from .reporters import render
from .runner import run_suite
from .suite import load_suite


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="speechloop", description="语音大模型全链路测试框架")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="运行套件")
    run_p.add_argument("suite", help="suite.yaml 路径")
    run_p.add_argument("--format", default="text", choices=["text", "json", "html", "md"])
    run_p.add_argument("-o", "--output", help="输出文件路径（默认 stdout）")
    run_p.add_argument("--filter", action="append", default=[], help="只跑带某 tag 的用例")
    run_p.add_argument("--exclude", action="append", default=[], help="排除某 tag")
    run_p.add_argument("--workers", type=int, default=1)
    run_p.add_argument("--timeout", type=float, default=30.0)
    run_p.add_argument("--artifacts-dir", default=None)
    run_p.add_argument("--dry-run", action="store_true", help="只打印计划")
    run_p.add_argument("--stream", action="store_true", help="逐条 JSON line 输出")

    init_p = sub.add_parser("init", help="生成最小套件骨架")
    init_p.add_argument("path", help="目标目录")

    rep_p = sub.add_parser("report", help="把 JSON 结果重新渲染为别的格式")
    rep_p.add_argument("input", help="先前 --format json 的输出")
    rep_p.add_argument("--format", default="text", choices=["text", "html", "md"])
    rep_p.add_argument("-o", "--output", default=None)

    return p


def _emit(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def _cmd_run(args) -> int:
    try:
        suite = load_suite(args.suite)
    except SuiteLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.filter:
        suite.include_tags = list(set(suite.include_tags) | set(args.filter))
    if args.exclude:
        suite.exclude_tags = list(set(suite.exclude_tags) | set(args.exclude))

    if args.dry_run:
        plan = Pipeline.from_suite(suite)
        cases = suite.filter_cases()
        print(f"suite: {plan.suite}")
        for s in plan.steps:
            print(f"  step {s.name}: {s.adapter}")
        print(f"  cases: {len(cases)} × perturbations: {len(suite.perturbations) or 1}")
        return 0

    progress = None
    if args.stream:
        def _p(cr):
            sys.stdout.write(json.dumps(
                {"event": "case", "name": cr.name, "passed": cr.passed,
                 "metrics": cr.metrics}, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        progress = _p

    # workers=0 → 串行
    workers = max(1, args.workers) if args.workers and args.workers > 0 else 1

    sr = run_suite(
        suite,
        workers=workers,
        timeout_s=args.timeout,
        artifacts_dir=args.artifacts_dir,
        progress=progress,
    )
    text = render(args.format, sr)
    _emit(text, args.output)
    return 0 if not sr.summary.get("threshold_failures") and sr.summary["failed"] == 0 else 1


def _cmd_init(args) -> int:
    target = Path(args.path)
    target.mkdir(parents=True, exist_ok=True)
    (target / "suite.yaml").write_text(MINIMAL_SUITE, encoding="utf-8")
    # 生成一个最小 WAV
    from .audio import sine, write_wav
    write_wav(target / "hello.wav", sine(0.5, 440.0))
    print(f"initialized minimal suite at {target}")
    return 0


def _cmd_report(args) -> int:
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    from .result import SuiteResult, CaseResult, StepRecord
    sr = SuiteResult(
        suite_name=data.get("suite", ""),
        cases=[
            CaseResult(
                name=c["name"], tags=c.get("tags", []),
                transcript=c.get("transcript", ""), response=c.get("response", ""),
                metrics=c.get("metrics", {}), passed=c.get("passed", True),
                steps=[StepRecord(**s) for s in c.get("steps", [])],
            )
            for c in data.get("cases", [])
        ],
        summary=data.get("summary", {}),
    )
    _emit(render(args.format, sr), args.output)
    return 0


MINIMAL_SUITE = """\
suite: demo
defaults:
  asr: dummy
  llm: echo
  tts: tone
cases:
  - name: hello
    audio: ./hello.wav
    expected_transcript: hello
    expected_response_contains: ["hello"]
    tags: [smoke]
thresholds:
  wer_max: 0.5
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == "run":
            return _cmd_run(args)
        if args.cmd == "init":
            return _cmd_init(args)
        if args.cmd == "report":
            return _cmd_report(args)
    except SpeechloopError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
