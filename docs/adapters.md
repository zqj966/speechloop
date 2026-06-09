# 编写适配器

## 最小例子

```python
from speechloop.adapters import register


@register("ASR", "whisper-tiny")
class WhisperTinyASR:
    def __init__(self, model_dir: str = "models/whisper-tiny"):
        ...

    def transcribe(self, audio_path: str) -> str:
        ...
```

注册后即可在 YAML 里用：

```yaml
defaults:
  asr: whisper-tiny
```

## 通过 entry-points 注册

在外部包的 `pyproject.toml`：

```toml
[project.entry-points."speechloop.adapters"]
my-asr = "my_pkg.adapters:register_all"
```

`register_all` 是任意可调用对象，import 时执行注册装饰器即可。
启动时 `speechloop.adapters.discover_entry_points()` 会扫描所有 entry-points。

## HTTP 适配器复用

如果服务接口是简单的 POST：

```yaml
defaults:
  asr: http
adapter_args:
  asr:
    url: http://localhost:8000/transcribe
    field: audio
    text_key: text
```
