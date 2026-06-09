import time
import pytest

from speechloop.adapters import register
from speechloop.suite import Suite
from speechloop.case import Case
from speechloop.runner import run_suite


@register("LLM", "slow-test")
class _SlowLLM:
    def respond(self, prompt: str) -> str:
        time.sleep(0.3)
        return prompt


def test_runner_timeout_fails(tone_wav):
    case = Case(name="c", audio=tone_wav, timeout_s=0.1)
    suite = Suite(name="s", cases=[case],
                  defaults={"asr": "dummy", "llm": "slow-test", "tts": "quiet"})
    sr = run_suite(suite, workers=1)
    # 用例应失败，但 suite 还是结束
    assert sr.cases[0].passed is False
