"""适配器接口、注册表与内置实现入口。"""
from __future__ import annotations

# HTTP 适配器（独立模块，避免循环导入）
from . import (
    http_asr,  # noqa: F401
    http_llm,  # noqa: F401
    http_tts,  # noqa: F401
)
from .base import (
    ASRAdapter,
    LLMAdapter,
    TTSAdapter,
    discover_entry_points,
    get_adapter,
    register,
    registered_names,
)

__all__ = [
    "ASRAdapter", "LLMAdapter", "TTSAdapter",
    "register", "get_adapter", "registered_names", "discover_entry_points",
]
