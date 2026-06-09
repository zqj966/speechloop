"""轻量语义相似度 —— 基于 token 集合的 Jaccard 指数。

不引入大模型嵌入，避免给核心包加重依赖；够用于回归断言。
"""
from __future__ import annotations

from ..text import tokenize_zh


def similarity(a: str, b: str) -> float:
    sa = set(tokenize_zh(a))
    sb = set(tokenize_zh(b))
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)
