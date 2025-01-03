# Gra Pasjans (Klondike) w Pythonie z Tkinter

Ten projekt to implementacja klasycznej wersji gry Pasjans (Klondike) przy użyciu języka Python i biblioteki Tkinter.  
Gra oferuje możliwość przeciągania i upuszczania kart, sprawdzania poprawności ruchów, cofania ruchów, a także współpracuje z bazą danych PostgreSQL (zapisywanie i wyświetlanie najlepszych wyników).

---

## Spis treści
1. [Opis projektu](#opis-projektu)
2. [Funkcjonalności](#funkcjonalności)
3. [Struktura plików](#struktura-plików)
4. [Wymagania](#wymagania)
5. [Instrukcja instalacji](#instrukcja-instalacji)
6. [Uruchomienie projektu](#uruchomienie-projektu)
7. [Jak grać](#jak-grać)
8. [Dodatkowe informacje](#dodatkowe-informacje)
9. [Kontakt](#kontakt)

---

## Opis projektu

Gra Pasjans (Klondike) jest jedną z najpopularniejszych odmian pasjansa. W tym projekcie zaimplementowano następujące elementy:
- Logikę rozkładania kart (pierwsze rozdanie) zgodnie z klasycznymi zasadami.
- Obsługę ruchów (przeciąganie i upuszczanie kart do kolumn, na stos typu foundation, a także na stos dobierania i stos odrzuconych).
- Interfejs graficzny utworzony w oparciu o **Tkinter** – karty są prezentowane w formie etykiet (`Label`), które można przeciągać myszą.
- Częściową integrację z bazą danych PostgreSQL w celu zapisywania i odczytywania najlepszych wyników (high score).

---

## Funkcjonalności

1. **Rozdawanie kart**  
   - Początkowe rozłożenie 28 kart w 7 kolumnach, w każdej ostatnia karta jest odkryta.  
   - Pozostałe 24 karty trafiają do stosu dobierania (stock).

2. **Przeciąganie i upuszczanie kart**  
   - Logika `drag & drop` zaimplementowana w pliku `gameEvents.py`.  
   - Możliwość zaznaczenia całego ciągu kart w kolumnie i przeniesienia go na inną kolumnę, jeśli ruch jest poprawny.

3. **Sprawdzanie poprawności ruchów**  
   - Karty można kłaść wyłącznie według klasycznych reguł (naprzemienny kolor, wartość o 1 niższa).  
   - Tylko Król może być położony na pustą kolumnę.  
   - Na foundation można kłaść karty w rosnącej kolejności i w odpowiednim kolorze (Asy zaczynają puste stosy).

4. **Obsługa stosu dobierania (stock) i odrzuconych kart (waste)**  
   - Możliwość kilkukrotnego przerzucenia kart ze stosu odrzuconych na stos dobierania, dopóki gra nie zostanie ukończona.

5. **System punktacji**  
   - Różne modyfikatory punktów przy odkrywaniu kart, przenoszeniu kart na foundation bądź do kolumn.  
   - Możliwość zapisu najlepszych wyników w bazie danych.

6. **Zapis i odczyt rekordów z bazy PostgreSQL**  
   - Funkcje `get_highscore()` oraz `add_highscore()` w pliku `gameLogic.py`.  
   - Wyświetlanie listy najlepszych wyników w oknie po zakończeniu gry lub z poziomu menu głównego.

7. **Interfejs graficzny**  
   - Prosty, ale przejrzysty interfejs z przyciskami do rozpoczęcia nowej gry, cofnięcia ruchu czy wyświetlenia wyników.  
   - Timer (czas rozgrywki), licznik ruchów i aktualna punktacja.

8. **Efekty wizualno-muzyczne**  
   - Prosta animacja GIF po wygranej.  
   - Odtwarzanie dźwięku w tle (wykorzystanie biblioteki **pygame**).

---

## Struktura plików

```
├── main.py                # Główne wywołanie programu (menu startowe, start rozgrywki)
├── gameSetup.py           # Konfiguracja i zarządzanie stanem gry, reset gry, cofanie ruchów
├── gameUI.py              # Warstwa graficzna: tworzenie okien, przycisków, timera, obsługa animacji
├── gameEvents.py          # Obsługa zdarzeń myszy (klik, przeciągnięcie, upuszczenie, dobieranie kart)
├── gameLogic.py           # Funkcje pomocnicze do walidacji ruchów i zarządzania logiką, połączenie z bazą danych
├── cardDeck.py            # Tworzenie i mieszanie talii 52 kart
├── card.py                # Klasa reprezentująca pojedynczą kartę
├── firstDeal.py           # Funkcja rozkładu początkowych 28 kart do 7 kolumn
├── resources/             # Folder z zasobami: grafiki kart, tła, placeholdery, pliki audio itp.
│   ├── cards/             # Obrazy kart (asy, króle, itd.)
│   ├── placeholders/      # Obrazy placeholderów stosów
│   ├── background/        # Obrazy tła
│   ├── menu/              # Obrazy menu (np. tło menu, obraz corona itp.)
│   └── win/               # Pliki animacji i dźwięków wygranej (gif, mp3)
└── README.md              # Dokumentacja projektu
└── requirements.txt       # Lista wymaganych bibliotek
```

---

## Wymagania

- **Python 3.8+** (zalecane)  
- Zainstalowane biblioteki wymienione w [requirements.txt](#instrukcja-instalacji)  
- Dostępna biblioteka **tkinter** (w większości dystrybucji Pythona jest domyślnie)  
- Jeśli korzystasz z bazy PostgreSQL:
  - Działający serwer PostgreSQL
  - Utworzona baza danych i tabela `player` (jak w kodzie `gameLogic.py`)
  - Zmodyfikowane parametry w `gameLogic.py` (host, user, password) na własne

---

## Instrukcja instalacji

1. **Klonowanie repozytorium:**
   ```bash
   git clone https://github.com/kacperszczudlo/iosolitare.git
   cd pasjans
   ```

2. **Utworzenie i aktywacja wirtualnego środowiska (opcjonalne, ale zalecane):**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / Mac
   # lub
   venv\Scripts\activate           # Windows
   ```

3. **Instalacja wymaganych bibliotek:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcjonalne) Konfiguracja bazy danych**  
   Jeżeli chcesz korzystać z opcji zapisu wyników do bazy PostgreSQL, w pliku `gameLogic.py` (funkcje `get_highscore()` i `add_highscore()`) należy ustawić parametry połączenia:
   ```python
   connection = psycopg2.connect(
       host="adres_serwera",
       port="5432",
       user="nazwa_uzytkownika",
       password="haslo",
       database="nazwa_bazy"
   )
   ```
   Upewnij się, że w bazie istnieje tabela `player`:
   ```sql
   CREATE TABLE IF NOT EXISTS player (
       nickname VARCHAR(255),
       score INT
   );
   ```

---

## Uruchomienie projektu

1. Upewnij się, że jesteś w głównym katalogu projektu (tam, gdzie `main.py`).
2. W linii poleceń wpisz:
   ```bash
   python main.py
   ```
3. Uruchomi się okno główne aplikacji z menu:
   - **Nowa gra**: rozpoczyna rozgrywkę i wyświetla planszę.  
   - **Najlepsze wyniki**: próba połączenia z bazą i pobrania top wyników.  
   - **Zasady gry**: otwiera okno z tekstem zasad, o ile jest obecny plik `rules.txt`.  
   - **Samouczek**, **Zmiana Motywu** (jeśli zaimplementowane): dodatkowe przyciski.

---

## Jak grać

1. Po kliknięciu **Nowa gra** następuje automatyczne potasowanie i rozłożenie 28 kart w 7 kolumnach.  
2. Pozostałe 24 karty trafiają do stosu dobierania (u góry po lewej).  
3. Aby przenieść kartę (lub karty) z jednej kolumny do drugiej, **kliknij i przytrzymaj** wybraną kartę, a następnie **przeciągnij** ją w docelowe miejsce i **upuść** (zwolnij przycisk myszy).  
4. Sprawdzana jest poprawność ruchu – karty muszą być kładzione w porządku malejącym, naprzemiennego koloru (czerwona na czarną i odwrotnie).  
5. Puste kolumny mogą przyjąć **tylko Króla**.  
6. Możesz **dobrać kartę** ze stosu dobierania – kliknięcie na stos odwraca wierzchnią kartę i kładzie ją na stos odrzuconych (obok).  
7. W każdej chwili możesz **cofnąć ruch** (o ile nie zacząłeś nowej akcji) przyciskiem **Cofnij**.  
8. Wygrywasz, gdy uda Ci się ułożyć wszystkie karty w 4 stosach typu foundation (hearts, diamonds, clubs, spades) w rosnącej kolejności (od Asa do Króla), a wszystkie kolumny są puste bądź ich karty są odkryte i gotowe do przeniesienia.

---

## Dodatkowe informacje

- **Timer i punkty**: W prawym górnym rogu widać zegar odmierzający czas gry, licznik ruchów oraz aktualną liczbę punktów.  
- **Animacja i muzyka**: Po wygranej wyświetla się animacja GIF i odtwarza się muzyka z katalogu `resources/win/` (wymaga biblioteki **pygame**).  
- **Zapis wyników**: Jeśli wprowadzisz swój nick i klikniesz **Dodaj wynik** po wygranej, wynik zapisze się w bazie.  
- **Najlepsze wyniki**: Możesz podejrzeć listę rankingową z bazy danych w menu głównym.  

---

## Kontakt

W razie pytań lub problemów prosimy o kontakt:
- **Email**: [kacper.szczudlo@gmail.com](mailto:kacper.szczudlo@gmail.com)
- **GitHub**: [kacperszczudlo](https://github.com/kacperszczudlo)

Zapraszamy do testowania, zgłaszania uwag i propozycji rozwoju!


