"""结构化日志辅助。

speechloop 不强制接管 ``logging``，只提供一个轻量 JSON line 输出函数，
用于 CI 环境下把每一条事件写到 stdout 方便机读。
"""
from __future__ import annotations
import json
import sys
from typing import Any


def log_event(stream, event: str, **fields: Any) -> None:
    """写一条 JSON line 事件到给定 stream。"""
    record = {"event": event, **fields}
    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    stream.flush()


def info(event: str, **fields: Any) -> None:
    log_event(sys.stderr, event, level="info", **fields)


def warn(event: str, **fields: Any) -> None:
    log_event(sys.stderr, event, level="warn", **fields)
