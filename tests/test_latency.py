from speechloop.metrics.latency import latency_percentiles


def test_latency_percentiles_basic():
    vals = list(range(100))
    p = latency_percentiles(vals)
    assert p["p50"] >= 49
    assert p["p95"] >= 94
    assert p["max"] == 99


def test_latency_percentiles_empty():
    p = latency_percentiles([])
    assert p["p50"] == 0.0
