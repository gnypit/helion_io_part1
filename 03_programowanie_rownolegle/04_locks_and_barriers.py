import threading
from time import sleep
import os

order_dir = 'orders'

"""Raport dot. zamówień jest do wspólnego użytku przez różne wątki, więc trzeba go odpowiednio zabezpieczyć. Ponadto
chcemy, aby wątki czekały na kolejny przydział zadań (czyli synchronizować ich pracę), więc tworzymy barierę, która
działa jak tama - puści wątki dopiero, gdy zadana ich liczba dotrze do bariery."""
report = []
report_lock = threading.Lock()  # Zamykamy raport na kłódkę i tylko jeden wątek naraz może mieć do niej kluczyk
barrier = threading.Barrier(10)  # Jest 10 zamówień, a każde będzie miało sój wątek


def process_order_file(path):
    """Funkcja pobierająca dane zamówienia z pliku o konkretnej, podanej ścieżce. Po uzyskaniu dostępu do
    współdzielonego z innymi wątkami raportu dot. zamówień, dane pobrane z pliku są tam dodawane, po czym wątek
    czeka na swoje dalsze losy na barierze - dzięki temu praca wątków będzie zsynchronizowana."""
    print(f"Otrzymano ścieżkę pliku, jest on analizowany.")

    with open(path, 'r') as file:
        lines = file.readlines()

    order_id = int(lines[0].split(":")[1].strip())
    client_name = lines[1].split(":")[1].strip()
    items_line = lines[2].split(":")[1].strip()
    items = [(item.split('(')[0].strip(), int(item.split('(')[1].split(')')[0])) for item in items_line.split(',')]
    status = lines[5].split(":")[1].strip()

    """Symulujemy przetwarzanie danych"""
    sleep(1)

    total_items = sum(quantity for item, quantity in items)

    """Przygotowujemy podsumowanie danego zamówienia do wstawienia do raportu"""
    order_summary = {
        "order_id": order_id,
        "client_name": client_name,
        "total_items": total_items,
        "status": status
    }

    """Prosimy o dostęp do raportu, który jest we wspólnej pamięci"""
    with report_lock:
        report.append(order_summary)

    """Czekamy na barierze, aż wszystkie wątki zakończą pracę - dzięki temu je synchronizujemy. Gdyby była kolejna
    porcja danych do przetworzenia, zadbalibyśmy w ten sposób o równoległy start."""
    barrier.wait()

    print(f"Plik przeanalizowany z powodzeniem.")


if __name__ == '__main__':
    """Inicjujemy wątki i listę na ich przechowywanie"""
    threads = []
    for file_name in os.listdir(order_dir):
        file_path = os.path.join(order_dir, file_name)
        if file_path.endswith(".txt"):
            thread = threading.Thread(target=process_order_file, args=(file_path,))
            threads.append(thread)
            thread.start()

    """Zbieramy wątki z bariery i je zamykamy"""
    for thread in threads:
        thread.join()

    """Zwracamy końcowy raport - zwracamy uwagę na kolejność ID zamówień w raporcie!!! Jest inna niż kolejność, w jakiej
    inicjowaliśmy wątki i przekazywaliśmy im pliki."""
    print(f"Końcowy raport:")
    for entry in report:
        print(entry)
