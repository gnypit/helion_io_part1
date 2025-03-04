import os
import pandas as pd
import time
import threading
from tqdm import tqdm


def process_csv(file_path, results, lock, progress_bar):
    """Przetwarza pojedynczy plik CSV i zapisuje wynik do listy `results`."""
    try:
        df = pd.read_csv(file_path)

        num_rows, num_columns = df.shape
        mean_value = df.mean().mean()  # Średnia wszystkich liczb w pliku
        min_value = df.min().min()  # Najmniejsza liczba
        max_value = df.max().max()  # Największa liczba

        with lock:  # Blokada dla współdzielonej listy wyników
            results.append((file_path, num_rows, num_columns, mean_value, min_value, max_value))
            progress_bar.update(1)

    except Exception as e:
        with lock:
            results.append((file_path, None, None, None, None, None, str(e)))
            progress_bar.update(1)


def read_csv_threading(directory="csv_data", report_file="csv_wzorcowe_raporty/report_threading.txt", max_threads=4):
    """Czyta pliki CSV równolegle za pomocą `threading` i zapisuje raport."""
    start_time = time.time()
    report_lines = []

    os.makedirs(directory, exist_ok=True)
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]

    results = []  # Lista na wyniki przetwarzania
    lock = threading.Lock()  # Blokada do synchronizacji
    progress_bar = tqdm(total=len(csv_files), desc="Processing CSV files", position=0)

    # Tworzymy wątki dla każdego pliku (maksymalnie `max_threads` jednocześnie)
    threads = []
    for file_path in csv_files:
        thread = threading.Thread(target=process_csv, args=(file_path, results, lock, progress_bar))
        thread.start()
        threads.append(thread)

        # Jeśli liczba aktywnych wątków przekracza `max_threads`, czekamy na ich zakończenie
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    # Czekamy na zakończenie pozostałych wątków
    for t in threads:
        t.join()

    progress_bar.close()

    # Tworzenie raportu
    for result in results:
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
    print(f"\nThreading processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")


if __name__ == "__main__":
    read_csv_threading(max_threads=4)  # Można dostosować liczbę wątków
