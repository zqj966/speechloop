"""Character Error Rate —— 中文场景常用。"""
from __future__ import annotations

from ..text import tokenize_zh
from .wer import _edit_distance


def cer(reference: str, hypothesis: str) -> float:
    ref = tokenize_zh(reference)
    hyp = tokenize_zh(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    return _edit_distance(ref, hyp) / len(ref)
