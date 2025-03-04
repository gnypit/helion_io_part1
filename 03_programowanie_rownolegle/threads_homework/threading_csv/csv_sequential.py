import os
import pandas as pd
import time
from tqdm import tqdm


def read_csv_sequentially(directory="csv_data", report_file="report.txt"):
    """Czyta pliki CSV sekwencyjnie i zapisuje raport ze statystykami."""
    start_time = time.time()
    report_lines = []

    os.makedirs(directory, exist_ok=True)
    csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    for file_name in tqdm(csv_files, desc="Processing CSV files"):
        file_path = os.path.join(directory, file_name)

        # Wczytaj dane do DataFrame
        df = pd.read_csv(file_path)

        # Oblicz statystyki
        num_rows, num_columns = df.shape
        mean_value = df.mean().mean()  # Średnia wszystkich liczb w pliku
        min_value = df.min().min()  # Najmniejsza liczba
        max_value = df.max().max()  # Największa liczba

        # Zapisz wyniki do raportu
        report_lines.append(
            f"File: {file_name}\n"
            f"Rows: {num_rows}, Columns: {num_columns}\n"
            f"Mean: {mean_value:.5f}, Min: {min_value:.5f}, Max: {max_value:.5f}\n"
            f"{'-' * 40}\n"
        )

    # Zapisz raport do pliku tekstowego
    with open(report_file, "w", encoding="utf-8") as f:
        f.writelines(report_lines)

    end_time = time.time()
    print(f"\nSequential processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")


if __name__ == "__main__":
    read_csv_sequentially()
