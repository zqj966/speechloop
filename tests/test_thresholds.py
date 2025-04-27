from speechloop.metrics.thresholds import evaluate_thresholds


class _SR:
    summary = {"wer_mean": 0.4, "cer_mean": 0.3, "latency_p95_ms": 2000.0}


def test_threshold_fails_on_wer():
    f = evaluate_thresholds(_SR(), {"wer_max": 0.1})
    assert f and "wer_mean" in f[0]


def test_threshold_ok():
    assert evaluate_thresholds(_SR(), {"wer_max": 0.9, "cer_max": 0.9}) == []
