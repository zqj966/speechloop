"""YAML 套件加载与展开。"""
from __future__ import annotations
import glob
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .case import Case
from .errors import SuiteLoadError
from .perturb import Perturbation, expand_matrix


@dataclass
class Suite:
    name: str
    cases: list[Case]
    defaults: dict = field(default_factory=dict)
    perturbations: list[Perturbation] = field(default_factory=list)
    thresholds: dict = field(default_factory=dict)
    base_dir: Path = field(default_factory=Path)
    include_tags: list[str] = field(default_factory=list)
    exclude_tags: list[str] = field(default_factory=list)

    def filter_cases(self) -> list[Case]:
        if not self.include_tags and not self.exclude_tags:
            return list(self.cases)
        inc = set(self.include_tags)
        exc = set(self.exclude_tags)
        out = []
        for c in self.cases:
            tags = set(c.tags)
            if inc and not (tags & inc):
                continue
            if exc and (tags & exc):
                continue
            out.append(c)
        return out


def load_suite(path: str | Path) -> Suite:
    p = Path(path)
    if not p.exists():
        raise SuiteLoadError(f"suite file not found: {p}")
    try:
        data: dict[str, Any] = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise SuiteLoadError(f"invalid yaml in {p}: {exc}") from exc

    base = p.parent
    # $ref 简易展开 —— 一层
    for ref in data.pop("imports", []) or []:
        ref_path = (base / ref).resolve()
        ref_data = yaml.safe_load(Path(ref_path).read_text(encoding="utf-8")) or {}
        for k, v in ref_data.items():
            data.setdefault(k, v)

    cases_raw = data.get("cases") or []
    cases: list[Case] = []
    for c in cases_raw:
        audio_field = c.get("audio", "")
        # glob 展开
        if any(ch in str(audio_field) for ch in "*?["):
            matches = sorted(glob.glob(str(base / audio_field)))
            if not matches:
                raise SuiteLoadError(f"glob matched nothing: {audio_field}")
            for m in matches:
                cases.append(_make_case(c, m).resolve(base))
        else:
            cases.append(_make_case(c, audio_field).resolve(base))

    return Suite(
        name=str(data.get("suite", p.stem)),
        cases=cases,
        defaults=dict(data.get("defaults", {})),
        perturbations=expand_matrix(data.get("perturbations", [])),
        thresholds=dict(data.get("thresholds", {})),
        base_dir=base,
        include_tags=list(data.get("include_tags", [])),
        exclude_tags=list(data.get("exclude_tags", [])),
    )


def _make_case(c: dict, audio_path: str) -> Case:
    return Case(
        name=str(c.get("name", Path(audio_path).stem)),
        audio=Path(audio_path),
        expected_transcript=c.get("expected_transcript"),
        expected_response_contains=list(c.get("expected_response_contains", [])),
        tags=list(c.get("tags", [])),
        timeout_s=c.get("timeout_s"),
    )

# Path.expanduser() inside Case.resolve() handles ~
