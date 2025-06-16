from speechloop.pipeline import Pipeline
from speechloop.suite import Suite


def test_from_suite_default_steps():
    s = Suite(name="t", cases=[], defaults={"asr": "x-asr", "llm": "x-llm", "tts": "x-tts"})
    p = Pipeline.from_suite(s)
    assert [s.adapter for s in p.steps] == ["x-asr", "x-llm", "x-tts"]
