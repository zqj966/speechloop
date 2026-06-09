"""纯文本控制台 reporter。"""
from __future__ import annotations

from ..result import SuiteResult
from .base import Reporter


class TextReporter(Reporter):
    name = "text"

    def render(self, sr: SuiteResult) -> str:
        s = sr.summary
        lines = [f"suite: {sr.suite_name}",
                 f"total: {s.get('total', 0)}  passed: {s.get('passed', 0)}  failed: {s.get('failed', 0)}"]
        if s.get("wer_mean") is not None:
            lines.append(f"WER (mean): {s['wer_mean']:.3f}")
        if s.get("cer_mean") is not None:
            lines.append(f"CER (mean): {s['cer_mean']:.3f}")
        lines.append(f"latency p95: {s.get('latency_p95_ms', 0):.1f} ms")
        if s.get("threshold_failures"):
            lines.append("threshold failures:")
            for f in s["threshold_failures"]:
                lines.append(f"  - {f}")
        lines.append("")
        for c in sr.cases:
            mark = "✓" if c.passed else "✗"
            lines.append(f"  {mark} {c.name}  ({c.total_latency_ms:.0f} ms)")
            if not c.passed:
                for f in c.failures:
                    lines.append(f"      ! {f}")
        return "\n".join(lines) + "\n"
