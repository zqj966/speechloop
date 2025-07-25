import subprocess, sys, textwrap

from speechloop.audio import sine, write_wav


def test_dry_run_does_not_execute(tmp_path):
    write_wav(tmp_path / "a.wav", sine(0.2, 440.0))
    suite = tmp_path / "s.yaml"
    suite.write_text(textwrap.dedent("""\
    suite: t
    defaults: {asr: dummy, llm: echo, tts: quiet}
    cases:
      - {name: a, audio: a.wav}
    """), encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "speechloop.cli", "run", str(suite),
                        "--dry-run"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "step asr: dummy" in r.stdout
