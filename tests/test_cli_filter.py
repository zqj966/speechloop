import subprocess
import sys
import textwrap

from speechloop.audio import sine, write_wav


def test_cli_filter_tag(tmp_path):
    write_wav(tmp_path / "a.wav", sine(0.2, 440.0))
    write_wav(tmp_path / "b.wav", sine(0.2, 440.0))
    suite = tmp_path / "s.yaml"
    suite.write_text(textwrap.dedent("""\
    suite: t
    defaults: {asr: dummy, llm: echo, tts: quiet}
    cases:
      - name: a
        audio: a.wav
        tags: [keep]
      - name: b
        audio: b.wav
        tags: [skip]
    """), encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "speechloop.cli", "run", str(suite),
                        "--filter", "keep", "--format", "json"], capture_output=True, text=True)
    import json
    data = json.loads(r.stdout)
    assert data["summary"]["total"] == 1
