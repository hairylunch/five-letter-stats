#!/usr/bin/env python3.9

import string
import sys


def get_words():
    with open('sgb-words.txt', 'r') as f:
        words = f.read().splitlines()
    return words


def get_stats(words: list[str]) -> dict:
    stats = {}
    for _ in string.ascii_lowercase:
        stats[_] = {'count': 0,
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0
                    }
    for word in words:
        for i, letter in enumerate(word):
            stats[letter]['count'] += 1
            stats[letter][i] += 1

    return stats

def normalize_stats(stats: dict, words: list[str]) -> dict:
    # normalize
    word_count = float(len(words))
    normalized_stats = {x: {} for x in string.ascii_lowercase}
    for letter in stats:
        for k, v in stats[letter].items():
            normalized_stats[letter][k] = v/word_count

    return normalized_stats

def main():
    words = get_words()
    stats = get_stats(words)
    print(stats)
    print(normalize_stats(stats, words))

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
