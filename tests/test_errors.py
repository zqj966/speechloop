from speechloop.errors import (
    AdapterError,
    CaseTimeoutError,
    SpeechloopError,
    SuiteLoadError,
    ThresholdNotMet,
    TransientError,
)


def test_hierarchy():
    for cls in [SuiteLoadError, AdapterError, CaseTimeoutError, ThresholdNotMet]:
        assert issubclass(cls, SpeechloopError)
    assert issubclass(TransientError, AdapterError)
