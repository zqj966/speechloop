from speechloop.text import normalize, tokenize_en, tokenize_zh


def test_normalize_lower_strip_punct():
    assert normalize("  Hello, World!  ") == "hello world"


def test_tokenize_en():
    assert tokenize_en("Hello, world!") == ["hello", "world"]


def test_tokenize_zh_mixes():
    toks = tokenize_zh("你好 world 你好")
    assert "你" in toks and "好" in toks and "world" in toks
