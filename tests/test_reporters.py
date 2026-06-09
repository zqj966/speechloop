import json

from speechloop.reporters import render
from speechloop.result import CaseResult, StepRecord, SuiteResult


def _sample():
    return SuiteResult(
        suite_name="s",
        cases=[CaseResult(name="c1", tags=["smoke"], transcript="hi", response="hi",
                          metrics={"wer": 0.0, "latency_ms": 50}, passed=True,
                          steps=[StepRecord("asr", 10.0, True),
                                 StepRecord("llm", 20.0, True),
                                 StepRecord("tts", 20.0, True)])],
        summary={"total": 1, "passed": 1, "failed": 0, "wer_mean": 0.0,
                 "cer_mean": None, "latency_p95_ms": 50},
    )


def test_json_reporter_shape():
    sr = _sample()
    data = json.loads(render("json", sr))
    assert data["schema"] == 1
    assert data["suite"] == "s"
    assert data["cases"][0]["name"] == "c1"


def test_text_reporter_has_summary():
    out = render("text", _sample())
    assert "passed: 1" in out
