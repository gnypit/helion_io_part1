Szanowni Państwo!

W tym folderze znajduje się generator danych liczbowych do plików CSV (ang. "comma-separated values"). Z obecnymi
ustawieniami powinien utworzyć 4 pliki po 10^7 wierszy i 10 kolumn, z liczbami zmiennoprzecinkowymi
losowo wybranymi z rozkładu jednostajnego na [0, 100] w każdym wierszu i kolumnie. Łączny rozmiar takich plików powinien
wynosić ok. 6,8 GB. Załóżmy, że chcemy te dane wczytać oraz stworzyć na ich podstawie raport ze średnimi wartościami
liczb w każdym z nich, z najmniejszymi i największymi występującymi liczbami. Proszę pamiętać, że łączny rozmiar
danych do przetworzenia powinien być mniejszy niż dostępna pamięć RAM - Python będzie te dane po wczytaniu "trzymać"
właśnie w pamięci podręcznej i potrzebuje do tego miejsca.

W tym celu proponuję uzupełnić skrypty z "praca_domowa" w nazwie. Stosując wątki na tym przykładzie, powinniśmy uzyskać
zauważalne przyspieszenie przetwarzania. Ponownie, jak w przypadku danych tekstowych, sam folder z danymi dodałem do
.gitignore, aby nie wymuszać na nikim pobieranie tak dużych plików. Stąd dane wygenerować należy samemu.

Poza `threading`, którego już używaliśmy, proponuję spróbować użyć `ThreadPoolExecutor`:
https://docs.python.org/3/library/concurrent.futures.html

Zachęcam do eksperymentowania oraz rozważenia odpowiedzi na następujące pytania: przy jakim rozmiarze i liczbie plików
CSV tempo pracy kodu sekwencyjnego i równoległego są do siebie zbliżone? Jakie jest ryzyko, jeśli ze względu
na obliczenia cały kod równoległy - w tym wczytywanie danych - byłby oparty na procesach, nie wątkach?

Prosze patrzeć do wzorcowych skryptów oraz raportów dopiero po napisaniu własnych albo gdy się "utknie"!

Przykładowy output kodu sekwencyjnego:
    Processing CSV files: 100%|██████████| 4/4 [00:50<00:00, 12.72s/it]

    Sequential processing completed in 50.89 seconds.
    Report saved as 'report.txt'.

    Process finished with exit code 0

Przykładowy output z wykorzystaniem threading:
    Processing CSV files: 100%|██████████| 4/4 [00:15<00:00,  3.98s/it]

    Threading processing completed in 15.94 seconds.
    Report saved as 'report_threading.txt'.

    Process finished with exit code 0

Przykładowy output z wykorzystaniem ThreadPoolExecutor:
    Processing CSV files: 100%|██████████| 4/4 [00:16<00:00,  4.14s/it]

    Parallel processing completed in 16.59 seconds.
    Report saved as 'report_parallel.txt'.

    Process finished with exit code 0

Pozdrawiam serdecznie,
Jakub T. Gnyp