"""Skrypt przygotowany w ramach kursu z inteligencji obliczeniowej dla wydawnictwa Helios
Jakub T. Gnyp, gnyp.jakub@gmail.com
Projekt nr 1: Labirynt
"""
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import pygad
import tqdm

from time import time
from projekt01_labirynt_wizualizacje import see_route

"""Labirynt zakodowano za pomocą macierzy o elementach 0 i 1. Zero oznacza pole dozwolone, po którym można się poruszać, 
natomiast pole czarne oznacza ścianę; na te pola nie wolno wchodzić. Włącznie ze ścianami na granicy labiryntu, ma on 
wymiary 12x12, zatem współrzędne w Python będą numerowane od 0 do 11. Wejście znajduje się na polu (1,1), natomiast
wyjście na polu (10,10).
"""

labyrinth = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ])

"""Ruchy przez labirynt zakodowano w następujący sposób:
0 - bez ruchu;
1 - w lewo;
2 - w prawo;
3 - w górę;
4 - w dół.

Dodatkowo, stworzono słownik mapujący to kodowanie do zmian odpowiednich współrzędnych.
"""
gene_space = [0, 1, 2, 3, 4]
moves_mapping = {
    0: (0, 0),    # bez ruchu
    1: (0, -1),   # w lewo
    2: (0, 1),    # w prawo
    3: (-1, 0),   # w górę
    4: (1, 0)     # w dół
}


def main():
    # Przykład użycia funkcji do wizualizacji trasy
    steps = [2, 2, 4, 4, 4, 1, 4, 2, 2, 1, 4, 4, 1, 1, 1, 4, 2, 2, 4, 2, 4, 2]
    see_route(steps=steps, labyrinth=labyrinth, moves_mapping=moves_mapping)
    print("Plik wygenerowany poprawnie")


if __name__ == "__main__":
    main()