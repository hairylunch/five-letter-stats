#!/usr/bin/env python3.9

import collections
import itertools
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

def normalize_stats(stats: dict, word_count: float) -> dict:
    # normalize
    normalized_stats = {x: {} for x in string.ascii_lowercase}
    for letter in stats:
        for k, v in stats[letter].items():
            normalized_stats[letter][k] = v/word_count

    return normalized_stats


def get_word_points_considering_dist_and_positions(words: list[str], normalized_stats: dict) -> dict:
    # naive with absolute frequency and positional frequency weight evenly (assuming normalized stats)
    # no handling of duplicates or anything
    scores = {w: 0 for w in words}
    for word in words:
        score = 0
        for i, letter in enumerate(word):
            score += normalized_stats[letter]['count'] + normalized_stats[letter][i]
        scores[word] = score
    return dict(sorted(scores.items(), key=lambda x: x[1]))


def get_points_for_pairs_of_words(word_scores: dict, normalized_stats: dict) -> dict:
    # considers words in pairs, removing duplicate frequencies
    # brute force, but should be fine with this small data set
    all_scores = {}
    loop = 1
    for first_word, s1 in word_scores.items():
        print(loop)
        for second_word, s2 in dict(itertools.islice(word_scores.items(), loop, None)).items():
            if first_word != second_word:
                score = s1 + s2
                frequency_by_letter = collections.Counter(first_word + second_word)
                # print(first_word, second_word, s1, s2, frequency_by_letter)
                for letter, freq in frequency_by_letter.items():
                    if freq > 1:
                        score -= (normalized_stats[letter]['count'] * (freq-1))
                all_scores[f"{first_word},{second_word}"] = score
        loop += 1

    return dict(sorted(all_scores.items(), key=lambda x: x[1]))


def main():
    words = get_words()
    word_count = float(len(words))
    stats = get_stats(words)
    print(stats)
    normalized_stats = normalize_stats(stats, word_count)
    dumb_points = get_word_points_considering_dist_and_positions(words, normalized_stats)
    print(dumb_points)
    print(get_points_for_pairs_of_words(dumb_points, normalized_stats))

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
