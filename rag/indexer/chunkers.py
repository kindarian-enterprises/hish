import re
from typing import List

import tiktoken


# Simple tokenizer-based chunker for markdown/text/code
def chunk_text(
    text: str, max_tokens=300, overlap=40, model="gpt-3.5-turbo"
) -> List[str]:
    enc = (
        tiktoken.get_encoding("cl100k_base")
        if "gpt" in model
        else tiktoken.get_encoding("cl100k_base")
    )
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunks.append(enc.decode(tokens[start:end]))
        start = end - overlap if end - overlap > start else end
    return [c.strip() for c in chunks if c.strip()]


def prefer_md_splits(text: str) -> List[str]:
    # split on headings / lists / blank lines for better semantic boundaries
    parts = re.split(r"(?m)^(#{1,6}\s.*$)|^\s*$|^[-*]\s+", text)
    # filter out None and trivial whitespace
    return [p.strip() for p in parts if p and p.strip()]
