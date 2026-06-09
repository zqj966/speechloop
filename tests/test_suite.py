from speechloop.suite import load_suite


def test_load_minimal(make_suite, tone_wav):
    yaml_text = f"""\
suite: t
defaults: {{asr: dummy, llm: echo, tts: quiet}}
cases:
  - name: hi
    audio: {tone_wav}
"""
    p = make_suite(yaml_text)
    s = load_suite(p)
    assert s.name == "t"
    assert len(s.cases) == 1
    assert s.cases[0].name == "hi"
