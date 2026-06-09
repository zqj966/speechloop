from speechloop.metrics.cer import cer


def test_cer_perfect_zh():
    assert cer("你好世界", "你好世界") == 0.0


def test_cer_substitution_zh():
    assert cer("你好世界", "你好天空") == 0.5


def test_cer_empty():
    assert cer("", "你") == 1.0
