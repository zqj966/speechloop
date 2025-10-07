"""把指标计算从 runner 里拆出来 —— 输入 (case, case_result) → metrics dict。"""
from __future__ import annotations

from ..case import Case
from ..result import CaseResult
from .cer import cer
from .similarity import similarity
from .wer import wer


def aggregate_metrics(case: Case, cr: CaseResult) -> dict[str, float]:
    metrics: dict[str, float] = {"latency_ms": cr.total_latency_ms}
    if case.expected_transcript is not None:
        metrics["wer"] = wer(case.expected_transcript, cr.transcript)
        metrics["cer"] = cer(case.expected_transcript, cr.transcript)
    if case.expected_response_contains:
        ref = " ".join(case.expected_response_contains)
        metrics["similarity"] = similarity(ref, cr.response)
    return metrics

# pure-function aggregator; easy to unit-test
