"""Case dataclass — stub."""
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Case:
    name: str
    audio: Path
    tags: list = field(default_factory=list)
