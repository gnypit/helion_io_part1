import os
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_csv(file_path):
    """Przetwarza pojedynczy plik CSV i zwraca statystyki."""
    try:
        df = pd.read_csv(file_path)

        num_rows, num_columns = df.shape
        mean_value = df.mean().mean()  # Średnia wszystkich liczb w pliku
        min_value = df.min().min()  # Najmniejsza liczba
        max_value = df.max().max()  # Największa liczba

        return (
            file_path,
            num_rows,
            num_columns,
            mean_value,
            min_value,
            max_value
        )
    except Exception as e:
        return file_path, None, None, None, None, None, str(e)


def read_csv_parallel(directory="csv_data", report_file="csv_wzorcowe_raporty/report_parallel.txt", max_workers=4):
    """Czyta pliki CSV równolegle i zapisuje raport ze statystykami."""
    start_time = time.time()
    report_lines = []

    os.makedirs(directory, exist_ok=True)
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_csv, file): file for file in csv_files}

        for future in tqdm(as_completed(future_to_file), total=len(csv_files), desc="Processing CSV files"):
            result = future.result()
            if len(result) == 7:  # Jeśli wystąpił błąd
                file_name, _, _, _, _, _, error_msg = result
                report_lines.append(f"File: {file_name}\nError: {error_msg}\n{'-' * 40}\n")
            else:
                file_name, num_rows, num_columns, mean_value, min_value, max_value = result
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
    print(f"\nParallel processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")

if __name__ == "__main__":
    read_csv_parallel(max_workers=4)  # Można dostosować liczbę wątków
