# 参与贡献

感谢你愿意为 `speechloop` 出一份力。

## 开发流程

```bash
git clone https://github.com/zqj966/speechloop.git
cd speechloop
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pre-commit install
```

跑测试：

```bash
make test
```

## 提交

- 使用 [Conventional Commits](https://www.conventionalcommits.org/) 风格（不强制，但推荐）。
- 一个 PR 一个关注点；不要把无关重构混进 feature PR。
- 新增代码需要附带测试；改 bug 也尽量附带 regression test。

## 添加新适配器

实现 `ASRAdapter` / `LLMAdapter` / `TTSAdapter` 协议中的对应方法，注册到全局 registry：

```python
from speechloop.adapters import register, ASRAdapter

@register("ASR", "my-asr")
class MyASR(ASRAdapter):
    def transcribe(self, audio, sample_rate):
        ...
```

或者通过 `entry_points` 注册（详见 docs/adapters.md）。

## 风格

```bash
make lint
make fmt
```

## 报告 bug

请在 issue 模板里附上：
- 复现步骤（最好是最小 YAML）
- 期望 vs 实际
- 环境（Python 版本、OS、`pip freeze | grep speechloop`）
