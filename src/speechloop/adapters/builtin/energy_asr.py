"""基于能量阈值的"是否有声音" ASR —— 用于离线 sanity-check。"""
from __future__ import annotations

from ...audio import read_wav
from ..base import register


@register("ASR", "energy")
class EnergyASR:
    def __init__(self, threshold: int = 100):
        self.threshold = threshold

    def transcribe(self, audio_path: str) -> str:
        audio = read_wav(audio_path)
        if not audio.samples:
            return ""
        peak = max(abs(s) for s in audio.samples)
        return "speech" if peak >= self.threshold else "silence"
