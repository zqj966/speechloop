"""speechloop —— 语音大模型全链路测试框架。

公共 API:

    from speechloop import Suite, run_suite, register, get_adapter
"""
from __future__ import annotations

__version__ = "0.3.0"

from .suite import Suite, load_suite
from .runner import run_suite, CaseResult, SuiteResult
from .adapters import register, get_adapter, ASRAdapter, LLMAdapter, TTSAdapter

# 触发内置适配器注册
from .adapters import builtin as _builtin  # noqa: F401

__all__ = [
    "__version__",
    "Suite", "load_suite",
    "run_suite", "CaseResult", "SuiteResult",
    "register", "get_adapter",
    "ASRAdapter", "LLMAdapter", "TTSAdapter",
]
