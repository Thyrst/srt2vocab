import string
import re
from collections.abc import Iterator
from typing import Optional

import srt


TAG_RE = re.compile(r"<[^>]+>")


def remove_tags(text: str) -> str:
    return TAG_RE.sub("", text)


def normalize_word(word: str) -> Optional[str]:
    """
    Returns the word lowercased and stripped of punctuation marks.
    If the word is shortened using apostrophe, is a number or is deformed then `None` is returned.

    >>> normalize_word("Peter!")
    'peter'
    >>> normalize_word("'sup")
    >>> normalize_word("4,000")
    >>> normalize_word("bád")
    >>> normalize_word("+")
    >>> normalize_word("<i>Dad\u2019s…?</i>")
    'dad'
    """
    word = remove_tags(word)

    punctuation_marks = string.punctuation.replace("'", "") + "…"
    word = word.strip(punctuation_marks)

    if word.endswith("'s") or word.endswith("\u2019s"):
        word = word[:-2]
    elif word.endswith("s'") or word.endswith("s\u2019"):
        word = word[:-1]

    word = word.lower()

    if word and all(c in string.ascii_lowercase for c in word):
        return word


def parse_words_from_line(line: srt.Subtitle) -> Iterator[str]:
    for word in line.content.split():
        if normalized := normalize_word(word):
            yield normalized


def parse_words(srt_raw_data: str) -> Iterator[str]:
    lines = srt.parse(srt_raw_data)
    for line in lines:
        for word in parse_words_from_line(line):
            yield word
