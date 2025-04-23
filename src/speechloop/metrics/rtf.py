"""Real-Time Factor —— 处理时长 / 音频时长。"""
from __future__ import annotations


def rtf(process_ms: float, audio_duration_s: float) -> float:
    if audio_duration_s <= 0:
        return 0.0
    return (process_ms / 1000.0) / audio_duration_s
