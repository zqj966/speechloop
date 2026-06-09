from speechloop.adapters import get_adapter


def test_dummy_asr_uses_sidecar(tmp_path):
    wav = tmp_path / "x.wav"
    wav.write_bytes(b"RIFF")  # path-only access, dummy doesn't read content
    (tmp_path / "x.txt").write_text("你好", encoding="utf-8")
    asr = get_adapter("ASR", "dummy")
    assert asr.transcribe(str(wav)) == "你好"


def test_echo_llm_roundtrips():
    llm = get_adapter("LLM", "echo")
    assert llm.respond("ping") == "ping"
