"""Reporter 基类。"""
from __future__ import annotations

from ..result import SuiteResult


class Reporter:
    name = "abstract"

    def render(self, sr: SuiteResult) -> str:  # pragma: no cover - abstract
        raise NotImplementedError
