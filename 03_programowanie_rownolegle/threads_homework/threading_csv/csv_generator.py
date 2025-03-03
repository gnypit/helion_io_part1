import csv
import os
import random
import string
from tqdm import tqdm


def generate_large_csv_files(directory="csv_data", num_files=40, num_rows=10 ** 6, num_columns=10):
    """Generuje duże pliki CSV z losowymi danymi."""
    os.makedirs(directory, exist_ok=True)

    for i in tqdm(range(num_files)):
        file_path = os.path.join(directory, f"data_{i + 1}.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Nagłówki kolumn
            headers = [f"Column_{j}" for j in range(1, num_columns + 1)]
            writer.writerow(headers)
            # Wiersze z losowymi danymi
            for _ in range(num_rows):
                row = [
                    ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    for _ in range(num_columns)
                ]
                writer.writerow(row)
    print(f"Generated {num_files} large CSV files in {directory}")


if __name__ == "__main__":
    generate_large_csv_files()
