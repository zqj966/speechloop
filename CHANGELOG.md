# Changelog

所有显著变更都会记录在这里。本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [0.3.0] - 2026-06

### Added
- Markdown reporter
- 扰动矩阵展开 + 可复现 seed
- 每用例 artifact 输出目录
- HTTP-based 适配器（ASR/LLM/TTS）

### Changed
- `SilentTTS` 重命名为 `QuietTTS`（注册名仍为 `quiet`）
- HTML reporter 增加 per-case diff 视图

### Fixed
- 空 WAV 不再抛出 IndexError
- HTML 报告中转写文本现在会被转义

## [0.2.0] - 2026-05

### Added
- 并行执行 + per-case 超时 + transient 重试
- WER/CER 归一化前置
- TOML 配置 + 环境变量覆盖

### Changed
- 重构 reporters 共享基类

## [0.1.0] - 2026-04

### Added
- 初始版本：YAML 套件 / Dummy 适配器 / WER+CER / JSON+HTML reporter / CLI
