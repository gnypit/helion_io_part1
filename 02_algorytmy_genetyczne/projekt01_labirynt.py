"""Skrypt przygotowany w ramach kursu z inteligencji obliczeniowej dla wydawnictwa Helios
Jakub T. Gnyp, gnyp.jakub@gmail.com
Projekt nr 1: Labirynt
"""
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import pygad
import tqdm
import copy

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
num_generations = 4000
sol_per_pop = 500
num_parents_mating = 250
num_genes = 30
selection = "tournament"
mutation = "random"
mutation_prob = 0.15
k_tournament = 10
stop_criteria = "reach_1"

"""Wagi punktów nagród & kar:"""
bonus_point = 2  # do nagród
pos_repeat_point = 1  # do kary za powtórzenie pozycji
hitting_a_wall_point = 1.25  # do kary za zmarnowanie ruchu na odbicie się od ściany

"""Rozwiązywanie labiryntu jest problemem NP-trudnym, tak jak problem plecakowym (złodzieja) oraz komiwojażera"""
def fitness_fun(genetic_algorithm_instance, route, route_idx):
    """Używamy metryki Taxi do ewaluacji tras przez labirynt"""
    position = {'y': 1, 'x': 1}  # zaczynamy w (1,1)

    for move in route:  # zmieniamy położenie w zależności od wykonanego ruchu
        new_y, new_x = position.get('y') + moves_mapping.get(move)[0], position.get('x') + moves_mapping.get(move)[1]

        if 0 <= new_y <= 11 and 0 <= new_x <= 11:
            """Po zweryfikowaniu, że nowe współrzędne są wewnątrz labiryntu (tzn. mieszczą się w macierzy),
            sprawdzamy, czy reprezentują dozwolone pole:
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


def fitness_fun_new(genetic_algorithm_instance, route, route_idx):
    """Używamy metryki Taxi do ewaluacji tras przez labirynt. Dodatkowo, przydzielamy kary i nagrody za poszczególne
    zachowania, aby trasy proponowane przez chromosomy były jak najbliższe tym faktycznym, po uwzględnieniu
    "odbijania się" od ścian.
    """
    position = {'y': 1, 'x': 1}  # zaczynamy w (1,1)

    """Aby uniknąć kłopotu z cechą 'mutable' słowników, zapamiętujemy w liście historii położeń kopię
    początkowego stanu słownika położeń, zamiast przypisywać do listy dynamiczną strukturę danych.
    """
    history = [copy.deepcopy(position)]
    is_probem = 0  # początkowa wartość licznika problemów, do którego przydzielamy punkty kar
    bonus = 0  # początkowa wartość bonusu, do której dodajemy punkty nagród

    for move in route:  # zmieniamy położenie w zależności od wykonanego ruchu

        if position.get('x') == exit_labyrinth.get('x') and position.get('y') == exit_labyrinth.get('y') and move == 0:
            bonus += bonus_point  # bonus za pozostanie w mecie
            continue

        new_y, new_x = position.get('y') + moves_mapping.get(move)[0], position.get('x') + moves_mapping.get(move)[1]

        if 0 <= new_y <= 11 and 0 <= new_x <= 11:
            """Po zweryfikowaniu, że nowe współrzędne są wewnątrz labiryntu (tzn. mieszczą się w macierzy),
            sprawdzamy, czy reprezentują dozwolone pole:
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


def example():
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
    """Główna funkcja wykonująca, aplikująca algorytm genetyczny do labiryntu zgodnie z ustawieniami w zmiennych
    globalnych oraz z wykorzystaniem zdefiniowanych w skrypcie `projekt01_labirynt_wizualizacje.py` funkcji
    do wizualizacji.
    """
    fitness_list = []
    times = []
    output_list = []
    generations_no = []  # nr generacji w danej iteracji, w której osiągnięto najlepsze rozwiązanie

    for i in tqdm.tqdm(range(10)):
        start = time()  # sprawdzamy czas na starcie

        ga_instance = pygad.GA(
            gene_space=gene_space,
            num_genes=num_genes,
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=fitness_fun,
            sol_per_pop=sol_per_pop,
            parent_selection_type=selection,
            mutation_type=mutation,
            mutation_probability=mutation_prob,
            stop_criteria=stop_criteria,
            suppress_warnings=True,
            K_tournament=k_tournament
        )

        ga_instance.run()  # uruchamiamy algorytm genetyczny
        end = time()  # mierzymy czas na koniec
        times.append(end - start)

        """Ręcznie wizualizujemy historię fitnessu na przestrzeni generacji."""
        fig, ax = plt.subplots()  # tworzymy osobną figurę na wykresy historii fitnessu!
        fitness = ga_instance.best_solutions_fitness  # wartości na oś 0y
        generations = list(range(len(fitness)))  # wartości na oś 0x

        ax.plot(generations, fitness, color="lime", linewidth=2, drawstyle='steps-post', label='Fitness')

        ax.set_xlabel("Generations")
        ax.set_ylabel("Fitness")
        ax.set_title("PyGAD - Generations vs. Fitness")
        ax.legend()  # żeby mieć pewność, że legenda się wyświetli
        ax.grid(True)
        plt.show()

        """Zapamiętujemy parametry rozwiązania:"""
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        generations_no.append(ga_instance.best_solution_generation)
        fitness_list.append(solution_fitness)
        output_list.append(solution)

        """Wizualizujemy wyniki (trasy, które chromosomy chciały przejść)"""
        gif_filename = 'chromosome_animation' + str(i) + '.gif'
        picture_filename = 'chromosome_picture' + str(i) + '.png'
        see_route(labyrinth=labyrinth, moves_mapping=moves_mapping, steps=output_list[-1],
                  gif_filename=gif_filename, summary_filename=picture_filename)

        """Wizualizujemy faktyczną trasę, z pominięciem kroków polegających na wejściu na pole niedozwolone"""
        x, y = 1, 1
        history = []

        for step in output_list[-1]:
            new_y, new_x = y + moves_mapping.get(step)[0], x + moves_mapping.get(step)[1]
            if 0 <= new_y <= 11 and 0 <= new_x <= 11:
                """Po zweryfikowaniu, że nowe współrzędne są wewnątrz labiryntu (tzn. mieszczą się w macierzy),
                sprawdzamy, czy reprezentują dozwolone pole:
                """
                if labyrinth[new_y, new_x] == 0:
                    x, y = new_x, new_y
                    history.append(step)
                else:
                    history.append(0)
            else:
                print(f"Dostaliśmy współrzędne x={new_x} oraz y={new_y} poza labiryntem (przy wizualizacji).")

        gif_filename = 'actual_route_animation' + str(i) + '.gif'
        picture_filename = 'actual_route_picture' + str(i) + '.png'
        see_route(labyrinth=labyrinth, moves_mapping=moves_mapping, steps=history,
                  gif_filename=gif_filename, summary_filename=picture_filename)

    print(f"Średni czas działania algorytmu genetycznego: {np.mean(times)}")
    print(f"Średnia wartość f. fitnessu najlepszego rozwiązania: {np.mean(fitness_list)}")
    print(f"Średnia liczba generacji do otrzymania najlepszego rozwiązania: {np.mean(generations_no)}")

    print(f"Historia wyników: \n")
    for j in range(len(output_list)):
        print(output_list[j])


if __name__ == "__main__":
    main()
