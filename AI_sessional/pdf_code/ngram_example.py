"""
Simple bigram (n=2) example matching the PDF snippet.
"""
from __future__ import annotations
from collections import defaultdict


def build_bigrams(text: str) -> dict[tuple[str, ...], list[str]]:
    words = text.split()
    n = 2  # bigram
    ngrams: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for i in range(len(words) - n):
        key = tuple(words[i : i + n - 1])
        ngrams[key].append(words[i + n - 1])
    return dict(ngrams)


if __name__ == "__main__":
    sample = "I love AI and I love Python"
    print(build_bigrams(sample))
