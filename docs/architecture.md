# 架构

```
            ┌──────────┐    ┌──────────┐    ┌──────────┐
audio.wav ─▶│  ASR     │─▶  │  LLM     │─▶  │  TTS     │─▶ out.wav
            └──────────┘    └──────────┘    └──────────┘
                  │               │               │
                  ▼               ▼               ▼
            ┌──────────────────────────────────────────┐
            │  Runner（扰动、超时、重试、并行）         │
            └──────────────────────────────────────────┘
                                  │
                                  ▼
                            ┌──────────┐
                            │ Metrics  │
                            └──────────┘
                                  │
                                  ▼
                  ┌──────────────────────────────┐
                  │ Reporters (json/html/md/...) │
                  └──────────────────────────────┘
```

## 模块拆分

- `adapters/` —— ASR/LLM/TTS 协议 + 注册表 + 内置实现
- `runner.py` —— 把 case × perturbation 展开为任务，控制并发/超时/重试
- `metrics/` —— WER/CER/相似度/延迟/RTF/阈值
- `reporters/` —— 多格式渲染
- `suite.py` —— YAML → `Suite` 对象
- `audio.py` —— WAV I/O + 扰动原语
- `perturb.py` —— 扰动矩阵展开
- `cli.py` —— `speechloop run/init/report`

## 不在范围

- 真实声学模型 —— 用 `http` 适配器接外部服务
- 评分模型 —— `similarity` 故意做成 Jaccard，需要更准的请自行注册新指标

# noted
