"""JSON reporter —— 同时是 ``speechloop report`` 的输入格式。"""
from __future__ import annotations

import json
from dataclasses import asdict

from ..result import SuiteResult
from .base import Reporter


class JSONReporter(Reporter):
    name = "json"
    SCHEMA_VERSION = 1

    def render(self, sr: SuiteResult) -> str:
        data = {
            "schema": self.SCHEMA_VERSION,
            "suite": sr.suite_name,
            "summary": sr.summary,
            "cases": [asdict(c) for c in sr.cases],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
