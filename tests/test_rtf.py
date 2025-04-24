from speechloop.metrics.rtf import rtf


def test_rtf_basic():
    assert rtf(1000.0, 2.0) == 0.5


def test_rtf_zero_duration():
    assert rtf(1000.0, 0.0) == 0.0
