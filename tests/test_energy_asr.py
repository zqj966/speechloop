from speechloop.adapters import get_adapter
from speechloop.audio import silence, sine, write_wav


def test_energy_detects_tone(tmp_path):
    wav = tmp_path / "t.wav"
    write_wav(wav, sine(0.3, 440.0))
    asr = get_adapter("ASR", "energy")
    assert asr.transcribe(str(wav)) == "speech"


def test_energy_detects_silence(tmp_path):
    wav = tmp_path / "s.wav"
    write_wav(wav, silence(0.3))
    asr = get_adapter("ASR", "energy")
    assert asr.transcribe(str(wav)) == "silence"
