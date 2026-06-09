"""suite loader — stub."""
from dataclasses import dataclass, field

@dataclass
class Suite:
    name: str = ""
    cases: list = field(default_factory=list)
