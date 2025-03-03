import os
from time import time
from threading import Lock, Thread, current_thread

lock = Lock()  # blokada na raport istniejący we współdzielonej pamięci
report = ""


def process_single_file(file_path):
    """Czyta zawartość pliku i dodaje ją do raportu z komunikatami statusu; jest wykonywana przez pojedynczy wątek."""
    global report
    thread_name = current_thread().name  # Nazwa bieżącego wątku
    # print(f"{thread_name} started processing {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        with lock:  # Zabezpieczenie dostępu do raportu
            report += f"\n=== File: {os.path.basename(file_path)} ===\n"
            report += content
    except Exception as e:
        print(f"{thread_name} encountered an error: {e}")

    print(f"{thread_name} finished processing {file_path}")


def read_files_with_threading(base_dir="text_data", output_file="reports/report_threading.txt"):
    """Czyta pliki tekstowe z folderu i zapisuje ich zawartość do raportu, wypisując status wątków."""
    global report
    threads = []

    for file_name in os.listdir(base_dir):  # dla każdego znalezionego pliku tworzymy wątek
        if file_name.endswith(".txt"):
            file_path = os.path.join(base_dir, file_name)
            t = Thread(target=process_single_file, args=(file_path,))
            threads.append(t)
            t.start()

    for t in threads:
        """To trochę tak, jakbyśmy najpierw rozdzielili rzekę na kilka kanałów. Nie chcemy, żeby woda nam się rozlała 
        potem z tych kanałów, ani ciągnąć ich w nieskończoność. Lepiej jest te kanały połączyć z powrotem w koryto 
        rzeki, która naturalnie potem zbiega do morza.
        
        Tak samo my, tworzymy wątki, bo chcemy równolegle mieć kilka nurtów pracy, ale potem bez sensu jest trzymać
        te biedne wątki w zawieszeniu albo musieć ręcznie kończyć działanie kodu. Lepiej jest zebrać wątki po wykonaniu
        przez nie pracy z powrotem do głównego, który to już w odpowiednim momencie się zakończy. W ten sposób na pewno
        nie wycieknie nam pamięć czy coś takiego.
        
        Alternatywnie moglibyśmy użyć opcji 'deamom', czyli wymusić na tworzonych wątkach, że same siebie eliminują,
        niczym szpieg połykający uśmiercającą pigułkę.
        """
        t.join()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {output_file}")


if __name__ == '__main__':
    start = time()
    read_files_with_threading()
    end = time()

    print(f"Threads executed in {end - start} seconds.")
