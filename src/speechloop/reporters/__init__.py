"""报告渲染器分发表。"""
from __future__ import annotations

from collections.abc import Callable

from ..result import SuiteResult
from .html_reporter import HTMLReporter
from .json_reporter import JSONReporter
from .md_reporter import MarkdownReporter
from .text_reporter import TextReporter

_REGISTRY: dict[str, Callable[[SuiteResult], str]] = {
    "text": lambda sr: TextReporter().render(sr),
    "json": lambda sr: JSONReporter().render(sr),
    "html": lambda sr: HTMLReporter().render(sr),
    "md": lambda sr: MarkdownReporter().render(sr),
}


def render(fmt: str, sr: SuiteResult) -> str:
    fmt = fmt.lower()
    if fmt not in _REGISTRY:
        raise KeyError(f"unknown reporter format: {fmt}")
    return _REGISTRY[fmt](sr)


def manifest(sr: SuiteResult) -> dict:
    return {
        "suite": sr.suite_name,
        "total": len(sr.cases),
        "passed": sum(1 for c in sr.cases if c.passed),
        "artifacts": [c.synthesized_path for c in sr.cases if c.synthesized_path],
    }
