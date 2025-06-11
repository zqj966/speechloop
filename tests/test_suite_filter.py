from speechloop.suite import Suite
from speechloop.case import Case
from pathlib import Path


def test_include_exclude():
    cases = [
        Case(name="a", audio=Path("/tmp/a.wav"), tags=["zh"]),
        Case(name="b", audio=Path("/tmp/b.wav"), tags=["en"]),
        Case(name="c", audio=Path("/tmp/c.wav"), tags=["zh", "slow"]),
    ]
    s = Suite(name="t", cases=cases, include_tags=["zh"], exclude_tags=["slow"])
    names = [c.name for c in s.filter_cases()]
    assert names == ["a"]
