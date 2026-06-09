import subprocess
import sys
import textwrap


def test_threshold_failure_exits_nonzero(tmp_path):
    suite = tmp_path / "s.yaml"
    suite.write_text(textwrap.dedent("""\
    suite: t
    defaults: {asr: dummy, llm: echo, tts: quiet}
    cases:
      - name: c1
        audio: x.wav
        expected_transcript: bonjour
    thresholds:
      wer_max: 0.0
    """), encoding="utf-8")
    # 需要一个真实 wav
    from speechloop.audio import sine, write_wav
    write_wav(tmp_path / "x.wav", sine(0.2, 440.0))
    r = subprocess.run([sys.executable, "-m", "speechloop.cli", "run", str(suite),
                        "--format", "text"], capture_output=True, text=True)
    assert r.returncode != 0
