"""Result dataclasses — stub."""
from dataclasses import dataclass, field

@dataclass
class CaseResult:
    name: str
    tags: list = field(default_factory=list)
    passed: bool = True

@dataclass
class SuiteResult:
    suite_name: str
    cases: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)
