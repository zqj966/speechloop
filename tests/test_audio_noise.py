from speechloop.audio import add_noise, sine


def test_noise_changes_samples_but_keeps_length():
    a = sine(0.2, 440.0)
    b = add_noise(a, snr_db=10.0, seed=42)
    assert len(a.samples) == len(b.samples)
    diffs = sum(1 for x, y in zip(a.samples, b.samples) if x != y)
    assert diffs > len(a.samples) // 2


def test_noise_empty_safe():
    from speechloop.audio import Audio
    a = Audio([], 16000)
    b = add_noise(a, 10.0)
    assert b.samples == []
