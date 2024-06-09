class SuperCalculator:
    """This class can handle any number of inputs"""
    # result: float = None

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