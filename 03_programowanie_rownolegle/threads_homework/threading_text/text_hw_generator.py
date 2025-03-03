import os
import random
import string


"""Aby móc powielić wyniki z zachowaniem pseudolosowości, ustawia się tzw. ziarno:"""
random.seed(6122024)  # 6 grudnia 2024 r.


def generate_text_files(base_dir="text_data", num_files=100):
    """Generuje pliki tekstowe w folderze `base_dir`."""
    os.makedirs(base_dir, exist_ok=True)
    for _ in range(num_files):
        # Losowa nazwa pliku
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".txt"
        file_path = os.path.join(base_dir, file_name)

        # Zapisujemy tekst do pliku; dodajemy 'losową' liczbę wierszy tekstu
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
                "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
                "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                "sunt in culpa qui officia deserunt mollit anim id est laborum.\n" * random.randint(80000, 90000)
            )

    print(f"Generated {num_files} text files in {base_dir}")


if __name__ == '__main__':
    generate_text_files()
