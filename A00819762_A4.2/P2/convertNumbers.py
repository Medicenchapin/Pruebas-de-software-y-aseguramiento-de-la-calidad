import sys
import time
import re
from typing import List, Tuple


def clean_number(line: str) -> str:
    """
    Cleans a line by replacing non-numeric characters with spaces.
    """
    line = re.sub(r'[a-zA-Z]', ' ', line)
    line = re.sub(r'[,;:]', '.', line)
    line = re.sub(r'[^0-9.\-]', '', line).strip()
    return line


def decimal_to_binary(n: int) -> str:
    """
    Converts a decimal number to binary using basic division algorithm.
    """
    if n == 0:
        return "0"

    binary = ""
    is_negative = n < 0
    n = abs(n)

    while n > 0:
        binary = str(n % 2) + binary
        n //= 2

    return f"-{binary}" if is_negative else binary


def decimal_to_hexadecimal(n: int) -> str:
    """
    Converts a decimal number to hexadecimal using basic division algorithm.
    """
    if n == 0:
        return "0"

    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    is_negative = n < 0
    n = abs(n)

    while n > 0:
        hexadecimal = hex_chars[n % 16] + hexadecimal
        n //= 16

    return f"-{hexadecimal}" if is_negative else hexadecimal


def process_numbers(filename: str) -> List[Tuple[int, int, str, str]]:
    """
    Reads a file, processes numbers, and converts them to binary and hexadecimal.
    """
    results = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line = clean_number(line)

                # Ensure it's a valid integer
                if cleaned_line and re.fullmatch(r'-?\d+', cleaned_line):
                    try:
                        num = int(cleaned_line)
                        bin_value = num % 256
                        binary = decimal_to_binary(bin_value)
                        hexadecimal = decimal_to_hexadecimal(bin_value)
                        results.append((num, bin_value, binary, hexadecimal))
                    except ValueError:
                        print(f"Skipping invalid data: '{line.strip()}'")
                else:
                    print(f"Skipping invalid line: '{line.strip()}'")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    if not results:
        print("Error: No valid numbers found in the file.")
        sys.exit(1)

    return results


def save_results(filename: str, results: List[Tuple[int, int, str, str]], elapsed_time: float) -> None:
    """
    Saves the converted numbers to a file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{'ITEM':<5} {'TC1':<10} {'BIN':<10} {'Binary':<20} {'Hexadecimal':<10}\n")
        file.write("=" * 60 + "\n")

        for idx, (num, bin_value, binary, hex_value) in enumerate(results, start=1):
            file.write(f"{idx:<5} {num:<10} {bin_value:<10} {binary:<20} {hex_value:<10}\n")

        file.write("=" * 60 + "\n")
        file.write(f"Execution Time: {elapsed_time:.6f} seconds\n")


def main() -> None:
    """
    Main function
    """
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    start_time = time.time()

    results = process_numbers(input_filename)

    elapsed_time = time.time() - start_time

    # Print results to console
    print(f"{'ITEM':<5} {'TC1':<10} {'BIN':<10} {'Binary':<20} {'Hexadecimal':<10}")
    print("-" * 60)
    for idx, (num, bin_value, binary, hex_value) in enumerate(results, start=1):
        print(f"{idx:<5} {num:<10} {bin_value:<10} {binary:<20} {hex_value:<10}")

    print("-" * 60)
    print(f"Execution Time: {elapsed_time:.6f} seconds")

    # Save results to file
    save_results("ConvertionResults.txt", results, elapsed_time)


if __name__ == "__main__":
    main()
