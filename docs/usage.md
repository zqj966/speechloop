# 使用指南

## 1. 安装

```bash
pip install speechloop
# 含 HTTP 适配器
pip install 'speechloop[http]'
```

## 2. YAML 套件 schema

```yaml
suite: <string>             # 必填，套件名
defaults:                   # 适配器默认配置
  asr: <name>
  llm: <name>
  tts: <name>
cases:
  - name: <string>
    audio: <path or glob>
    expected_transcript: <string>     # 可选
    expected_response_contains: []    # 可选
    tags: []
    timeout_s: 30
perturbations:                        # 可选；每条会与每个 case 做笛卡尔积
  - kind: noise   # noise / gain / tempo
    snr_db: [20, 10]
  - kind: gain
    db: [-6, 0, 6]
thresholds:                           # 可选
  wer_max: 0.2
  cer_max: 0.2
  latency_p95_ms: 1500
include_tags: []                      # 可选，按 tag 过滤
exclude_tags: []
imports:                              # 可选，从另一个 yaml 合并 defaults / thresholds
  - common.yaml
```

## 3. CLI

```bash
speechloop run suite.yaml --format html -o report.html
speechloop run suite.yaml --filter smoke --workers 8 --timeout 10
speechloop run suite.yaml --stream                # 每条用例一行 JSON
speechloop run suite.yaml --dry-run               # 只打印 pipeline
speechloop report result.json --format md         # 把 JSON 转 Markdown
speechloop init demo/                             # 生成最小套件
```

## 4. HTML 报告 (浏览器自包含)

报告包含：

- 顶部 summary 卡片：pass/fail、WER、CER、latency p95
- 用例表：每行展示 case / tags / latency / WER / CER / transcript / response
- 转写文本会被转义，防止 XSS

## 5. 在 CI 中消费

```yaml
- run: speechloop run tests/suite.yaml --format json -o result.json
- run: speechloop report result.json --format md -o $GITHUB_STEP_SUMMARY
```

阈值未通过 → exit code 1，CI 会自动失败。

<!-- polish 4 -->
