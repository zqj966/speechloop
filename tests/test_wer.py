from speechloop.metrics.wer import wer


def test_wer_perfect():
    assert wer("hello world", "hello world") == 0.0


def test_wer_single_substitution():
    assert wer("hello world", "hello there") == 0.5


def test_wer_empty_reference():
    assert wer("", "") == 0.0
    assert wer("", "hi") == 1.0
