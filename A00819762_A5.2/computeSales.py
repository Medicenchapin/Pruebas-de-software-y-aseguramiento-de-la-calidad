import json
import sys
import time


def load_json_file(filename):
    """Load JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File {filename} invalid JSON.")
        sys.exit(1)


def compute_total_sales(price_catalogue, sales_record):
    """Calculate total sales cost."""
    product_prices = {
        item['title']: item['price']
        for item in price_catalogue
    }
    total_cost = 0.0
    errors = []

    for sale in sales_record:
        product_name = sale['Product']
        quantity = sale['Quantity']

        if product_name not in product_prices:
            errors.append(
                f"'{product_name}' not found in catalog prices."
            )
            continue

        total_cost += product_prices[product_name] * quantity

    return total_cost, errors


def main():
    """Main function to execute."""

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    start_time = time.time()

    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)

    total_cost, errors = compute_total_sales(price_catalogue, sales_record)

    execution_time = time.time() - start_time

    print("Total sales cost: ${:.2f}".format(total_cost))
    print("Execution time: {:.4f} seconds".format(execution_time))
    if errors:
        print("\nErrors:")
        for error in errors:
            print(error)

    with open("SalesResults.txt", "w", encoding='utf-8') as results_file:
        results_file.write("Total sales cost: ${:.2f}\n".format(total_cost))
        results_file.write(
            "Execution time: {:.4f} seconds\n".format(execution_time)
        )
        if errors:
            results_file.write("\nErrors:\n")
            for error in errors:
                results_file.write(error + "\n")


if __name__ == "__main__":
    main()
