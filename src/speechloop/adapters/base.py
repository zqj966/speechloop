"""adapter protocols — stub."""
from typing import Protocol

class ASRAdapter(Protocol):
    def transcribe(self, p): ...

class LLMAdapter(Protocol):
    def respond(self, p): ...

class TTSAdapter(Protocol):
    def synthesize(self, t, p): ...

_REG = {}

def register(kind, name):
    def deco(c):
        _REG[(kind.upper(), name)] = c
        return c
    return deco

def get_adapter(kind, name, **kw):
    return _REG[(kind.upper(), name)](**kw)
