from speechloop.audio import read_wav, sine, write_wav


def test_wav_round_trip(tmp_path):
    p = tmp_path / "a.wav"
    a = sine(0.2, 880.0)
    write_wav(p, a)
    b = read_wav(p)
    assert b.sample_rate == a.sample_rate
    assert b.channels == 1
    assert len(b.samples) == len(a.samples)
