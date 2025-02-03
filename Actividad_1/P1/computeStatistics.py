import sys
import time
import re 

def read_numbers_from_file(filename):
    """
    Reads numbers from a file, removes non-numeric characters, and handles encoding issues.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            numbers = []
            for line in file:
                # Remove all non-numeric characters except digits, dots, and minus signs
                clean_line = re.sub(r'[^0-9,.-]', '', line).strip()

                # Remove commas (used as thousand separators) to correctly parse as floats
                clean_line = clean_line.replace(',', '')

                if clean_line:
                    try:
                        numbers.append(float(clean_line))
                    except ValueError:
                        print(f"Skipping invalid data: '{line.strip()}'")

        # If no valid numbers are found, exit with an error
        if not numbers:
            print("Error: The file is empty or contains only invalid data.")
            sys.exit(1)

        return numbers
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def compute_statistics(numbers):
    """
    Computes descriptive statistics: mean, median, mode, variance, and standard deviation.
    """
    n = len(numbers)

    # Mean: Sum all numbers and divide by count
    mean = sum(numbers) / n

    # Median: Sort the numbers and select the middle one
    sorted_nums = sorted(numbers)
    mid = n // 2
    median = (sorted_nums[mid] if n % 2 != 0 else
              (sorted_nums[mid - 1] + sorted_nums[mid]) / 2)

    # Mode: Find the most frequently occurring number
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    mode = max(freq, key=freq.get)

    # Variance: Measure of how spread out numbers are from the mean
    variance = sum((x - mean) ** 2 for x in numbers) / n

    # Standard Deviation: Square root of variance
    std_dev = variance ** 0.5

    return mean, median, mode, variance, std_dev


def save_results(filename, mean, median, mode, variance, std_dev, elapsed_time):
    """
    Saves computed statistics to a results file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Mean: {mean:.2f}\n")
        file.write(f"Median: {median:.2f}\n")
        file.write(f"Mode: {mode:.2f}\n")
        file.write(f"Variance: {variance:.2f}\n")
        file.write(f"Standard Deviation: {std_dev:.2f}\n")
        file.write(f"Execution Time: {elapsed_time:.6f} seconds\n")


def main():
    """
    Main execution function.
    """
    # Ensure correct usage with exactly one argument (file name)
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()

    numbers = read_numbers_from_file(filename)
    mean, median, mode, variance, std_dev = compute_statistics(numbers)

    elapsed_time = time.time() - start_time

    # Print results to console
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Mode: {mode:.2f}")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    print(f"Execution Time: {elapsed_time:.6f} seconds")

    # Save results to file
    save_results("StatisticsResults.txt", mean, median, mode, variance, std_dev, elapsed_time)


if __name__ == "__main__":
    main() 
