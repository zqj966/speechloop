from speechloop.case import Case
from speechloop.runner import run_suite
from speechloop.suite import Suite


def test_runner_parallel(tone_wav):
    cases = [Case(name=f"c{i}", audio=tone_wav) for i in range(6)]
    suite = Suite(name="s", cases=cases, defaults={"asr": "dummy", "llm": "echo", "tts": "quiet"})
    sr = run_suite(suite, workers=4)
    assert sr.summary["total"] == 6
    assert sr.summary["passed"] == 6
