from speechloop.text import tokenize_zh


def test_zh_per_character():
    assert tokenize_zh("中文测试") == ["中", "文", "测", "试"]


def test_zh_with_punct():
    assert tokenize_zh("你好，世界！") == ["你", "好", "世", "界"]
