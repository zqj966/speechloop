"""WAV I/O — stub."""
from dataclasses import dataclass

@dataclass
class Audio:
    samples: list
    sample_rate: int = 16000
