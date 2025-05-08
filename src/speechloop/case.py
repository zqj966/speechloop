"""测试用例数据类。"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Case:
    name: str
    audio: Path
    expected_transcript: str | None = None
    expected_response_contains: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    timeout_s: float | None = None
    perturbation_id: str | None = None

    def resolve(self, base: Path) -> "Case":
        """把 audio 解析为相对 ``base`` 的绝对路径。"""
        p = Path(str(self.audio)).expanduser()
        if not p.is_absolute():
            p = (base / p).resolve()
        return Case(
            name=self.name,
            audio=p,
            expected_transcript=self.expected_transcript,
            expected_response_contains=list(self.expected_response_contains),
            tags=list(self.tags),
            timeout_s=self.timeout_s,
            perturbation_id=self.perturbation_id,
        )
