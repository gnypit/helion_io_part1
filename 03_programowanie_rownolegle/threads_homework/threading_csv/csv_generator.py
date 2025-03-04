import csv
import os
import random
from tqdm import tqdm


def generate_large_csv_files(directory="csv_data", num_files=4, num_rows=10 ** 7, num_columns=10):
    """Generuje duże pliki CSV z losowymi liczbami zmiennoprzecinkowymi."""
    os.makedirs(directory, exist_ok=True)

    for i in tqdm(range(num_files), desc="Generating CSV files"):
        file_path = os.path.join(directory, f"data_{i + 1}.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Nagłówki kolumn
            headers = [f"Column_{j}" for j in range(1, num_columns + 1)]
            writer.writerow(headers)
            # Wiersze z losowymi liczbami zmiennoprzecinkowymi
            for _ in range(num_rows):
                row = [random.uniform(0, 100) for _ in
                       range(num_columns)]  # Liczby zmiennoprzecinkowe z zakresu [0, 100]
                writer.writerow(row)

    print(f"Generated {num_files} large CSV files in {directory}")


if __name__ == "__main__":
    generate_large_csv_files()

