"""文本归一化与简易分词。"""
from __future__ import annotations
import re
import unicodedata

_PUNCT_RE = re.compile(r"[\W_]+", re.UNICODE)
_CN_SPLIT = re.compile(r"([\u4e00-\u9fff])")


def normalize(text: str) -> str:
    """大小写归一 + 去多余空白 + 标点剥离 + NFKC。"""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # 统一换行
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip().lower()
    text = _PUNCT_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_zh(text: str) -> list[str]:
    """中文按字、ASCII 按词（空格切分）。"""
    text = normalize(text)
    if not text:
        return []
    tokens: list[str] = []
    buf: list[str] = []
    for part in _CN_SPLIT.split(text):
        if not part:
            continue
        if _CN_SPLIT.fullmatch(part):
            if buf:
                tokens.extend("".join(buf).split())
                buf.clear()
            tokens.append(part)
        else:
            buf.append(part)
    if buf:
        tokens.extend("".join(buf).split())
    return [t for t in tokens if t]


def tokenize_en(text: str) -> list[str]:
    return normalize(text).split()

# CR/LF already collapsed in normalize()
