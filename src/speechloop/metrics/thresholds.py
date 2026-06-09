"""阈值评估 —— 把 summary 与配置对比，给出失败原因列表。"""
from __future__ import annotations


def evaluate_thresholds(suite_result, thresholds: dict) -> list[str]:
    failures: list[str] = []
    s = suite_result.summary
    if "wer_max" in thresholds and s.get("wer_mean") is not None:
        if s["wer_mean"] > float(thresholds["wer_max"]):
            failures.append(f"wer_mean {s['wer_mean']:.3f} > {thresholds['wer_max']}")
    if "cer_max" in thresholds and s.get("cer_mean") is not None:
        if s["cer_mean"] > float(thresholds["cer_max"]):
            failures.append(f"cer_mean {s['cer_mean']:.3f} > {thresholds['cer_max']}")
    if "latency_p95_ms" in thresholds:
        if s.get("latency_p95_ms", 0) > float(thresholds["latency_p95_ms"]):
            failures.append(
                f"latency_p95 {s['latency_p95_ms']:.1f} > {thresholds['latency_p95_ms']}"
            )
    return failures
