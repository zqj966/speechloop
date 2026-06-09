from speechloop.adapters import get_adapter
from speechloop.audio import read_wav


def test_tone_tts_writes_wav(tmp_path):
    tts = get_adapter("TTS", "tone")
    out = tmp_path / "o.wav"
    tts.synthesize("你好世界", str(out))
    a = read_wav(out)
    assert a.sample_rate == 16000
    assert a.duration_s > 0
