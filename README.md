# speechloop

> 语音大模型全链路测试框架 · ASR → LLM → TTS pipeline test harness

[![CI](https://github.com/zqj966/speechloop/actions/workflows/ci.yml/badge.svg)](https://github.com/zqj966/speechloop/actions/workflows/ci.yml)
[![codeql](https://github.com/zqj966/speechloop/actions/workflows/codeql.yml/badge.svg)](https://github.com/zqj966/speechloop/actions/workflows/codeql.yml)
[![python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

`speechloop` 把 ASR、LLM、TTS 三段拼成一条可重放、可断言、可对比的的链路，
用 YAML 描述测试套件，用一行 `speechloop run` 跑完，得到结构化的 JSON / HTML 报告。

它解决的问题：

- **ASR/LLM/TTS 任何一环升级都可能破坏体感**，但每一环单测都"通过"。
- **端到端回归没有标准做法**：人耳听？跑一遍线上？两者都不可复现。
- **指标各家口径不同**：WER / CER / latency p95 / RTF / 语义相似度，需要拢到一处。

`speechloop` 提供：

- 适配器协议（`ASRAdapter` / `LLMAdapter` / `TTSAdapter`）+ 注册表 + 入口点发现
- YAML 套件描述 → 用例展开 → 多线程执行 → 报告生成
- 噪声 / 增益 / 变速 / 截幅等可复现的音频扰动矩阵
- 内置 WER / CER / 语义相似度 / 延迟分位数 / RTF / 阈值断言
- JSON / HTML / Markdown / 控制台 多种 reporter
- CLI 退出码绑定阈值，方便 CI 直接消费

## 安装

```bash
pip install speechloop
# 或者从源码
pip install -e .[dev]
```

## 30 秒跑通

```bash
speechloop init demo
speechloop run demo/suite.yaml --format html -o report.html
```

## YAML 套件示例

```yaml
suite: "demo"
defaults:
  asr: dummy
  llm: echo
  tts: tone
cases:
  - name: "中文问候"
    audio: ./hello.wav
    expected_transcript: "你好"
    expected_response_contains: ["你好"]
    tags: [zh, smoke]
perturbations:
  - kind: noise
    snr_db: [20, 10, 0]
  - kind: gain
    db: [-6, 0, 6]
thresholds:
  wer_max: 0.2
  latency_p95_ms: 1500
```

## 内置适配器

| 名称        | 类型 | 说明                                   |
|-------------|------|----------------------------------------|
| `dummy`     | ASR  | 查表匹配，零外部依赖，用于自检         |
| `energy`    | ASR  | 基于能量分段的极简 ASR                 |
| `http`      | ASR  | 通用 HTTP 接口适配器                   |
| `echo`      | LLM  | 原文返回，用于链路调通                 |
| `regex`     | LLM  | 正则规则驱动的离线 LLM                 |
| `http`      | LLM  | 通用 HTTP 接口适配器                   |
| `quiet`     | TTS  | 生成静默 WAV，验证文本→音频环节        |
| `tone`      | TTS  | 单频正弦波合成器                       |
| `http`      | TTS  | 通用 HTTP 接口适配器                   |

接入自家模型只需实现协议中的几个方法，详见 [docs/adapters.md](docs/adapters.md)。

## 命令行

```text
speechloop init <dir>           生成最小可跑套件
speechloop run <suite.yaml>     执行套件
speechloop report <result.json> 重新渲染报告
```

常用参数：`--format {json,text,html,md}`、`--filter <tag>`、`--workers <N>`、
`--timeout <sec>`、`--dry-run`、`--artifacts-dir <path>`。

## 报告样例

JSON：

```json
{
  "schema": 1,
  "suite": "demo",
  "summary": {"total": 12, "passed": 11, "failed": 1, "wer": 0.07},
  "cases": [...]
}
```

HTML 报告内置 per-case diff、扰动矩阵热力图、p50/p95/p99 折线，详见
[docs/usage.md](docs/usage.md#html-报告)。

## 设计要点

- 适配器 = 协议 + 注册表，业务依赖装进 extras，核心包零依赖（除 PyYAML）
- 扰动 / 重试 / 超时统一在 `runner` 层处理，适配器不需要关心
- 指标是纯函数，输入是 `CaseResult`，方便单测
- 报告器只读 `SuiteResult`，互不依赖

更多见 [docs/architecture.md](docs/architecture.md) 与 [docs/design-notes.md](docs/design-notes.md)。

## 开发

```bash
make install
make lint
make test
```

## 贡献

欢迎 issue / PR，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

MIT

<!-- polish 1 -->

<!-- polish 2 -->
