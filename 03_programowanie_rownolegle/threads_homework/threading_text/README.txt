Szanowni Państwo!

W tym folderze znajduje się generator danych tekstowych. Przy obecnych ustawieniach, powinien stworzyć 100 plików o
łącznym rozmiarze ok. 3,5 GB. Załóżmy, że chcemy te dane wczytać i wypisać do jednego, wspólnego pliku, raportu.
Przy tej ilości wciąż nie powinno być przyspieszenia w czasie pracy kodu sekwencyjnego Vs równoległego - wymagałoby
to znacznie większego wolumenu danych. Dlatego w kursie skupiliśmy się na API, tzn. wykorzystywaliśmy opóźnienia
w pobieraniu danych z Internetu, aby w tym samym czasie kod wykonywał zadania.

Niemniej, zależy mi na pokazywaniu zarówno zalet, jak i wad pewnych rozwiązań. W związku z tym zachęcam
do eksperymentowania z wolumenem danych i samymi kodami (sekwencyjnym oraz z wykorzystaniem 'threading'), aby porównać
czasy działania i jednocześnie przećwiczyć pisanie kodu równoległego na dodatkowym przykładzie.

W szczególności ciekawym może być sprawdzenie, czy kod równoległy działa szybciej dla wielu małych plików,
czy mniejszej liczby, ale większych? Czy jest pewien sumaryczny rozmiar danych, przy którym kod równoległy zacznie
działać w tym samym czasie, co sekwencyjny? Może w tym przypadku przez GIL nie da się równolegle działać szybciej
niż sekwencyjnie? Proszę obudzić w sobie naukowca ;)

Przykładowe pliki również tu zamieszczam - proszę do nich zaglądać dopiero po napisaniu własnych albo gdy się "utknie"!

Przykładowy output kodu sekwencyjnego:
    Report saved to reports/report_sequential.txt
    Sequential code run for 62.91653633117676 seconds.

    Process finished with exit code 0

Przykładowy output kodu z wykorzystaniem 'threading':
    >wypisywanie informacji o ID wątku, który właśnie zakończył pracę<
    Report saved to reports/report_threading.txt
    Threads executed in 102.83041071891785 seconds.

    Process finished with exit code 0

Alternatywnie można przećwiczyć pobieranie różnych wolumenów danych z portali, które takie możliwości poprzez API
oferują. W przypadku danych pogodowych polecam bogaty wybór, aczkolwiek płatny, z Visual Crossing (dane pogodowe).
