"""适配器接口、注册表与内置实现入口。"""
from __future__ import annotations

from .base import (
    ASRAdapter, LLMAdapter, TTSAdapter,
    register, get_adapter, registered_names, discover_entry_points,
)

# HTTP 适配器（独立模块，避免循环导入）
from . import http_asr  # noqa: F401
from . import http_llm  # noqa: F401
from . import http_tts  # noqa: F401

__all__ = [
    "ASRAdapter", "LLMAdapter", "TTSAdapter",
    "register", "get_adapter", "registered_names", "discover_entry_points",
]
