# API Reference

## 顶层

- `speechloop.__version__: str`
- `speechloop.load_suite(path) -> Suite`
- `speechloop.run_suite(suite, *, workers=1, timeout_s=None, ...) -> SuiteResult`
- `speechloop.register(kind, name)` —— 适配器注册装饰器
- `speechloop.get_adapter(kind, name, **kwargs)`

## 协议

```python
class ASRAdapter(Protocol):
    def transcribe(self, audio_path: str) -> str: ...

class LLMAdapter(Protocol):
    def respond(self, prompt: str) -> str: ...

class TTSAdapter(Protocol):
    def synthesize(self, text: str, out_path: str) -> None: ...
```

## 指标

- `speechloop.metrics.wer(ref, hyp) -> float`
- `speechloop.metrics.cer(ref, hyp) -> float`
- `speechloop.metrics.similarity(a, b) -> float`
- `speechloop.metrics.latency_percentiles(values) -> dict`
- `speechloop.metrics.rtf(process_ms, audio_duration_s) -> float`
- `speechloop.metrics.evaluate_thresholds(suite_result, thresholds) -> list[str]`

## 报告

- `speechloop.reporters.render(fmt, suite_result) -> str`
- `fmt` ∈ `{"text", "json", "html", "md"}`

## 错误

- `SpeechloopError` (基类)
- `SuiteLoadError`, `AdapterError`, `TransientError`,
  `CaseTimeoutError`, `ThresholdNotMet`

<!-- polish 7 -->

<!-- polish 8 -->
