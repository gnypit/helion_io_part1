import os


def generate_test_files(base_dir="text_data", num_dirs=5, num_files_per_dir=100):
    """Generuje strukturę folderów z plikami tekstowymi."""
    os.makedirs(base_dir, exist_ok=True)

    for dir_idx in range(1, num_dirs + 1):
        sub_dir = os.path.join(base_dir, f"subdir_{dir_idx}")
        os.makedirs(sub_dir, exist_ok=True)

        for file_idx in range(1, num_files_per_dir + 1):
            file_name = f"file_{file_idx}.txt"
            file_path = os.path.join(sub_dir, file_name)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(
                    ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                     "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris"
                     "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
                     "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
                     "proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n") * 100
                )

    print(f"Generated {num_dirs} directories with {num_files_per_dir} files each in {base_dir}")


if __name__ == '__main__':
    generate_test_files()
