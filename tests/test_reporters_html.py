from speechloop.reporters import render
from speechloop.result import SuiteResult, CaseResult


def test_html_contains_each_case():
    sr = SuiteResult(suite_name="s",
                     cases=[CaseResult(name=f"c{i}", tags=[]) for i in range(5)],
                     summary={"total": 5, "passed": 5, "failed": 0,
                              "latency_p95_ms": 0, "wer_mean": None, "cer_mean": None})
    out = render("html", sr)
    for i in range(5):
        assert f"c{i}" in out
    assert "<table" in out


def test_html_escapes_transcript():
    sr = SuiteResult(
        suite_name="s",
        cases=[CaseResult(name="evil", tags=[], transcript="<script>x</script>")],
        summary={"total": 1, "passed": 1, "failed": 0, "latency_p95_ms": 0,
                 "wer_mean": None, "cer_mean": None},
    )
    out = render("html", sr)
    assert "<script>x</script>" not in out
    assert "&lt;script&gt;" in out
