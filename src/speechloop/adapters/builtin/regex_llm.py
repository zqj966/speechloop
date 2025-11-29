"""正则规则驱动的离线 LLM，用于回归测试链路。"""
from __future__ import annotations

import re
from collections.abc import Iterable

from ..base import register


@register("LLM", "regex")
class RegexLLM:
    def __init__(self, rules: Iterable[tuple[str, str]] | None = None,
                 default: str = "(no match)"):
        rules = list(rules or [])
        self.rules = [(re.compile(p), r) for p, r in rules]
        self.default = default

    def respond(self, prompt: str) -> str:
        for pat, reply in self.rules:
            if pat.search(prompt):
                return reply
        return self.default
