import os
from time import time


def read_files_sequentially(base_dir="text_data", output_file="reports/report_sequential.txt"):
    """Czyta pliki tekstowe z folderu i zapisuje ich zawartość do raportu."""
    report = ""
    for file_name in os.listdir(base_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(base_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    report += f"\n=== File: {file_name} ===\n"
                    report += f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {output_file}")


if __name__ == '__main__':
    start = time()
    read_files_sequentially()
    end = time()
    print(f"Sequential code run for {end - start} seconds.")
