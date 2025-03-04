import os
import pandas as pd
import time
from tqdm import tqdm

def read_csv_sequentially(directory="csv_data", report_file="report.txt"):
    """Czyta pliki CSV SEKWENCYJNIE i zapisuje raport ze statystykami."""
    start_time = time.time()
    report_lines = []

    # 📝 Stwórz katalog `directory`, jeśli nie istnieje
    # 📌 Użyj os.makedirs() z parametrem `exist_ok=True`

    # 📝 Pobierz listę wszystkich plików CSV w katalogu
    # 📌 Wykorzystaj os.listdir() i sprawdź, czy kończą się na ".csv"

    # 📝 Przetwarzaj pliki w pętli, wyświetlając pasek postępu tqdm
    for file_name in tqdm(______, desc="Processing CSV files"):
        file_path = os.path.join(directory, file_name)

        # 📝 Wczytaj plik CSV do DataFrame
        df = pd.read_csv(______)

        # 📝 Pobierz liczbę wierszy i kolumn
        num_rows, num_columns = ______

        # 📝 Oblicz średnią, min i max dla wszystkich wartości numerycznych
        mean_value = ______
        min_value = ______
        max_value = ______

        # 📝 Dodaj wynik do listy `report_lines` (formatowanie tekstu)
        report_lines.append(
            f"File: {file_name}\n"
            f"Rows: {num_rows}, Columns: {num_columns}\n"
            f"Mean: {mean_value:.5f}, Min: {min_value:.5f}, Max: {max_value:.5f}\n"
            f"{'-' * 40}\n"
        )

    # 📝 Zapisz `report_lines` do pliku tekstowego
    with open(report_file, "w", encoding="utf-8") as f:
        ______

    end_time = time.time()
    print(f"\nSequential processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")

if __name__ == "__main__":
    read_csv_sequentially()
