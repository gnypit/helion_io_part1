import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel


class SuperCalculator:
    """This class can handle any number of inputs"""
    result: float = None

    def __init__(self):
        print("This is a super calculator which can handle any number of inputs")

    def add(self, *args):
        """Method to add any number of inputs"""
        try:
            if not args and self.result is not None:
                """Nie podaliśmy nowych liczb, ale pamiętamy stary wynik"""
                return self.result  # koniec wykonywania metody
            elif not args:
                raise ValueError("At least one number is needed")  # koniec wykonywania metody

            """Został scenariusz, w którym faktycznie dostaliśmy liczby na wejściu"""
            total_sum = self.result if self.result is not None else 0
            for number in args:  # pętla "for"
                total_sum += float(number)
            self.result = total_sum  # nadpisujemy wynik
            return self.result  # koniec wykonywania metody
        except Exception as info:
            print(f"An exception occurred: {info}")

    def multiply(self, *args):
        """Method to multiply any number of inputs"""
        try:
            if not args and self.result is not None:
                """Nie podaliśmy nowych liczb, ale pamiętamy stary wynik"""
                return self.result  # koniec wykonywania metody
            elif not args:
                raise ValueError("At least one number is needed")  # koniec wykonywania metody

            """Został scenariusz, w którym faktycznie dostaliśmy liczby na wejściu"""
            total_product = self.result if self.result is not None else 1
            for number in args:  # pętla "for"
                total_product *= float(number)
            self.result = total_product  # nadpisujemy wynik
            return self.result  # koniec wykonywania metody
        except Exception as info:
            print(f"An exception occurred: {info}")

    def clear_memory(self):
        """Czyszczenie ostatniego wyniku z pamięci"""
        self.result = None
        print("Pamięć wyczyszczona")


class MainCalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = SuperCalculator()  # tworzymy instancję kalkulatora "wewnątrz" głównego okna aplikacji

        """Zadajemy geometrię:"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.setWindowTitle("Kalkulator")
        self.setGeometry(1000, 300, 400, 300)  # x, y, szerokość, wysokość

        """Dodajemy elementy głównego okienka"""
        self.input_line = QLineEdit("Podaj liczby")
        self.layout.addWidget(self.input_line)

        self.addition_button = QPushButton("Dodaj")
        self.layout.addWidget(self.addition_button)

        self.multiplication_button = QPushButton("Pomnóż")
        self.layout.addWidget(self.multiplication_button)

        self.result_display = QLabel()
        self.layout.addWidget(self.result_display)

        self.clear_memory_button = QPushButton("Wyczyść pamięć")
        self.layout.addWidget(self.clear_memory_button)

        """Łączymy elementy okna z kalkulatorem"""
        self.addition_button.clicked.connect(self.perform_addition)
        self.clear_memory_button.clicked.connect(self.perform_memory_clearing)

    def perform_addition(self):
        try:
            input_text = self.input_line.text()
            numbers = [float(num) for num in input_text.split(sep=",")]
            result = self.calculator.add(*numbers)
            self.result_display.setText(f"Wynik: {result}")
        except Exception as info:
            self.result_display.setText(f"Zadział się problem - info: {info}")

    # TODO: stworzyć funkcję `perform_multiplication` & podłączyć odpowiednio do aplikacji

    def perform_memory_clearing(self):
        self.calculator.clear_memory()
        self.result_display.setText("Pamięć wyczyszczona")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainCalculatorWindow()
    main_window.show()
    sys.exit(app.exec())
