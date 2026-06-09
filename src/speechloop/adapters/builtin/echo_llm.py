"""把输入原样返回 —— 用于打通整条链路。"""
from __future__ import annotations
from ..base import register


@register("LLM", "echo")
class EchoLLM:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def respond(self, prompt: str) -> str:
        return f"{self.prefix}{prompt}" if self.prefix else prompt
