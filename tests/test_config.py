import os

from speechloop.config import Config


def test_config_defaults():
    cfg = Config.load()
    assert cfg.workers >= 1


def test_config_env_overrides(monkeypatch):
    monkeypatch.setenv("SPEECHLOOP_WORKERS", "7")
    cfg = Config.load()
    assert cfg.workers == 7


def test_config_from_toml(tmp_path):
    p = tmp_path / "c.toml"
    p.write_text("[speechloop]\nworkers = 3\ntimeout_s = 1.5\n", encoding="utf-8")
    cfg = Config.load(p)
    assert cfg.workers == 3
    assert cfg.timeout_s == 1.5
