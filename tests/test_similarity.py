from speechloop.metrics.similarity import similarity


def test_similarity_identical():
    assert similarity("你好", "你好") == 1.0


def test_similarity_disjoint():
    assert similarity("你好", "天空") == 0.0


def test_similarity_partial():
    assert 0 < similarity("你好世界", "你好") < 1
