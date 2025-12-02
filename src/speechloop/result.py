"""单用例 / 套件级结果数据类。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StepRecord:
    name: str          # "asr" | "llm" | "tts"
    latency_ms: float
    ok: bool
    error: str | None = None
    payload_summary: str = ""


@dataclass
class CaseResult:
    name: str
    tags: list[str]
    transcript: str = ""
    response: str = ""
    synthesized_path: str | None = None
    steps: list[StepRecord] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    passed: bool = True
    failures: list[str] = field(default_factory=list)

    @property
    def total_latency_ms(self) -> float:
        return sum(s.latency_ms for s in self.steps)


@dataclass
class SuiteResult:
    suite_name: str
    cases: list[CaseResult] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
