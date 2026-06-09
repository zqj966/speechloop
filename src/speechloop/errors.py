"""speechloop 错误类型层次。"""
from __future__ import annotations


class SpeechloopError(Exception):
    """所有 speechloop 异常的基类。"""


class SuiteLoadError(SpeechloopError):
    """读取 / 解析套件 YAML 失败。"""


class AdapterError(SpeechloopError):
    """适配器调用失败。"""


class TransientError(AdapterError):
    """可重试的瞬时错误（网络抖动等）。"""


class CaseTimeoutError(SpeechloopError):
    """单个用例超时。"""


class ThresholdNotMet(SpeechloopError):
    """聚合指标未达阈值。"""
