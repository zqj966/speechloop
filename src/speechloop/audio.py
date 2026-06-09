"""极简 WAV I/O 与扰动原语 —— 只依赖标准库 ``wave``。"""
from __future__ import annotations
import array
import math
import random
import wave
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Audio:
    samples: list[int]
    sample_rate: int
    sample_width: int = 2  # bytes per sample
    channels: int = 1

    @property
    def duration_s(self) -> float:
        if self.sample_rate <= 0:
            return 0.0
        return len(self.samples) / (self.sample_rate * self.channels)


def read_wav(path: str | Path) -> Audio:
    with wave.open(str(path), "rb") as w:
        sw = w.getsampwidth()
        sr = w.getframerate()
        ch = w.getnchannels()
        n = w.getnframes()
        raw = w.readframes(n)
    if sw not in (1, 2, 4):
        raise ValueError(f"unsupported sample width: {sw}")
    typecode = {1: "b", 2: "h", 4: "i"}[sw]
    a = array.array(typecode)
    a.frombytes(raw)
    return Audio(samples=list(a), sample_rate=sr, sample_width=sw, channels=ch)


def write_wav(path: str | Path, audio: Audio) -> None:
    typecode = {1: "b", 2: "h", 4: "i"}[audio.sample_width]
    a = array.array(typecode, audio.samples)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(audio.channels)
        w.setsampwidth(audio.sample_width)
        w.setframerate(audio.sample_rate)
        w.writeframes(a.tobytes())


def _max_amp(width: int) -> int:
    return (1 << (8 * width - 1)) - 1


def gain(audio: Audio, db: float) -> Audio:
    """按 dB 调整音量，并做硬截幅。"""
    factor = 10 ** (db / 20.0)
    cap = _max_amp(audio.sample_width)
    out = [max(-cap - 1, min(cap, int(s * factor))) for s in audio.samples]
    return Audio(out, audio.sample_rate, audio.sample_width, audio.channels)


def add_noise(audio: Audio, snr_db: float, *, seed: int | None = None) -> Audio:
    """高斯白噪 + 目标 SNR。"""
    if not audio.samples:
        return audio
    rng = random.Random(seed)
    # signal RMS
    s2 = sum(s * s for s in audio.samples) / len(audio.samples)
    if s2 <= 0:
        return audio
    snr_lin = 10 ** (snr_db / 10.0)
    n2 = s2 / snr_lin
    sigma = math.sqrt(n2)
    cap = _max_amp(audio.sample_width)
    out = [
        max(-cap - 1, min(cap, int(s + rng.gauss(0, sigma))))
        for s in audio.samples
    ]
    return Audio(out, audio.sample_rate, audio.sample_width, audio.channels)


def resample_linear(audio: Audio, target_sr: int) -> Audio:
    if audio.sample_rate == target_sr or not audio.samples:
        return audio
    ratio = target_sr / audio.sample_rate
    n_out = int(len(audio.samples) * ratio)
    out: list[int] = []
    for i in range(n_out):
        src = i / ratio
        lo = int(src)
        hi = min(lo + 1, len(audio.samples) - 1)
        frac = src - lo
        out.append(int(audio.samples[lo] * (1 - frac) + audio.samples[hi] * frac))
    return Audio(out, target_sr, audio.sample_width, audio.channels)


def trim_silence(audio: Audio, threshold: int = 50) -> Audio:
    if not audio.samples:
        return audio
    start = 0
    end = len(audio.samples)
    while start < end and abs(audio.samples[start]) < threshold:
        start += 1
    while end > start and abs(audio.samples[end - 1]) < threshold:
        end -= 1
    return Audio(
        audio.samples[start:end], audio.sample_rate, audio.sample_width, audio.channels
    )


def to_mono(audio: Audio) -> Audio:
    if audio.channels == 1:
        return audio
    ch = audio.channels
    out: list[int] = []
    for i in range(0, len(audio.samples), ch):
        chunk = audio.samples[i : i + ch]
        out.append(sum(chunk) // ch)
    return Audio(out, audio.sample_rate, audio.sample_width, channels=1)


def silence(duration_s: float, sample_rate: int = 16000) -> Audio:
    n = int(duration_s * sample_rate)
    return Audio([0] * n, sample_rate)


def sine(duration_s: float, freq_hz: float = 440.0, sample_rate: int = 16000,
         amplitude: float = 0.3) -> Audio:
    n = int(duration_s * sample_rate)
    cap = _max_amp(2)
    amp = int(cap * amplitude)
    samples = [int(amp * math.sin(2 * math.pi * freq_hz * i / sample_rate)) for i in range(n)]
    return Audio(samples, sample_rate)

# eof
