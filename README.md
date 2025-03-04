Witam wszystkich w repozytorium do kursu video "Inteligencja obliczeniowa. Algorytmy genetyczne i programowanie równoległe"!

Na wstępie należą się podziękowania trzem osobom:
1. Pani Beacie Chmiest z Wydawnictwa Helion, za wystąpienie z propozycją współpracy, sugestie i rady redaktorskie oraz przede wszystkim za cierpliwość przy moich ciągłych opóźnieniach w nadsyłaniu kolejnych filmów (przepraszam!);
2. Mojej żone Alicji, za wyrozumiałość, gdy nasze mieszkanie zmieniało się w studio nagraniowe o mało standardowych godzinach dnia i nocy;
3. Mojemu tacie Tomaszowi, za wiele nocy spędzonych nad uczeniem mnie programowania w Pascalu, gdy byłem jeszcze w gimnazjum.

Struktura repozytorium jest następująca:
- folder "01_wstep" zawiera zeszyty z użytecznymi bibliotekami w Pythonie, przykładami programowania obiektowego oraz skryptem do aplikacji okienkowej prostego kalkulatora;
- folder "02_algorytmy_genetyczne" zawiera zeszyty z optymalizacją funkcji oraz rozwiązaniami problemu plecakowego/złodzieja za pomocą algorytmów genetycznych z wykorzystaniem biblioteki PyGAD - dodatkowo w tym folderze znajdują się wszystkie pliki związane z pierwszym projektem, czyli rozwiązaniem problemy labiryntu;
- folder "03_programowanie_rownolegle" zawiera skrypty do uruchomienia za pomocą PyPy bądź CPython, profilowania kodu, generowania danych oraz pracy z wątkami i procesami - ponadto znajdują się tu również dane i praca domowa związana z przetwarzaniem danych za pomocą wątków oraz drugi projekt, czyli mnożenie dowolnie dużych macierzy kwadratowych równolegle;
- folder "notatki" z plikami PDF z tym, co pisałem podczas filmów teoretycznych.

Dodatkowo w repozytorium można znaleźć notatki z filmów teoretycznych i nieco przydatnych linków. Pomijając skrypty do aplikacji okienkowej oraz te stworzone do porównywania różnych implementacji Pythona, wszystko można uruchomić w Google Colaboratory. W razie potrzeby zachęcam do komentarzy i zgłaszania chęci kontaktu tutaj, w repozytorium. Zwłaszcza, jeśli zauważy się niedociągnięcia - jestem tylko człowiekiem i mogłem coś przeoczyć ;) albo czegoś nie wiedzieć. W razie kłopotów z korzystaniem z repozytorium zapraszam do tworzenia issues oraz dyskusji tu, na GitHub.

Spis treści do filmów w kursie:
01. Wstęp
	- 01.00 - Zwiastun
	- 01.01 - Krótko o kursie & polecane materiały
	- 01.02 - Krótka prezentacja gotowego repozytorium (https://www.github.com/gnypit/helion_io_part1)
	- 01.03 - Instalacja Pythona, instalowanie bibliotek, korzystanie z Google Colaboratory
	- 01.04 - Typy danych, struktury danych, klasy (programowanie obiektowe) - teoria
	- 01.05 - Stworzenie repozytorium Git, obsługa Jupytera oraz początek "projektu" kalkulatora
	- 01.06 - Kalkulator c.d
	- 01.07 - Kalkulator c.d.
	- 01.08 - Kalkulator - koniec wersji w zeszycie Jupytera
	- 01.09 - Predefiniowane metody dla klas w Pythonie
	- 01.10 - Kalkulator jako aplikacja okienkowa cz. 1
	- 01.11 - Kalkulator jako aplikacja okienkowa cz. 2
	- 01.12 - Kalkulator jako aplikacja okienkowa cz. 3
	- 01.13 - Używanie biblioteki numpy oraz matplotlib
	- 01.14 - Używanie biblioteki plotly
	- 01.15 - Krótko o bibliotekach pandas i seaborn
	- BONUS 01 - Funkcje, przestrzenie, miary i metryki
	- BONUS 02 - Prawdopodobieństwo & ekstrema funkcji
02. Wprowadzenie do algorytmów genetycznych z biblioteką pygad
	- 02.01 - Fundamenty algorytmów genetycznych - teoria
	- 02.02 - Operatory selekcji - ranking i losowy - teoria
	- 02.03 - Operatory selekcji - rangowy: liniowy i ekspotencjalny - teoria
	- 02.04 - Operatory selekcji - turniej + pseudokody - teoria
	- 02.05 - Operatory krzyżowania - teoria
	- 02.06 - PyGAD: strona www & dokumentacja
	- 02.07 - PyGAD ćw. nr 1: Optymalizacja funkcji wytrzymałości stopu
	- 02.08 - PyGAD ćw. nr 2: Problem partycji - cz. 1
	- 02.09 - PyGAD ćw. nr 2: Problem partycji - cz. 2
	- 02.10 - PyGAD ćw. nr 3: Problem "złodzieja"
	- 02.11 - PyGAD ćw. nr 3: Problem "złodzieja" c.d. - jak ewaluować kod
	- 02.12 - Projekt nr 1: Rozwiązywanie labiryntu cz. 1 (teoria & nieco o symulacjach)
	- 02.13 - Projekt nr 1: Rozwiązywanie labiryntu cz. 2
	- 02.14 - Projekt nr 1: Rozwiązywanie labiryntu cz. 3
	- 02.15 - Projekt nr 1: Rozwiązywanie labiryntu cz. 4
	- 02.16 - Projekt nr 1: Rozwiązywanie labiryntu cz. 5
	- 02.17 - Podsumowanie rozdziału nr 2 i zapowiedź rozdziału nr 3
03. Podstawy programowania równoległego
	- 03.01 - Omówienie idei programowania równoległego, procesów, wątków, oraz problemów CPU- bądź I/O-bound
	- 03.02 - Krótko o Python 3.13; omówienie kompilatorów i interpreterów
	- 03.03 - Używanie PyPy
	- 03.04 - Profilowanie kodu
	- 03.05 - Blokady i bariery na przykładzie przetwarzania danych tekstowych wątkami
	- 03.06 - Zmienne warunkowe, race condition - symulacja konta bankowego
	- 03.07 - Równoległe pobieranie danych za pomocą API i ich przetwarzanie - wątki c.d.
	- 03.08 - Trochę teorii związanej z macierzami
	- 03.09 - Projekt nr 2: mnożenie macierzy w sposób równoległy cz. 1
	- 03.10 - Projekt nr 2: mnożenie macierzy w sposób równoległy cz. 2
	- 03.11 - Projekt nr 2: mnożenie macierzy w sposób równoległy cz. 3
	- 03.12 - Podsumowanie rozdziału 3 i zapowiedź równoległych algorytmów genetycznych w drugiej części kursu

Aby nie popełniać autoplagiatu, już na tym etapie wspomnę, że część kodów jest inspirowana innym repozytorium:
https://github.com/gnypit/pyqkd

Ponadto należą się ukłony wobec wszelkich twórców oraz osób kontrybuujących do powstawania Pythona i bibliotek, których tu używaliśmy, z PyGAD na czele.

Finalnie, coby nieco autopromocji też było, zachęcam do zapoznania się z moimi publikacjami oraz zespołami naukowymi, z którymi mam przyjemność pracować:
 - ResearchGate https://www.researchgate.net/profile/Jakub-Gnyp?ev=hdr_xprf
 - Zakład Spektroskopii Fazy Skondensowanej (Instytut Fizyki Doświadczalnej, Uniwersytet Gdański) https://cmsd.ug.edu.pl/
 - Grupa badawcza Kwantowego Cyberbezpieczeństwa i Komunikacji w Międzynarodowym Centrum Teorii Technologii Kwantowych https://ictqt.ug.edu.pl/pages/quantum-cybersecurity-and-communication/

Do kontaktu zachęcam tutaj: https://www.linkedin.com/in/gnypit/


Powodzenia w nauce!
Jakub T. Gnyp