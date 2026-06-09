"""可选的 TOML 配置加载 + 环境变量覆盖。"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib  # type: ignore[attr-defined]
except ImportError:  # py<3.11
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass
class Config:
    workers: int = 1
    timeout_s: float = 30.0
    artifacts_dir: str = "artifacts"
    extras: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Config":
        data: dict = {}
        if path is not None and Path(path).exists():
            with open(path, "rb") as f:
                data = tomllib.load(f)
            data = data.get("speechloop", data)
        cfg = cls(
            workers=int(data.get("workers", 1)),
            timeout_s=float(data.get("timeout_s", 30.0)),
            artifacts_dir=str(data.get("artifacts_dir", "artifacts")),
            extras={k: v for k, v in data.items()
                    if k not in {"workers", "timeout_s", "artifacts_dir"}},
        )
        return cfg.apply_env()

    def apply_env(self) -> "Config":
        if "SPEECHLOOP_WORKERS" in os.environ:
            self.workers = int(os.environ["SPEECHLOOP_WORKERS"])
        if "SPEECHLOOP_TIMEOUT" in os.environ:
            self.timeout_s = float(os.environ["SPEECHLOOP_TIMEOUT"])
        if "SPEECHLOOP_ARTIFACTS" in os.environ:
            self.artifacts_dir = os.environ["SPEECHLOOP_ARTIFACTS"]
        return self
