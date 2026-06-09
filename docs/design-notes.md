# 设计笔记

## 为什么不直接用 `pytest-asyncio` 之类？

`speechloop` 想覆盖的链路里，每一段都可能是 RPC、子进程、外部服务，
直接套 `pytest` 写起来会变成"包一层 fixture 再包一层 mock"。
把 suite 描述独立成 YAML，让"加 case"不需要写 Python。

## 为什么核心包只依赖 PyYAML？

- ASR/LLM/TTS 是注入式适配器，业务依赖装到 extras
- WAV 处理只用标准库 `wave`
- 指标都是纯 Python

这样在 CI、嵌入式、容器里都很轻。

## 为什么相似度只用 Jaccard？

更精确的相似度需要 embedding 模型，硬塞进核心包不合适。
真要用 cosine + sentence-transformers，注册一个新指标即可：

```python
from speechloop.metrics import wer  # noqa
# 在你自己的包里再 register 一个就行
```

## 故意没有做的事

- 不做实时流式 ASR/TTS 评测 —— 不是这条 issue 的需求
- 不做对抗样本生成 —— 太特化
- 不维护内置语料库 —— 各家差异太大
