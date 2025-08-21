# speechloop

> 语音大模型全链路测试框架

![CI](https://github.com/zqj966/speechloop/actions/workflows/ci.yml/badge.svg)

`speechloop` 把 ASR/LLM/TTS 三段拼成一条可重放、可断言、可对比的链路。

## 安装

```bash
pip install speechloop
```

## 30 秒跑通

```bash
speechloop init demo
speechloop run demo/suite.yaml --format html -o report.html
```
