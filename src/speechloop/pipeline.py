"""把 Suite 转换成一个声明式 Pipeline 描述（便于 dry-run / 可视化）。"""
from __future__ import annotations

from dataclasses import dataclass

from .suite import Suite


@dataclass
class PipelineStep:
    name: str
    adapter: str


@dataclass
class Pipeline:
    suite: str
    steps: list[PipelineStep]

    @classmethod
    def from_suite(cls, suite: Suite) -> Pipeline:
        defaults = suite.defaults
        return cls(
            suite=suite.name,
            steps=[
                PipelineStep("asr", defaults.get("asr", "dummy")),
                PipelineStep("llm", defaults.get("llm", "echo")),
                PipelineStep("tts", defaults.get("tts", "quiet")),
            ],
        )
