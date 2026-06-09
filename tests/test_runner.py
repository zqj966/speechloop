from speechloop.suite import Suite
from speechloop.case import Case
from speechloop.runner import run_suite


def test_runner_single_case(tone_wav):
    case = Case(name="c1", audio=tone_wav, expected_transcript="tone",
                expected_response_contains=["tone"])
    suite = Suite(name="s", cases=[case], defaults={"asr": "dummy", "llm": "echo", "tts": "quiet"})
    sr = run_suite(suite, workers=1)
    assert sr.summary["total"] == 1
    assert sr.cases[0].transcript == "tone"
