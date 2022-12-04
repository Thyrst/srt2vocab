#!/usr/bin/env python
import argparse, pathlib
from parse_words import parse_words


parser = argparse.ArgumentParser(description="create a wordlist from a subtitles file")
parser.add_argument("srt", type=pathlib.Path, help="SRT file to extract new words from")
parser.add_argument(
    "wordlist",
    nargs="+",
    type=pathlib.Path,
    help="file that contain common or already known words to discard from the result",
)
parser.add_argument(
    "-o", "--output", type=pathlib.Path, help="output file", default="output.txt"
)
args = parser.parse_args()


with open(args.srt) as f:
    data = f.read()

discarded_words = set()
for filename in args.wordlist:
    with open(filename) as f:
        words = f.read().splitlines()
        discarded_words.update(map(str.lower, words))

with open(args.output, "w") as f:
    for word in parse_words(data):
        if word not in discarded_words:
            f.write(word + "\n")
            discarded_words.add(word)
