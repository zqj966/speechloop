"""高精度计时器。"""
from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class TimingRecord:
    wall_ms: float
    monotonic_ms: float


@contextmanager
def stopwatch():
    """``with stopwatch() as t: ...`` —— 退出后 ``t.value`` 是 ``TimingRecord``。"""
    holder: dict[str, TimingRecord] = {}
    w0 = time.time()
    m0 = time.monotonic()
    try:
        yield holder
    finally:
        holder["value"] = TimingRecord(
            wall_ms=(time.time() - w0) * 1000.0,
            monotonic_ms=(time.monotonic() - m0) * 1000.0,
        )


def now_ms() -> float:
    return time.monotonic() * 1000.0
