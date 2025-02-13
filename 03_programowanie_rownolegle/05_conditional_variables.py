"""Inspirowany StingySpendy by James Cutajar. Dążymy do pokazania, dlaczego należy synchronizować pracę wątków."""
from time import sleep
from threading import Thread, Lock, Condition
from tqdm import tqdm
from random import uniform


class Konto:
    """Staram się jak najbardziej 'zepsuć' tę klasę, żeby zaprezentować race condition"""
    def __init__(self):
        self.hajsik = 100

    def wplac(self):
        for _ in range(10000):  # wykonujemy stosunkowo dużo operacji
            self.hajsik += 10
            sleep(uniform(0.00001, 0.0001))  # losowa przerwa po wpłaceniu, ale nie za duża

    def wydaj(self):
        for _ in range(10000):  # tyle samo operacji, co przy wpłacaniu
            self.hajsik -= 10  # odejmujemy tę samą kwotę, co dodajemy przy wpłacaniu

            if self.hajsik < 0:
                print(f"Wykryto race coindition - bilans ujemny: {self.hajsik}")

            sleep(uniform(0.00001, 0.0001))  # losowa przerwa po wydaniu, ale nie za duża


class KontoBlokada(Konto):
    blokada = Lock()

    def wplac(self):
        for _ in range(100000):  # wykonujemy operacje więcej razy niż bez blokady!
            self.blokada.acquire()
            self.hajsik += 10
            self.blokada.release()
        print(f"Wpłaty wykonane.")

    def wydaj(self):
        for _ in range(100000):  # wykonujemy tyle samo razy, co wpłaty
            self.blokada.acquire()
            self.hajsik -= 10
            self.blokada.release()
        print(f"Pieniądze wydane.")


class KontoWarunek(Konto):
    warunek = Condition()

    def wplac(self):
        for _ in range(100000):  # wykonujemy operacje więcej razy niż bez blokady!
            self.warunek.acquire()
            self.hajsik += 10
            self.warunek.notify()  # być może stan konta pozwoli na wydawanie pieniędzy
            self.warunek.release()
        print(f"Wpłaty wykonane.")

    def wydaj(self):
        for _ in range(50000):  # wykonujemy tyle samo razy, co wpłaty
            self.warunek.acquire()
            while self.hajsik < 20:
                self.warunek.wait()  # można podać konkretny czas oczekiwania w nawiasie
            self.hajsik -= 20  # tym razem naraz wydajemy więcej, niż naraz wpłacamy!

            if self.hajsik < 0:
                print(f"Warunek nie działa! Bilans wynosi {self.hajsik}")

            self.warunek.release()
        print(f"Pieniądze wydane.")


def main():
    race_condition_detected = False

    for _ in tqdm(range(1000)):  # powtarzamy eksperyment 1000 razy
        konto = Konto()
        threads = []

        for _ in range(6):  # uruchomienie względnie dużej liczby wątków
            thread_wplacajacy = Thread(target=konto.wplac, args=())
            threads.append(thread_wplacajacy)
            thread_wplacajacy.start()

            thread_wydajacy = Thread(target=konto.wydaj(), args=())
            threads.append(thread_wydajacy)
            thread_wydajacy.start()

        """Czekamy na zakończenie pracy przez wątki i zbieramy je:"""
        for t in threads:
            t.join()

        if konto.hajsik != 100:
            print(f"Wykryto race condition - końcowy bilans wynosi {konto.hajsik}")
            race_condition_detected = True

    if not race_condition_detected:
        print(f"Nie wykryto race condition.")


def main_blokada():
    race_condition_detected = False

    for _ in tqdm(range(1000)):  # powtarzamy eksperyment 1000 razy
        konto_z_blokada = KontoBlokada()
        threads = []

        for _ in range(6):  # uruchomienie względnie dużej liczby wątków
            thread_wplacajacy = Thread(target=konto_z_blokada.wplac, args=())
            threads.append(thread_wplacajacy)
            thread_wplacajacy.start()

            thread_wydajacy = Thread(target=konto_z_blokada.wydaj(), args=())
            threads.append(thread_wydajacy)
            thread_wydajacy.start()

        """Czekamy na zakończenie pracy przez wątki i zbieramy je:"""
        for t in threads:
            t.join()

        if konto_z_blokada.hajsik != 100:
            print(f"Wykryto race condition - końcowy bilans wynosi {konto_z_blokada.hajsik}")
            race_condition_detected = True

    if not race_condition_detected:
        print(f"Nie wykryto race condition.")


if __name__ == '__main__':
    race_condition_detected = False

    for _ in tqdm(range(1000)):  # powtarzamy eksperyment 1000 razy
        konto_z_warunkiem = KontoWarunek()
        threads = []

        for _ in range(6):  # uruchomienie względnie dużej liczby wątków
            thread_wplacajacy = Thread(target=konto_z_warunkiem.wplac, args=())
            threads.append(thread_wplacajacy)
            thread_wplacajacy.start()

            thread_wydajacy = Thread(target=konto_z_warunkiem.wydaj, args=())
            threads.append(thread_wydajacy)
            thread_wydajacy.start()

        """Czekamy na zakończenie pracy przez wątki i zbieramy je:"""
        for t in threads:
            t.join()

        if konto_z_warunkiem.hajsik != 100:
            print(f"Wykryto race condition - końcowy bilans wynosi {konto_z_warunkiem.hajsik}")
            race_condition_detected = True

    if not race_condition_detected:
        print(f"Nie wykryto race condition.")