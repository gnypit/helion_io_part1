import os
import pandas as pd
import time
import threading
from tqdm import tqdm


def process_csv(file_path, results, lock, progress_bar):
    """Przetwarza pojedynczy plik CSV i zapisuje wynik do listy `results`."""
    try:
        df = pd.read_csv(______)

        num_rows, num_columns = ______
        mean_value = ______
        min_value = ______
        max_value = ______

        # 📝 Blokada dostępu do `results` w celu synchronizacji pracy pomiędzy wieloma wątkami
        with ______:
            results.append((file_path, num_rows, num_columns, mean_value, min_value, max_value))
            progress_bar.update(1)

    except Exception as e:
        with ______:
            results.append((file_path, None, None, None, None, None, str(e)))
            progress_bar.update(1)


def read_csv_threading(directory="csv_data", report_file="report_threading.txt", max_threads=4):
    """Czyta pliki CSV równolegle za pomocą `threading` i zapisuje raport."""
    start_time = time.time()
    report_lines = []

    os.makedirs(directory, exist_ok=True)
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]

    results = []  # Lista na wyniki przetwarzania
    lock = ______  # Stwórz blokadę dla współdzielonych zasobów
    progress_bar = tqdm(total=len(csv_files), desc="Processing CSV files", position=0)

    threads = []
    for file_path in csv_files:
        # Utwórz, uruchom i zachowaj wątek dla danego pliku
        ______

        # 📝 Jeśli liczba aktywnych wątków przekracza `max_threads`, czekamy na ich zakończenie
        if len(threads) >= max_threads:
            for t in ______:
                t.join()
            threads = []

    # 📝 Czekamy na zakończenie pozostałych wątków
    for t in ______:
        t.join()

    progress_bar.close()

    # 📝 Zapisz raport do pliku (analogicznie do wersji sekwencyjnej)
    with open(report_file, "w", encoding="utf-8") as f:
        ______

    end_time = time.time()
    print(f"\nThreading processing completed in {end_time - start_time:.2f} seconds.")
    print(f"Report saved as '{report_file}'.")


if __name__ == "__main__":
    read_csv_threading(max_threads=4)
