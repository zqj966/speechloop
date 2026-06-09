from speechloop.audio import resample_linear, sine


def test_resample_preserves_duration():
    a = sine(0.5, 440.0, sample_rate=16000)
    b = resample_linear(a, 8000)
    assert b.sample_rate == 8000
    assert abs(b.duration_s - a.duration_s) < 0.01
