"""Shared pytest fixtures."""
from __future__ import annotations

import pytest

from speechloop.audio import silence, sine, write_wav


@pytest.fixture
def tone_wav(tmp_path):
    p = tmp_path / "tone.wav"
    write_wav(p, sine(0.4, 440.0))
    return p


@pytest.fixture
def silent_wav(tmp_path):
    p = tmp_path / "silent.wav"
    write_wav(p, silence(0.4))
    return p


@pytest.fixture
def make_suite(tmp_path):
    def _make(yaml_text: str, name: str = "suite.yaml"):
        p = tmp_path / name
        p.write_text(yaml_text, encoding="utf-8")
        return p
    return _make
