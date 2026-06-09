"""适配器协议 + 全局注册表 + entry-point 发现。"""
from __future__ import annotations
from typing import Any, Callable, Protocol, runtime_checkable

# (kind, name) -> factory
_REGISTRY: dict[tuple[str, str], Callable[..., Any]] = {}


@runtime_checkable
class ASRAdapter(Protocol):
    def transcribe(self, audio_path: str) -> str: ...


@runtime_checkable
class LLMAdapter(Protocol):
    def respond(self, prompt: str) -> str: ...


@runtime_checkable
class TTSAdapter(Protocol):
    def synthesize(self, text: str, out_path: str) -> None: ...


def register(kind: str, name: str):
    """装饰器：``@register("ASR", "my-asr")``。"""
    kind = kind.upper()

    def deco(cls_or_factory):
        _REGISTRY[(kind, name)] = cls_or_factory
        return cls_or_factory

    return deco


def get_adapter(kind: str, name: str, **kwargs):
    key = (kind.upper(), name)
    if key not in _REGISTRY:
        raise KeyError(f"adapter {kind}:{name} not registered. "
                       f"known: {registered_names()}")
    return _REGISTRY[key](**kwargs)


def registered_names() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for kind, name in _REGISTRY:
        out.setdefault(kind, []).append(name)
    return out


def discover_entry_points(group: str = "speechloop.adapters") -> int:
    """通过 importlib.metadata.entry_points 发现外部包注册的适配器。

    返回新注册的适配器数量。失败静默忽略，避免 import 副作用。
    """
    try:
        from importlib.metadata import entry_points
    except ImportError:  # pragma: no cover
        return 0
    eps = entry_points()
    selected = eps.select(group=group) if hasattr(eps, "select") else eps.get(group, [])
    count = 0
    for ep in selected:
        try:
            ep.load()
            count += 1
        except Exception:  # noqa: BLE001
            continue
    return count
