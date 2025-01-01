from multiprocessing import Process, Array, cpu_count
from time import time
from random import randint
from numpy import dot

"""Do testów, czy kod działa poprawnie, tworzymy dwie macierze jako stałe:"""
matrix_a = [
    [3, 1, -4],
    [2, -3, 1],
    [5, -2, 0]
]

matrix_b = [
    [1, -2, -1],
    [0, 5, 4],
    [-1, -2, 3]
]

"""Jeszcze jeden przykład, ale z macierzami 10x10:"""
matrix_big_a = [
    [-1, -3,  3, -5,  2,  4,  1,  2, -4, -4],
    [-5, -3,  1, -1,  0,  5,  2, -1, -4, -2],
    [ 0, -2, -5, -3, -2, -4,  5,  0, -4, -5],
    [-4,  2,  1,  1,  3, -4,  0,  2,  2,  0],
    [ 1, -3, -5,  4, -4,  2, -3, -5,  4, -1],
    [-4,  2,  0, -3, -5, -2,  2,  3, -2, -5],
    [ 3,  5,  2, -5,  5, -5,  3, -5, -3, -2],
    [ 3,  3, -3, -2, -2, -4,  2, -1,  0, -2],
    [-4, -5, -5,  4, -3, -4,  5,  3, -3,  3],
    [-4, -3, -5, -3, -4,  5, -4,  0, -2,  0]
]
matrix_big_b = [
    [ 5,  2,  1, -2, -5, -1,  2, -1,  0,  2],
    [ 4,  4,  4, -3,  1, -2, -2,  4, -3, -4],
    [ 1,  5,  1,  1, -1,  0,  4, -1,  0, -4],
    [-1,  2, -5,  5, -4,  2, -4, -5,  1,  5],
    [-1,  2,  1, -4, -4,  3, -5, -1,  5, -4],
    [ 3,  1, -3,  4, -2,  0, -2, -3,  0, -4],
    [-1, -4,  2, -1, -1, -4, -3,  5, -2,  2],
    [ 0,  2,  0,  0,  5,  2,  0, -2,  3,  2],
    [ 3, -5,  5,  2,  2,  0,  2,  0, -4, -4],
    [-1, -1,  0,  0,  4, -3,  3,  5, -2,  3]
]

def matrix_multiplication(matrix1, matrix2, size = 3):
    """Funkcja przyjmuje macierze jako tablice 2D i mnoży je ze sobą zagnieżdżonymi pętlami."""
    result = [[0] * size for _ in range(size)]
    time_start = time()
    for row in range(size):
        for col in range(size):
            for i in range(size):
                result[row][col] += matrix1[row][i] * matrix2[i][col]
    time_end = time()
    t = time_end - time_start

    return result, t

def matrix_as_list_multiplication(matrix1, matrix2, size=3):
    """Funkcja przerabia macierze z tablic 2D na tablice 1D i w tej postaci je mnoży."""
    m1 = [matrix1[i][j] for i, j in [[_i, _j] for _i in range(size) for _j in range(size)]]
    m2 = [matrix2[i][j] for i, j in [[_i, _j] for _i in range(size) for _j in range(size)]]
    result = [0] * (size ** 2)  # zakładamy, że nasze wszystkie macierze są kwadratowe

    time_start = time()
    for row in range(size):
        for col in range(size):
            for i in range(size):
                """Przerabiamy numer wiersza i numer kolumny na pojedynczy indeks"""
                result[row * size + col] += m1[row * size + i] * m2[i * size + col]
    end_time = time()
    t = end_time - time_start

    result_2d = [[0] * size for _ in range(size)]
    for index in range(len(result)):
        """Przerabiamy pojedynczy indeks na dwie współrzędne: nr wiersza i kolumny."""
        row = index // size  # tylko część całkowita tego dzielenia
        col = index % size  # tylko reszta z tego dzielenia
        result_2d[row][col] = result[index]

    return result_2d, t

def test(m1, m2, size=3, print_result=True):
    numpy_time_start = time()
    result1 = dot(m1, m2)
    numpy_time_end = time()
    time1 = round(numpy_time_end - numpy_time_start, 3)

    result2, time2 = matrix_multiplication(m1, m2)
    result3, time3 = matrix_as_list_multiplication(m1, m2)

    time2, time3 = round(time2, 3), round(time3, 3)

    if print_result:
        print(f"Numpy zwróciło {result1} w czasie {time1} sekund\n"
              f"Pierwsza funkcja zwróciła {result2} w czasie {time2} sekund\n"
              f"Druga funkcja zwróciła {result3} w czasie {time3} sekund")
    else:
        print(f"Numpy zwróciło wynik w czasie {time1} sekund\n"
              f"Pierwsza funkcja zwróciła wynik w czasie {time2} sekund\n"
              f"Druga funkcja zwróciła wynik w czasie {time3} sekund")

if __name__ == '__main__':
    test(m1=matrix_a, m2=matrix_b)