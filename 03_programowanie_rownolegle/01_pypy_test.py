from time import time


def creat_numbers(base_number):
    a = base_number
    b = base_number + 1
    return a, b


def multiply(number1, number2):
    return number1 * number2


def main():
    time_start = time()

    for _ in range(10000):
        results = []
        for i in range(10000):
            x, y = creat_numbers(i)
            z = multiply(x, y)
            results.append(z)

    time_end = time()

    print(f"Time it took to perform the loops: {time_end - time_start}")


if __name__ == '__main__':
    main()
