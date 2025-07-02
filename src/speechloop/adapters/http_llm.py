"""通用 HTTP LLM 适配器。"""
from __future__ import annotations
from typing import Any, Callable

from .base import register


@register("LLM", "http")
class HTTPLLM:
    def __init__(self, url: str, *, client: Callable[..., Any] | None = None,
                 prompt_key: str = "prompt", text_key: str = "text", timeout: float = 30.0):
        self.url = url
        self.client = client
        self.prompt_key = prompt_key
        self.text_key = text_key
        self.timeout = timeout

    def _get_client(self):
        if self.client is not None:
            return self.client
        try:
            import httpx  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("install speechloop[http] to use HTTPLLM") from exc
        return lambda url, **kw: httpx.post(url, timeout=self.timeout, **kw).json()

    def respond(self, prompt: str) -> str:
        client = self._get_client()
        resp = client(self.url, json={self.prompt_key: prompt})
        if isinstance(resp, dict):
            return str(resp.get(self.text_key, ""))
        return str(resp)
