from speechloop.case import Case
from speechloop.perturb import Perturbation
from speechloop.runner import run_suite
from speechloop.suite import Suite


def test_perturb_matrix(tone_wav):
    perts = [
        Perturbation(kind="none", id="none"),
        Perturbation(kind="noise", params={"snr_db": 10}, id="n10"),
        Perturbation(kind="gain", params={"db": -6}, id="g-6"),
    ]
    case = Case(name="c", audio=tone_wav)
    suite = Suite(name="s", cases=[case], perturbations=perts,
                  defaults={"asr": "dummy", "llm": "echo", "tts": "quiet"})
    sr = run_suite(suite, workers=1)
    assert sr.summary["total"] == 3
