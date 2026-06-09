"""按文件名 → 转写的查表式 ASR，便于在 CI 中跑通整条链路。"""
from __future__ import annotations

from pathlib import Path

from ..base import register


@register("ASR", "dummy")
class DummyASR:
    """简单查表：若 ``audio_path`` 同目录有 ``<stem>.txt``，读它；否则用 stem。"""

    def __init__(self, table: dict[str, str] | None = None):
        self.table = table or {}

    def transcribe(self, audio_path: str) -> str:
        p = Path(audio_path)
        if p.name in self.table:
            return self.table[p.name]
        if p.stem in self.table:
            return self.table[p.stem]
        sidecar = p.with_suffix(".txt")
        if sidecar.exists():
            return sidecar.read_text(encoding="utf-8").strip()
        return p.stem
