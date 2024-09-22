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
from projekt01_labirynt_wizualizacje import see_route, draw_labyrinth

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
moves_mapping = {ruch: (zmiana y, zmiana x), ...}
y jest pierwszą wsp. w macierzy, ponieważ to nr wiersza!
"""
gene_space = [0, 1, 2, 3, 4]
moves_mapping = {
    0: (0, 0),    # bez ruchu
    1: (0, -1),   # w lewo
    2: (0, 1),    # w prawo
    3: (-1, 0),   # w górę
    4: (1, 0)     # w dół
}


"""Ustawienia algorytmu genetycznego"""
exit_labyrinth = {'y': 10, 'x': 10}  # współrzędne "wyjścia" z labiryntu


"""Rozwiązywanie labiryntu jest problemem NP-trudnym, tak jak problem plecakowym (złodzieja) oraz komiwojażera"""
def fitness_fun(genetic_algorithm_instance, route, route_idx):
    """Używamy metryki Taxi do ewaluacji tras przez labirynt"""
    position = {'y': 1, 'x': 1}  # zaczynamy w (1,1)

    for move in route:  # zmieniamy położenie w zależności od wykonanego ruchu
        new_y, new_x = position.get('y') + moves_mapping.get(move)[0], position.get('x') + moves_mapping.get(move)[1]

        if 0 <= new_y <= 11 and 0 <= new_x <= 11:
            """Po zweryfikowaniu, że nowe współrzędne są wewnątrz labiryntu (tzn. mieszczą się w macierzy), analizujemy
            je dalej:
            """
            if labyrinth[new_y, new_x] == 0:
                position['x'], position['y'] = new_x, new_y
        else:
            print(f"Dostaliśmy współrzędne x={new_x} oraz y={new_y} poza labiryntem.")

    """Najpierw obliczamy pomocnicze zmienne, dla czytelności:"""
    x_distance = abs(exit_labyrinth.get('x') - position.get('x'))
    y_distance = abs(exit_labyrinth.get('y') - position.get('y'))
    sum_exit_coordinates = exit_labyrinth.get('x') + exit_labyrinth.get('y')

    """Faktyczna wartość fitnessu, maksymalnie 1:"""
    fitness_val = (sum_exit_coordinates - x_distance - y_distance) / sum_exit_coordinates

    return fitness_val


def main():
    """Główna funkcja wykonująca nasz program"""

    # Przykład użycia funkcji do wizualizacji trasy
    steps = [2, 2, 4, 4, 4, 1, 4, 2, 2, 1, 4, 4, 1, 1, 1, 4, 2, 2, 4, 2, 4, 2]
    see_route(steps=steps, labyrinth=labyrinth, moves_mapping=moves_mapping)
    print("Pliki wygenerowane poprawnie.")

    # Stworzę jeszcze pusty labirynt do analizy
    fig, ax = plt.subplots()
    draw_labyrinth(plot_object=ax, labyrinth=labyrinth)
    plt.savefig("pusty_labirynt.png")
    print("Pusty labirynt utworzony.")


if __name__ == "__main__":
    main()
