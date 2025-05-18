"""SilentTTS — emit a same-length silence WAV (will rename to QuietTTS)."""
from __future__ import annotations

from ...audio import silence, write_wav
from ..base import register


@register("TTS", "quiet")
class SilentTTS:
    def __init__(self, sample_rate: int = 16000, chars_per_sec: float = 5.0):
        self.sample_rate = sample_rate
        self.chars_per_sec = chars_per_sec

    def synthesize(self, text: str, out_path: str) -> None:
        dur = max(0.2, len(text) / max(0.1, self.chars_per_sec))
        write_wav(out_path, silence(dur, self.sample_rate))
