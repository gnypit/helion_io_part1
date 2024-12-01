import math
import numpy as np
import pygad
from cProfile import Profile


def endurance(x, y, z, u, v, w):
    """Funkcja do zoptymalizowania, podana przez eksperta z (danej) dziedziny"""
    return math.exp(-2 * (y - math.sin(x)) ** 2) + math.sin(z * u) + math.cos(v * w)


def fitness_function(genetic_algorithm_instance, chromosome, chromosome_idx):
    x = chromosome[0]
    y = chromosome[1]
    z = chromosome[2]
    u = chromosome[3]
    v = chromosome[4]
    w = chromosome[5]

    fitness_value = endurance(x=x, y=y, z=z, u=u, w=w, v=v)

    return fitness_value


if __name__ == '__main__':
    profiler = Profile()
    profiler.enable()  # Rozpoczęcie profilowania

    ga_instance = pygad.GA(
        gene_space=np.linspace(start=0, stop=1, num=100000),
        num_generations=70,
        num_parents_mating=9,
        fitness_func=fitness_function,
        sol_per_pop=18,
        num_genes=6,
        parent_selection_type='tournament',
        mutation_type='random',
        mutation_probability=float(1 / 6),
        stop_criteria=['reach_2.83', 'saturate_15']
    )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    generations_number = ga_instance.best_solution_generation

    print(f"Ilości metali do użycia w stopie (parametry rozwiązania): {solution}")
    print(f"Wytrzymałość stopu (wart. funkcji 'endurance'): {solution_fitness}")
    print(f"Nr generacji/pokolenia najlepszego rozwiązania: {generations_number}")

    ga_instance.plot_fitness()

    profiler.disable()  # Zakończenie procesu profilowania
    profiler.print_stats(sort="time")
