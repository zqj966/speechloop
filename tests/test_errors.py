from speechloop.errors import (
    SpeechloopError, SuiteLoadError, AdapterError, TransientError,
    CaseTimeoutError, ThresholdNotMet,
)


def test_hierarchy():
    for cls in [SuiteLoadError, AdapterError, CaseTimeoutError, ThresholdNotMet]:
        assert issubclass(cls, SpeechloopError)
    assert issubclass(TransientError, AdapterError)
