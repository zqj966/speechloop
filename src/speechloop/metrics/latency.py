"""延迟分位数。"""
from __future__ import annotations

from collections.abc import Iterable


def latency_percentiles(values: Iterable[float], ps=(0.5, 0.95, 0.99)) -> dict[str, float]:
    arr = sorted(float(v) for v in values)
    if not arr:
        return {f"p{int(p*100)}": 0.0 for p in ps}
    out: dict[str, float] = {}
    for p in ps:
        idx = max(0, min(len(arr) - 1, int(round(p * (len(arr) - 1)))))
        out[f"p{int(p*100)}"] = arr[idx]
    out["mean"] = sum(arr) / len(arr)
    out["max"] = arr[-1]
    return out
