"""HTML reporter —— 自包含的单文件输出。"""
from __future__ import annotations
import html

from ..result import SuiteResult
from .base import Reporter


_CSS = """
/* HTML output goes through html.escape; CSS stays minimal */
body{font-family:-apple-system,Helvetica,Arial,sans-serif;margin:24px;color:#222}
h1{margin-top:0}
.sum{padding:12px;background:#f5f5f7;border-radius:6px;margin:12px 0}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #eee;padding:6px 8px;text-align:left}
tr.fail td{background:#fff3f3}
tr.pass td{background:#f3fff5}
.diff-ref{color:#888}
.diff-hyp{color:#333}
"""


class HTMLReporter(Reporter):
    name = "html"

    def render(self, sr: SuiteResult) -> str:
        s = sr.summary
        rows = []
        for c in sr.cases:
            cls = "pass" if c.passed else "fail"
            wer = c.metrics.get("wer")
            cer_v = c.metrics.get("cer")
            wer_s = f"{wer:.3f}" if wer is not None else "—"
            cer_s = f"{cer_v:.3f}" if cer_v is not None else "—"
            rows.append(
                f"<tr class='{cls}'>"
                f"<td>{html.escape(c.name)}</td>"
                f"<td>{html.escape(','.join(c.tags))}</td>"
                f"<td>{c.total_latency_ms:.0f}</td>"
                f"<td>{wer_s}</td>"
                f"<td>{cer_s}</td>"
                f"<td><span class='diff-ref'>ref: </span>{html.escape(c.transcript)}</td>"
                f"<td>{html.escape(c.response)}</td>"
                f"</tr>"
            )
        body = "\n".join(rows)
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{html.escape(sr.suite_name)}</title>
<style>{_CSS}</style></head>
<body>
<h1>speechloop · {html.escape(sr.suite_name)}</h1>
<div class="sum">
  <strong>{s.get('passed', 0)}/{s.get('total', 0)} passed</strong>
  · latency p95: {s.get('latency_p95_ms', 0):.0f} ms
  · WER {s.get('wer_mean') and f"{s['wer_mean']:.3f}" or '—'}
  · CER {s.get('cer_mean') and f"{s['cer_mean']:.3f}" or '—'}
</div>
<table>
<thead><tr><th>case</th><th>tags</th><th>latency</th><th>WER</th><th>CER</th><th>transcript</th><th>response</th></tr></thead>
<tbody>
{body}
</tbody></table>
</body></html>
"""
