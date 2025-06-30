"""通用 HTTP ASR 适配器。

为了让核心包零外部依赖（除 PyYAML），HTTP 客户端是注入式的。
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Callable

from .base import register


@register("ASR", "http")
class HTTPASR:
    def __init__(self, url: str, *, client: Callable[..., Any] | None = None,
                 field: str = "audio", text_key: str = "text", timeout: float = 30.0):
        self.url = url
        self.client = client
        self.field = field
        self.text_key = text_key
        self.timeout = timeout

    def _get_client(self):
        if self.client is not None:
            return self.client
        try:
            import httpx  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("install speechloop[http] to use HTTPASR") from exc
        return lambda url, **kw: httpx.post(url, timeout=self.timeout, **kw).json()

    def transcribe(self, audio_path: str) -> str:
        data = Path(audio_path).read_bytes()
        client = self._get_client()
        resp = client(self.url, files={self.field: data})
        if isinstance(resp, dict):
            return str(resp.get(self.text_key, ""))
        return str(resp)
