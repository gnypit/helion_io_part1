import os
import csv
import time
from threading import Thread, Lock, current_thread

data = []  # Wspólna lista na dane
mutex = Lock()


def read_csv_thread(file_path):
    """Czyta jeden plik CSV."""
    global data
    local_data = []
    thread_name = current_thread().name  # Nazwa bieżącego wątku
    print(f"{thread_name} started processing {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            local_data.append(row)
    # Zapis do współdzielonej listy z użyciem blokady
    with mutex:
        data.extend(local_data)

    print(f"{thread_name} finished processing {file_path}")


def read_csv_with_threading(directory="csv_data"):
    """Czyta pliki CSV równolegle przy użyciu wątków."""
    start_time = time.time()
    threads = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            t = Thread(target=read_csv_thread, args=(file_path,))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Threaded read completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    read_csv_with_threading()
