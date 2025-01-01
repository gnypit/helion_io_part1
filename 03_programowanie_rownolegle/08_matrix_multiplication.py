"""Skrypt inspirowany przykładem aut. Jamesa Cutajara"""
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

def fill_in_matrix(matrix, size):
    for row in range(size):
        for col in range(size):
            matrix[row * size + col] = randint(-5, 5)

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

def compute_row(id, m1, m2, result, size, no_processes):
    """Ta funkcja oblicza wartości co któregoś wiersza macierzy docelowej, będącej wynikiem mnożenia m1 i m2.
    Jeśli jest 10 procesów i macierze 200x200, a id przekazane do tej funkcji wynosi np. 7, to ta funkcja obliczy
    kolejno wiersze: 7, 17, 27, 37, itd. (naraz jeden!).

    W tym celu pobierany będzie za każdym razem wiersz z macierzy m1 o tym samym numerze, co obliczany wiersz w macierzy
    docelowej, a kolejne elementy będą liczone po wymnożeniu go odpowiednio i każdorazowo z kolejnymi kolumnami macierzy
    m2."""
    rows_to_compute = range(id, size, no_processes)

    """Po zidentyfikowaniu wierszy do obliczenia (każdy proces ma inne!) pętle przebiegają analogicznie, co w funkcji
    matrix_as_list_multiplication()"""
    for row in rows_to_compute:
        for col in range(size):
            for i in range(size):
                """Przerabiamy numer wiersza i numer kolumny na pojedynczy indeks"""
                result[row * size + col] += m1[row * size + i] * m2[i * size + col]


def test(m1, m2, size=3, print_result=True):
    numpy_time_start = time()
    result1 = dot(m1, m2)
    numpy_time_end = time()
    time1 = round(numpy_time_end - numpy_time_start, 3)

    result2, time2 = matrix_multiplication(m1, m2, size=size)
    result3, time3 = matrix_as_list_multiplication(m1, m2, size=size)

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
    test(m1=matrix_big_a, m2=matrix_big_b, size=10)  # test(m1=matrix_a, m2=matrix_b)

    """Inicjujemy obiekty na macierze we wspólnej pamięci"""
    big_a = [matrix_big_a[i][j] for i, j in [[_i, _j] for _i in range(10) for _j in range(10)]]
    big_b = [matrix_big_b[i][j] for i, j in [[_i, _j] for _i in range(10) for _j in range(10)]]

    matrix1_array = Array('i', big_a, lock=False)  # blokada niepotrzebna, procesy tylko odczytują stąd wartości
    matrix2_array = Array('i', big_b, lock=False)  # blokada niepotrzebna, procesy tylko odczytują stąd wartości
    result_array = Array('i', [0] * 100, lock=False)  # blokada niepotrzebna, bo każdy proces oblicza inne wiersze

    """Tworzymy i inicjujemy procesy; rozpoczynamy pomiar czasu. Potrzebujemy używać procesów ręcznie!
    ProcessPoolExecutor w bibliotece concurrent oraz Pool w multiprocessing pracują na niezależnych zadaniach, bez
    współdzielonej pamięci. Pamięć możemy współdzielić na zasadzie dziedziczenia, ręcznie tworząc procesy-dzieci
    u procesu-rodzica."""
    process_count = 5
    processes = []
    process_time_start = time()
    for proc_id in range(process_count):
        p = Process(target=compute_row, args=(
            proc_id, matrix1_array, matrix2_array, result_array, 10, process_count
        ))
        processes.append(p)
        p.start()

    """Zbieramy procesy-dzieci. Gdyby czekały na barierze, jak to raz pokazaliśmy z wątkami, możliwe, że do bariery
    trzeba by było dołączyć główny proces, aby faktycznie móc zakończyć pracę programu!"""
    for p in processes:
        p.join()

    print(f"Procesy pracowały {time() - process_time_start:.2f}s")
    print(result_array[:])

    """Teraz naprawdę duże macierze"""
    matrix_size = 200
    matrix1_array = Array('i', [0] * (matrix_size ** 2), lock=False)
    matrix2_array = Array('i', [0] * (matrix_size ** 2), lock=False)
    result_array = Array('i', [0] * (matrix_size ** 2), lock=False)

    fill_in_matrix(matrix=matrix1_array, size=matrix_size)
    fill_in_matrix(matrix=matrix2_array, size=matrix_size)

    """Mamy macierze gotowe jako listy, więc:"""
    process_count = cpu_count()
    processes = []
    process_time_start = time()
    for proc_id in range(process_count):
        p = Process(target=compute_row, args=(
            proc_id, matrix1_array, matrix2_array, result_array, matrix_size, process_count
        ))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    process_time_end = time()

    result_array = Array('i', [0] * (matrix_size ** 2), lock=False)
    sequential_time_start = time()
    for row in range(matrix_size):
        for col in range(matrix_size):
            for i in range(matrix_size):
                result_array[row * matrix_size + col] += matrix1_array[row * matrix_size + i] * matrix2_array[
                    i * matrix_size + col
                ]
    sequential_time_end = time()

    print(f"Procesy pracowały {process_time_end - process_time_start} sekund\n"
          f"Kod sekwencyjny pracował {sequential_time_end - sequential_time_start} sekund")

