"""pipeline DSL — stub."""
from dataclasses import dataclass

@dataclass
class Pipeline:
    suite: str = ""
    steps: list = None
