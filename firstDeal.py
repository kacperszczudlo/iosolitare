class FirstDeal:
    def __init__(self, deck):
        # Inicjalizuje pierwsze rozdanie, przygotowując 7 kolumn dla kart.
        self.deck = deck
        self.columns = [[] for _ in range(7)]

    def setup_initial_layout(self):
        # Ustawia początkowy układ kart w kolumnach, odkrywając ostatnią kartę w każdej kolumnie.
        index = 0
        for col in range(7):
            for row in range(col + 1):
                card = self.deck.cards[index]

                if row == col:
                    card.reveal()
                self.columns[col].append(card)
                index += 1

            # Kod testowy: symuluje błędy w układzie kart.
            """
            if col == 2:  
                self.columns[col].pop()
            if col == 4:  
                self.columns[col][-1].hide()
            """
        for col_index, column in enumerate(self.columns):
            print(
                f"(Po błędach) Kolumna {col_index + 1}: {len(column)} kart, ostatnia odkryta: {column[-1].revealed if column else None}")

        return self.columns

    def validate_initial_layout(self):
        # Sprawdza poprawność początkowego układu kart.
        errors = []

        for col_index, column in enumerate(self.columns):
            # Sprawdza, czy liczba kart w każdej kolumnie jest poprawna.
            print(f"(Walidacja) Kolumna {col_index + 1}: {len(column)} kart (oczekiwane: {col_index + 1})")
            if len(column) != col_index + 1:
                errors.append(f"Kolumna {col_index + 1} ma {len(column)} kart zamiast {col_index + 1}.")

        # Sprawdza, czy ostatnia karta w każdej kolumnie jest odkryta.
        for col_index, column in enumerate(self.columns):
            print(
                f"(Walidacja) Ostatnia karta w kolumnie {col_index + 1}: {'odkryta' if column and column[-1].revealed else 'zakryta'}")
            if column and not column[-1].revealed:
                errors.append(f"Ostatnia karta w kolumnie {col_index + 1} nie jest odkryta.")

        print("Walidacja błędów:", errors)
        return errors
