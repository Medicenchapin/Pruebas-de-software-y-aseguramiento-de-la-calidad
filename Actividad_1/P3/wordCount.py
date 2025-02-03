import sys
import time
import re
import os
from typing import List, Tuple

def clean_word(word: str) -> str:
    """
    Cleans a word by removing punctuation and converting to lowercase.
    """
    return re.sub(r'[^a-zA-Z]', '', word).lower()


def process_words(filename: str) -> Tuple[List[Tuple[str, int]], int]:
    """
    Reads a file, processes words, and counts their frequency.
    """
    word_count = []
    words_list = []
    total_words = 0 

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Split the line into words
                words = line.strip().split()

                for word in words:
                    clean = clean_word(word)
                    if clean: 
                        words_list.append(clean)
                        total_words += 1 

        # Manually count word occurrences
        for word in words_list:
            found = False
            for i in range(len(word_count)):
                if word_count[i][0] == word:
                    word_count[i] = (word, word_count[i][1] + 1)
                    found = True
                    break
            if not found:
                word_count.append((word, 1))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    if not word_count:
        print("Error: No valid words found in the file.")
        sys.exit(1)

    return sorted(word_count, key=lambda x: x[1], reverse=True), total_words  # Sort by frequency (descending)


def save_results(filename: str, results: List[Tuple[str, int]], total_words: int, elapsed_time: float) -> None:
    """
    Saves the word count results to a file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{'Word':<15} {'Frequency':<10}\n")
        file.write("-" * 30 + "\n")

        for word, count in results:
            file.write(f"{word:<15} {count:<10}\n")

        file.write("-" * 30 + "\n")
        file.write(f"Total Words: {total_words}\n")  # ✅ Added total word count
        file.write(f"Execution Time: {elapsed_time:.6f} seconds\n")


def main() -> None:
    """
    Main function
    """
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    start_time = time.time()

    results, total_words = process_words(input_filename)

    elapsed_time = time.time() - start_time

    # Print results to console
    print(f"{'Word':<15} {'Frequency':<10}")
    for word, count in results:
        print(f"{word:<15} {count:<10}")
    print(f"Total Words: {total_words}")  # ✅ Print total word count
    print(f"Execution Time: {elapsed_time:.6f} seconds")

    # Save results to file
    save_results("WordCountResults.txt", results, total_words, elapsed_time)


if __name__ == "__main__":
    main()
