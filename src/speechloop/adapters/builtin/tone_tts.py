"""文本 → 单频正弦 WAV，频率由字符长度决定。"""
from __future__ import annotations

from ...audio import sine, write_wav
from ..base import register


@register("TTS", "tone")
class ToneTTS:
    def __init__(self, sample_rate: int = 16000, base_hz: float = 220.0):
        self.sample_rate = sample_rate
        self.base_hz = base_hz

    def synthesize(self, text: str, out_path: str) -> None:
        if not text:
            text = " "
        dur = max(0.2, len(text) * 0.15)
        # 让不同长度的输入产生不同频率，便于测试时区分
        freq = self.base_hz * (1 + (len(text) % 7) * 0.1)
        write_wav(out_path, sine(dur, freq, self.sample_rate))
