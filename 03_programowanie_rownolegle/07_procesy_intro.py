from multiprocessing import Process, Array, Manager, Lock

"""Tworzymy zmienne globalne: zwykłą listę (tablicę) oraz dwie współdzielone - z blokadą i bez."""
zwykla_lista = [0] * 10  # [0, 0, ...] - 10 zer
sprytna_lista = Array('i', [0] * 10, lock=False)
sprytna_lista_z_blokada = Array('i', [0] * 10)

def modyfikuj_zwykla_liste():
    global zwykla_lista
    zwykla_lista[0] = 42  # ustawiamy wartość na wybranym indeksie listy

def modyfikuj_sprytna_liste(lista: Array, lista_z_blokada: Array):
    global zwykla_lista
    zwykla_lista[1] = 42  # spróbujemy zmienić wartość zmiennej globalnej

    with lista_z_blokada.get_lock():  # prosimy o dostęp do listy z blokadą
        lista_z_blokada[0] = 42

    lista[0] = 42  # ustalamy wartość na zmiennej typu Array bez blokady

def modyfikuj_slownik(slownik, lock):
    with lock:  # prosimy o dostęp do słownika utworzonego przez managera razem z tą blokadą
        slownik['klucz1'] += 1
        slownik[20] = 'zmieniona_wartosc2'

class WlasnaKlasa:
    """Od razu tworząc klasę zakładamy, że będzie ona służyć do równoległej pracy między procesami i zawierać w sobie
    elementy ze wspólnej pamięci."""
    def __init__(self, wartosc, manager):
        self.wartosc = manager.Value('i', wartosc)
        self.lock = manager.Lock()

    def zmien_wartosc(self, nowa_wartosc):
        with self.lock:
            self.wartosc.value = nowa_wartosc

def modyfikuj_klase(obiekt: WlasnaKlasa):
    obiekt.zmien_wartosc(100)

def main():
    """Wykonujemy testy, jak procesy radzą sobie z modyfikowaniem zmiennych globalnych oraz tych we wspólnej pamięci"""
    # test nr 1 - dla zwykłej listy
    proces = Process(target=modyfikuj_zwykla_liste)
    proces.start()
    proces.join()
    print(zwykla_lista)

    # test nr 2 - dla list we wspólnej pamięci
    proces = Process(target=modyfikuj_sprytna_liste, args=(sprytna_lista, sprytna_lista_z_blokada))
    proces.start()
    proces.join()

    print(zwykla_lista)
    print(sprytna_lista[:])
    print(sprytna_lista_z_blokada[:])

    # test nr 3 - tworzenie i modyfikowanie słownika we wspólnej pamięci
    with Manager() as manager:
        lock = Lock()
        slownik = manager.dict(
            {'klucz1': 10, 20: 'wartosc2'}
        )

        proces = Process(target=modyfikuj_slownik, args=(slownik, lock))
        proces.start()
        proces.join()

        print(dict(slownik))

    # test nr 4 - praca z własną klasą wewnątrz procesu
    with Manager() as manager:
        obiekt = WlasnaKlasa(34, manager)

        proces = Process(target=modyfikuj_klase, args=(obiekt,))
        proces.start()
        proces.join()

        print(f"Końcowa wartość pola w naszej klasie to {obiekt.wartosc.value}")

if __name__ == '__main__':
    main()