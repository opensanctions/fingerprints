import os
from collections import defaultdict
from typing import List, Tuple


def common_partial_phrases(
    phrases: List[str], min_length: int, max_length: int
) -> List[Tuple[str, int]]:
    partial_phrases = defaultdict(int)

    for phrase in phrases:
        words = phrase.split()
        n = len(words)
        for length in range(min_length, max_length + 1):
            for start in range(n - length + 1):
                partial_phrase = " ".join(words[start : start + length])
                partial_phrases[partial_phrase] += 1

    sorted_phrases = sorted(
        partial_phrases.items(), key=lambda x: (len(x[0].split()), x[1]), reverse=True
    )
    return sorted_phrases


def process_file(file_path: str, min_length: int, max_length: int) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    result = common_partial_phrases(lines, min_length, max_length)

    # Filter phrases that appear at least 10 times and sort in descending order
    filtered_result = [
        (phrase, frequency) for phrase, frequency in result if frequency >= 200
    ]

    for phrase, frequency in filtered_result:
        print(f"{phrase}: {frequency}")


file_name = "tools/output.csv"
min_length = 4
max_length = 7

if os.path.exists(file_name):
    process_file(file_name, min_length, max_length)
else:
    print(f"File '{file_name}' not found in the current directory.")
