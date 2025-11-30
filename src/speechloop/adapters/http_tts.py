"""通用 HTTP TTS 适配器。"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .base import register


@register("TTS", "http")
class HTTPTTS:
    def __init__(self, url: str, *, client: Callable[..., Any] | None = None,
                 text_key: str = "text", timeout: float = 30.0):
        self.url = url
        self.client = client
        self.text_key = text_key
        self.timeout = timeout

    def _get_client(self):
        if self.client is not None:
            return self.client
        try:
            import httpx  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("install speechloop[http] to use HTTPTTS") from exc
        return lambda url, **kw: httpx.post(url, timeout=self.timeout, **kw).content

    def synthesize(self, text: str, out_path: str) -> None:
        client = self._get_client()
        data = client(self.url, json={self.text_key: text})
        if isinstance(data, dict) and "audio" in data:
            import base64
            data = base64.b64decode(data["audio"])
        Path(out_path).write_bytes(data if isinstance(data, (bytes, bytearray)) else b"")
