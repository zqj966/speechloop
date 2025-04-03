from speechloop.audio import gain, sine


def test_gain_clipping():
    a = sine(0.2, 440.0, amplitude=0.9)
    b = gain(a, 24.0)  # +24dB → 强烈截幅
    assert max(b.samples) <= 32767
    assert min(b.samples) >= -32768
