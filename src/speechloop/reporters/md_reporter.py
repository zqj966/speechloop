"""Markdown reporter —— 用于 PR 评论。"""
from __future__ import annotations

from ..result import SuiteResult
from .base import Reporter


class MarkdownReporter(Reporter):
    name = "md"

    def render(self, sr: SuiteResult) -> str:
        s = sr.summary
        out = [f"# speechloop · {sr.suite_name}", ""]
        out.append(f"**{s.get('passed', 0)}/{s.get('total', 0)} passed** "
                   f"— latency p95 {s.get('latency_p95_ms', 0):.0f} ms")
        out += ["", "| case | tags | latency (ms) | WER | CER | passed |",
                "|---|---|---:|---:|---:|:---:|"]
        for c in sr.cases:
            wer = c.metrics.get("wer")
            cer_v = c.metrics.get("cer")
            out.append(
                f"| {c.name} | {','.join(c.tags)} | {c.total_latency_ms:.0f} | "
                f"{wer if wer is not None else '—'} | {cer_v if cer_v is not None else '—'} | "
                f"{'✅' if c.passed else '❌'} |"
            )
        if s.get("threshold_failures"):
            out += ["", "### Threshold failures", ""]
            out += [f"- {f}" for f in s["threshold_failures"]]
        return "\n".join(out) + "\n"
