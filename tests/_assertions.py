"""Shared assertion helpers."""
from __future__ import annotations


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def in_range(x: float, lo: float, hi: float) -> bool:
    return lo <= x <= hi
