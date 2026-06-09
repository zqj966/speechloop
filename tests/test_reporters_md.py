from speechloop.reporters import render
from speechloop.result import SuiteResult, CaseResult


def test_md_table_columns():
    sr = SuiteResult(
        suite_name="s",
        cases=[CaseResult(name="c1", tags=["a"], passed=True)],
        summary={"total": 1, "passed": 1, "failed": 0, "latency_p95_ms": 0,
                 "wer_mean": None, "cer_mean": None},
    )
    out = render("md", sr)
    assert "| case | tags |" in out
    assert "c1" in out
