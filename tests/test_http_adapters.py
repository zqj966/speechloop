from speechloop.adapters.http_asr import HTTPASR
from speechloop.adapters.http_llm import HTTPLLM
from speechloop.adapters.http_tts import HTTPTTS


def test_http_asr_with_injected_client(tmp_path):
    wav = tmp_path / "x.wav"
    wav.write_bytes(b"\x00\x01")
    asr = HTTPASR("http://example", client=lambda url, **kw: {"text": "ok"})
    assert asr.transcribe(str(wav)) == "ok"


def test_http_llm_with_injected_client():
    llm = HTTPLLM("http://example", client=lambda url, **kw: {"text": "hi"})
    assert llm.respond("?") == "hi"


def test_http_tts_with_injected_client(tmp_path):
    out = tmp_path / "o.bin"
    tts = HTTPTTS("http://example", client=lambda url, **kw: b"PAYLOAD")
    tts.synthesize("x", str(out))
    assert out.read_bytes() == b"PAYLOAD"
