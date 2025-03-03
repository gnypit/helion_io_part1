import os
import csv
import time


def read_csv_sequentially(directory="csv_data"):
    """Czyta pliki CSV sekwencyjnie."""
    start_time = time.time()
    data = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            print(f"Data read successfully.")
    end_time = time.time()
    print(f"Sequential read completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    read_csv_sequentially()
