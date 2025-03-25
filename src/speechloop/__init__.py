"""speechloop —— 语音大模型全链路测试框架。"""
__version__ = "0.0.2"

from .suite import Suite
from .case import Case

__all__ = ["__version__", "Suite", "Case"]
