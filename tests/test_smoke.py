from speechloop import __version__


def test_version_is_str():
    assert isinstance(__version__, str)
    assert __version__
