from speechloop.metrics.wer import wer


def test_wer_deletion():
    assert wer("a b c d", "a c d") == 0.25


def test_wer_insertion():
    assert wer("a b", "a x b") == 0.5


def test_wer_punctuation_normalized():
    assert wer("hello, world!", "hello world") == 0.0
