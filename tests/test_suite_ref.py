import textwrap


def test_imports_merge(tmp_path):
    base = tmp_path / "base.yaml"
    base.write_text("defaults:\n  asr: dummy\n  llm: echo\n  tts: quiet\n", encoding="utf-8")
    main = tmp_path / "main.yaml"
    main.write_text(textwrap.dedent(f"""\
    suite: m
    imports:
      - {base.name}
    cases:
      - name: x
        audio: x.wav
    """), encoding="utf-8")
    from speechloop.audio import sine, write_wav
    write_wav(tmp_path / "x.wav", sine(0.2, 440.0))
    from speechloop.suite import load_suite
    s = load_suite(main)
    assert s.defaults["asr"] == "dummy"
