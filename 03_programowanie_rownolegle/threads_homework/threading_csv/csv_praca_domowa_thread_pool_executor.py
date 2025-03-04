import os
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_csv(file_path):
    """Przetwarza pojedynczy plik CSV i zwraca statystyki."""
    try:
        df = pd.read_csv(______)

        num_rows, num_columns = ______
        mean_value = ______
        min_value = ______
        max_value = ______

        return file_path, num_rows, num_columns, mean_value, min_value, max_value
    except Exception as e:
        return file_path, None, None, None, None, None, str(e)

def read_csv_parallel(directory="csv_data", report_file="report_parallel.txt", max_workers=4):
    """Czyta pliki CSV równolegle i zapisuje raport ze statystykami."""
    start_time = time.time()
    report_lines = []

    os.makedirs(directory, exist_ok=True)
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]

    with ThreadPoolExecutor(max_workers=______) as executor:
        # Przekaż zadanie do executora
        ______

        for ______ in tqdm(as_completed(______), total=len(csv_files), desc="Processing CSV files"):
            result = ______
            if len(result) == 7:  # Jeśli wystąpił błąd
                file_name, _, _, _, _, _, error_msg = result
                report_lines.append(f"File: {file_name}\nError: {error_msg}\n{'-' * 40}\n")
            else:
                # Przekaż zebrane przez funkcję `process_csv` dane do raportu
                ______

    # 📝 Zapisz raport do pliku tekstowego
    with open(report_file, "w", encoding="utf-8") as f:
        ______

    end_time = time.time()
    print(f"\nParallel processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")

if __name__ == "__main__":
    read_csv_parallel(max_workers=4)
