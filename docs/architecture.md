# 架构

初稿：speechloop 把 ASR/LLM/TTS 三段适配器串成 pipeline，
由 runner 调度，metrics 打分，reporters 渲染输出。
