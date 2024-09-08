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


"""Globalne zmienne/ustawienia algorytmu genetycznego"""
num_generations = 2000
sol_per_pop = 800
num_parents_mating = 400
elite_size = 2
num_genes = 30

def fitness_fun_1(ga_instance, route, route_idx):
    """Pierwsza funkcja fitnessu z samą metryką taxi"""
    y, x = 1, 1

    for move in route:
        """Analizujemy kolejne ruchy (move -> gen, route -> chromosom)"""
        if move == 0:
            new_y, new_x = y, x
        elif move == 1:
            new_y, new_x = y, x - 1
        elif move == 2:
            new_y, new_x = y, x + 1
        elif move == 3:
            new_y, new_x = y - 1, x
        else:  # został już tylko możliwy ruch w dół
            new_y, new_x = y + 1, x

        y, x = new_y, new_x

    x_distance, y_distance = abs(11 - x), abs(11 - y)
    fitness_val = (22 - x_distance - y_distance) / 22
    return fitness_val


def fitness_fun_2(ga_instance, route, route_idx):
    """Druga funkcja fitnessu z:
     1) metryką taxi;
     2) brakiem przyzwolenia na wejście w ścianę;
     3) karą za zmarnowanie ruchu na odbicie się od ściany;
     4) zmianą klauzuli warunkowych if/elif/else na case-match
     """
    y, x = 1, 1  # współrzędne pola "wejście"
    is_problem = 0

    for move in route:
        """Analizujemy kolejne ruchy (move -> gen, route -> chromosom)"""
        match move:
            case 0:
                new_y, new_x = y, x
            case 1:
                new_y, new_x = y, x - 1
            case 2:
                new_y, new_x = y, x + 1
            case 3:
                new_y, new_x = y - 1, x
            case 4:
                new_y, new_x = y + 1, x

        """Wiemy, że wszystkie możliwe przypadki zostały już uwzględnione!"""
        if labyrinth[new_y, new_x] == 0:
            y, x = new_y, new_x
        else:
            is_problem += 1

    x_distance, y_distance = abs(11 - x), abs(11 - y)
    fitness_val = (22 - x_distance - y_distance) / 22 - is_problem/num_genes
    return fitness_val


def fitness_fun_3(ga_instance, route, route_idx):

    """Zaczynamy w (1,1)"""
    y, x = 1, 1  # współrzędne pola "wejście"
    is_problem = 0  # "licznik" problemów
    bonus = 0  # licznik bonusu za pozostanie w mecie/wyjściu
    zero_no = 0  # licznik "postojów" przed metą/wyjściem

    """Lista list, gdzie każdy element jest listą wsp. pola, 
    na którym znajdujemy się po wykonaniu nowego ruchu (zakodowanego w chromosomie)
    """
    history = [[x, y]]
    # TODO: rozróżnienie w wizualizacjach pomiędzy faktycznie wykonaną, tj. dozwoloną trasą, a tą, którą chciał wykonać chromosom


    for move in route:
        """Bonus za pozostanie w mecie:"""
        if history[-1] == [10, 10] and move == 0:
            bonus += 1  # maksymalnie 10
            continue

        """Analizujemy kolejne ruchy (move -> gen, route -> chromosom)"""
        match move:
            case 0:
                new_y, new_x = y, x
                zero_no += 1
            case 1:
                new_y, new_x = y, x - 1
            case 2:
                new_y, new_x = y, x + 1
            case 3:
                new_y, new_x = y - 1, x
            case 4:
                new_y, new_x = y + 1, x

        """Przydzielamy kary:"""
        if labyrinth[new_y, new_x] == 0:
            y, x = new_y, new_x
            history.append([x, y])

            """Sprawdzamy, czy powtarzamy położenie:"""
            if history.count([x, y]) > 1:
                is_problem += 1  # kara za powtórzenie pozycji
        else:
            is_problem += 1.25  # kara za zmarnowanie ruchu na odbicie się od ściany

    """Obliczenie odległości za pomocą metryki taxi i nowa, prosta formuła na wart. f. fit., ograniczona z góry:"""
    x_distance, y_distance = abs(11 - x), abs(11 - y)
    fit_val = (((22 - x_distance - y_distance) + bonus) * 2 - is_problem - zero_no) / 64

    return fit_val


def example_vis():
    # Przykład użycia funkcji do wizualizacji trasy
    steps = [2, 2, 4, 4, 4, 1, 4, 2, 2, 1, 4, 4, 1, 1, 1, 4, 2, 2, 4, 2, 4, 2]
    see_route(steps=steps, labyrinth=labyrinth, moves_mapping=moves_mapping)
    print("Pliki wygenerowane poprawnie.")

    # Stworzę jeszcze pusty labirynt do analizy
    fig, ax = plt.subplots()
    draw_labyrinth(plot_object=ax, labyrinth=labyrinth)
    plt.savefig("pusty_labirynt.png")
    print("Pusty labirynt utworzony.")


def main():
    """Główna funkcja wykonująca nasz program"""
    fitness_list = []
    times = []
    output_list = []
    generations_no = []

    for _ in tqdm.tqdm(range(10)):
        start = time()  # sprawdzamy bieżący czas

        ga_instance = pygad.GA(  # inicjujemy algorytm genetyczny
            gene_space=gene_space,
            num_genes=num_genes,
            num_generations=num_generations,
            fitness_func=fitness_fun_2,
            sol_per_pop=sol_per_pop,
            keep_parents=elite_size,
            parent_selection_type="tournament",
            mutation_type="random",
            mutation_probability=0.1,
            stop_criteria=["reach_1", "saturate_500"],
            suppress_warnings=False,
            num_parents_mating=num_parents_mating
        )

        ga_instance.run()  # uruchamiamy algorytm genetyczny
        end = time()  # znowu sprawdzamy bieżący czas
        times.append(end - start)  # liczymy, ile czasu upłynęło

        """Pobieramy i zapamiętujemy wyniki:"""
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        generations_no.append(ga_instance.best_solution_generation)
        fitness_list.append(solution_fitness)
        output_list.append(solution)

    """Wypisujemy wyniki:"""
    print(f"Średni czas działania algorytmu genetycznego: {np.mean(times)}")
    print(f"Średnia wartość funkcji fitnessu najlepszego rozwiązania: {np.mean(fitness_list)}")
    print(f"Średnia liczba generacji do najlepszego rozwiązania: {np.mean(generations_no)}")

    print("Historia wyników:")
    file_number = 0
    for output in output_list:
        gif_filename = "animation_route_no_" + str(file_number) + ".gif"
        png_filename = "summary_route_no_" + str(file_number) + ".png"
        see_route(steps=output, labyrinth=labyrinth, moves_mapping=moves_mapping, gif_filename=gif_filename,
                  summary_filename=png_filename)
        file_number += 1


if __name__ == "__main__":
    main()
