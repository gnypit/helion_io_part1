import threading
import time
import requests
import numpy as np


def cpu_bound_task(size, number_of_iterations):
    """Mnożenie dużych macierzy"""
    print(f"Thread-{threading.current_thread().name}: Rozpoczynanie mnożenia macierzy...")

    for _ in range(number_of_iterations):  # wiele iteracji mnożenia dwóch macierzy
        A = np.random.rand(size, size)  # tworzenie pierwszej macierzy z losowymi wartościami
        B = np.random.rand(size, size)  # tworzenie drugiej macierzy z losowymi wartościami
        result = np.dot(A, B)  # mnożenie macierzy po raz pierwszy
        new_result = np.dot(result, result)  # wymnażamy wynik (pierwszego mnożenia) z samym sobą

    print(f"Thread-{threading.current_thread().name}: zakończono mnożenie macierzy.")


def io_bound_task(urls):
    """Pobiera dane z podanych URL"""
    print(f"Thread-{threading.current_thread().name}: Rozpoczynanie pobierania danych...")

    for url in urls:
        print(f"Thread-{threading.current_thread().name}: Pobieranie z {url}...")

        try:
            response = requests.get(url, timeout=5)
            print(f"Thread-{threading.current_thread().name}: Otrzymano {len(response.content)} bajtów z {url}")
        except requests.RequestException as e:
            print(f"Thread-{threading.current_thread().name}: Nie udało się pobrać danych z {url}: {e}")

    print(f"Thread-{threading.current_thread().name}: Zakończenie pobierania danych.")


def main():
    """Najpierw wersja równoległa, potem sekwencyjna, dla porównania czasu."""
    url_list = [
        "https://httpbin.org/get",
        "https://www.python.org",
        "https://www.example.com",
        "https://www.github.com",
        "https://www.stackoverflow.com"
    ]

    """Najpierw multithreading:"""
    print(f"Atakujemy problem równoległymi wątkami.")
    start = time.time()

    """Tworzenie wątków"""
    thread1 = threading.Thread(target=io_bound_task, args=(url_list,), name="IO-Thread")
    thread2 = threading.Thread(target=cpu_bound_task, args=(100, 10000), name="CPU-Thread")

    """Start wątków"""
    thread1.start()
    thread2.start()

    """Czekamy na wykonanie zadań i sprzątamy"""
    thread1.join()
    thread2.join()

    end = time.time()
    print(f"Wszystkie zadania wykonane w {round(end - start, 2)} sekund.")

    """Teraz wersja sekwencyjna:"""
    print(f"Atakujemy problem sekwencyjnie")
    start = time.time()

    io_bound_task(urls=url_list)
    cpu_bound_task(size=100, number_of_iterations=10000)

    end = time.time()
    print(f"Wszystkie zadania wykonane w {round(end - start, 2)} sekund.")


if __name__ == '__main__':
    main()