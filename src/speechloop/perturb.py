"""音频扰动矩阵 + 可复现 RNG。"""
from __future__ import annotations

import itertools
import random
from collections.abc import Iterable
from dataclasses import dataclass, field

from .audio import Audio, add_noise, gain, resample_linear


@dataclass
class Perturbation:
    """单一扰动配置。"""
    kind: str                  # "noise" | "gain" | "tempo"
    params: dict = field(default_factory=dict)
    id: str = ""

    def apply(self, audio: Audio, *, seed: int | None = None) -> Audio:
        if self.kind == "noise":
            return add_noise(audio, float(self.params["snr_db"]), seed=seed)
        if self.kind == "gain":
            return gain(audio, float(self.params["db"]))
        if self.kind == "tempo":
            factor = float(self.params["factor"])
            new_sr = max(1, int(audio.sample_rate * factor))
            tmp = Audio(audio.samples, new_sr, audio.sample_width, audio.channels)
            return resample_linear(tmp, audio.sample_rate)
        raise ValueError(f"unknown perturbation kind: {self.kind}")


def expand_matrix(specs: Iterable[dict]) -> list[Perturbation]:
    """把套件 YAML 的扰动矩阵展开成一个个 ``Perturbation``。

    ``{"kind": "noise", "snr_db": [20, 10]}`` → 两个 ``Perturbation``。
    """
    out: list[Perturbation] = []
    out.append(Perturbation(kind="none", params={}, id="none"))  # 永远包含一个基线
    for spec in specs or []:
        kind = spec.get("kind")
        if not kind:
            continue
        lists: list[tuple[str, list]] = []
        for k, v in spec.items():
            if k == "kind":
                continue
            lists.append((k, v if isinstance(v, list) else [v]))
        if not lists:
            out.append(Perturbation(kind=kind, params={}, id=kind))
            continue
        keys = [k for k, _ in lists]
        for values in itertools.product(*(vs for _, vs in lists)):
            params = dict(zip(keys, values, strict=False))
            ident = f"{kind}[{','.join(f'{k}={v}' for k, v in params.items())}]"
            out.append(Perturbation(kind=kind, params=params, id=ident))
    return out


def deterministic_rng(seed: int) -> random.Random:
    return random.Random(seed)

# Perturbation IDs land in CaseResult.tags so reports can filter on them.
