"""Skrypt przygotowany w ramach kursu z inteligencji obliczeniowej dla wydawnictwa Helios
Jakub T. Gnyp, gnyp.jakub@gmail.com
Projekt nr 1: Labirynt — funkcje do wizualizacji
Wymagany program: ImageMagick https://www.techspot.com/downloads/5515-imagemagick.html
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np


def draw_labyrinth(plot_object, labyrinth: np.ndarray):
    """Funkcja rysująca pusty labirynt (bez trasy) zgodnie z macierzą 'labyrinth', na podanym obiekcie
    graficznym 'plot_object'.
    """
    for i in range(len(labyrinth)):
        """Iteracja po kolejnych wierszach"""
        for j in range(len(labyrinth[i])):
            """Iteracja po kolejnych kolumnach"""
            if labyrinth[i, j] == 1:
                """Rysowanie ściany"""
                rect = patches.Rectangle(
                    (j, i), 1, 1, linewidth=1, edgecolor='black', facecolor='black'
                )
            else:
                """Rysowanie pustego pola"""
                rect = patches.Rectangle(
                    (j, i), 1, 1, linewidth=1, edgecolor='grey', facecolor='white'
                )
            plot_object.add_patch(rect)

    """Końcowe ustawienia"""
    plot_object.set_xlim(0, 12)
    plot_object.set_ylim(0, 12)
    plot_object.invert_yaxis()
    plot_object.set_aspect('equal')


def see_route(labyrinth: np.ndarray, moves_mapping: dict, steps: list,
              gif_filename='labirynt.gif', summary_filename='labirynt_summary.png'):
    """Funkcja przyjmująca na wejściu macierz reprezentującą labirynt (labyrinth), słownik dopasowujący kod ruchu
    do zmiany odpowiednich współrzędnych — w macierzy z biblioteki numpy najpierw jest wsp. wiersza, a następnie wsp.
    kolumny!

    Wynikiem funkcji jest animacja GIF danej trasy przez labirynt oraz grafika PNG z podsumowaniem całej trasy.
    """
    start_pos = (1, 1)
    fig, ax = plt.subplots()

    """Rysowanie pustego labiryntu"""
    draw_labyrinth(plot_object=ax, labyrinth=labyrinth)

    """Tworzenie trasy na podstawie kroków"""
    path_x, path_y = [start_pos[1] + 0.5], [start_pos[0] + 0.5]  # ścieżka zaczyna się w środku pola wejścia, stąd 0.5
    pos = list(start_pos)
    for step in steps:
        move = moves_mapping[step]
        pos[0] += move[0]
        pos[1] += move[1]
        path_x.append(pos[1] + 0.5)  # przesunięcie o 0.5, żeby linie były "wycentrowane", a nie wzdłuż krawędzi pól
        path_y.append(pos[0] + 0.5)  # przesunięcie o 0.5, żeby linie były "wycentrowane", a nie wzdłuż krawędzi pól

    def update(num, path_x, path_y, line):  # wewnątrz funkcji można tworzyć "lokalną" funkcję
        """Funkcja do aktualizacji animacji"""
        line.set_data(path_x[:num], path_y[:num])
        return line,

    """Inicjalizacja linii trasy"""
    line, = ax.plot([], [], lw=2, color='red')

    """Animacja trasy wzdłuż odpowiednich współrzędnych z zadanym interwałem, określającym jak szybko zmieniają się
    klatki w końcowym GIFie."""
    ani = animation.FuncAnimation(fig, update, frames=len(path_x), fargs=[path_x, path_y, line], interval=200,
                                  blit=True)

    """Ustawienia osi"""
    plt.xlim(0, 12)
    plt.ylim(0, 12)
    plt.gca().invert_yaxis()

    """Zapisanie animacji jako GIF"""
    ani.save(gif_filename, writer='imagemagick')
    print(f"Wygenerowano animację trasy przez labirynt")

    """Rysowanie całej trasy na grafice PNG"""
    fig, ax = plt.subplots()  # wykorzystuję ponownie zmienne lokalne
    draw_labyrinth(plot_object=ax, labyrinth=labyrinth)  # rysujemy pusty labirynt od nowa
    ax.plot(path_x, path_y, lw=2, color='red')  # dodajemy całą wygenerowaną trasę

    """Ustawienia osi"""
    plt.xlim(0, 12)
    plt.ylim(0, 12)
    plt.gca().invert_yaxis()

    """Zapisanie obrazu jako PNG"""
    plt.savefig(summary_filename)
    plt.close()
    print(f"Wykonano grafikę z całą trasą przez labirynt")
