from tkinter import Button
from functools import partial
import gameLogic
from gameLogic import *

def on_card_click(gsetup, event):
    card = event.widget.card_object

    if not card.revealed:
        return

    # Sprawdzamy, czy karta znajduje się na górnym stosie końcowym
    for area in gsetup.upper_stack_areas:
        if area['card'] == card:  # Jeśli kliknięto ostatnią kartę na stosie
            gsetup.selected_card = card
            gsetup.start_x = event.widget.winfo_x()
            gsetup.start_y = event.widget.winfo_y()
            gsetup.original_x = event.widget.winfo_x()
            gsetup.original_y = event.widget.winfo_y()
            gsetup.start_offset_x = event.x
            gsetup.start_offset_y = event.y
            gsetup.moving_cards = [card]  # Tylko jedna karta jest przenoszona
            print(f"Selected card {card.figure} from foundation stack ({area['suit']}).")
            return

    # Obsługa dla kart w kolumnach lub stosie dobieralnym
    for column in gsetup.columns:
        if card in column:
            card_index = column.index(card)
            gsetup.selected_card = card
            gsetup.start_x = event.widget.winfo_x()
            gsetup.start_y = event.widget.winfo_y()
            gsetup.original_x = event.widget.winfo_x()
            gsetup.original_y = event.widget.winfo_y()
            gsetup.start_offset_x = event.x
            gsetup.start_offset_y = event.y
            gsetup.moving_cards = column[card_index:]
            print(f"Selected card {card.figure} from column {gsetup.columns.index(column) + 1}.")
            return

    if card in gsetup.stock_waste:
        gsetup.selected_card = card
        gsetup.start_x = event.widget.winfo_x()
        gsetup.start_y = event.widget.winfo_y()
        gsetup.original_x = event.widget.winfo_x()
        gsetup.original_y = event.widget.winfo_y()
        gsetup.start_offset_x = event.x
        gsetup.start_offset_y = event.y
        gsetup.moving_cards = [card]
        print(f"Selected card {card.figure} from stock waste.")



def on_card_drag(gsetup, event):
    if gsetup.selected_card:
        # Obliczamy różnicę pozycji kursora myszy
        delta_x = event.x - gsetup.start_offset_x
        delta_y = event.y - gsetup.start_offset_y

        # Przesuwamy wszystkie zaznaczone karty
        for i, card in enumerate(gsetup.moving_cards):
            card_label = next(label for label in gsetup.card_labels if label.card_object == card)
            card_label.place(x=gsetup.start_x + delta_x, y=gsetup.start_y + delta_y + i * 30)

        # Aktualizujemy pozycję początkową
        gsetup.start_x += delta_x
        gsetup.start_y += delta_y

        overlap_detected = False

        # Sprawdzanie kolizji z kolumnami
        for label in gsetup.card_labels:
            if label != event.widget and rectangles_overlap(
                    {'x': gsetup.start_x, 'y': gsetup.start_y, 'width': 100, 'height': 145 + 30 * (len(gsetup.moving_cards) - 1)},
                    {'x': label.winfo_x(), 'y': label.winfo_y(), 'width': 100, 'height': 145}):
                target_card = label.card_object
                target_column_index = get_column_index(gsetup, target_card)

                if target_card.revealed:
                    if target_column_index is not None and is_valid_move(gsetup, gsetup.selected_card, target_column_index):
                        # Podświetlamy karty na zielono, jeśli ruch jest prawidłowy
                        for card in gsetup.moving_cards:
                            card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                            gsetup.game_ui.highlight_card(card_label, "green")
                        overlap_detected = True
                        break
                    elif target_column_index is not None:
                        # Podświetlamy karty na czerwono, jeśli ruch jest nieprawidłowy
                        for card in gsetup.moving_cards:
                            card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                            gsetup.game_ui.highlight_card(card_label, "red")
                        overlap_detected = True
                        break

        # Sprawdzanie kolizji z górnymi stosami
        for area in gsetup.upper_stack_areas:
            if rectangles_overlap(
                    {'x': gsetup.start_x, 'y': gsetup.start_y, 'width': 100, 'height': 145},
                    area):
                if is_valid_upper_stack_move(gsetup.selected_card, area):
                    gsetup.game_ui.highlight_card(event.widget, "green")
                    overlap_detected = True
                else:
                    gsetup.game_ui.highlight_card(event.widget, "red")
                break

        if not overlap_detected:
            # Usuwamy podświetlenie, jeśli nie wykryto kolizji
            for card in gsetup.moving_cards:
                card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                gsetup.game_ui.highlight_card(card_label, "black")

        # Wyświetlenie komunikatu w terminalu o przeciąganiu karty
        print(f"Dragging card: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")


def on_card_release(gsetup, event):
    if gsetup.selected_card:
        card_x = event.widget.winfo_x()  # Pobieramy pozycję karty
        card_y = event.widget.winfo_y()

        target_column = None  # Zmienna do przechowywania indeksu docelowej kolumny
        valid_move = False  # Flaga do śledzenia poprawnego ruchu

        # Sprawdzanie kolizji z górnymi stosami
        for area in gsetup.upper_stack_areas:
            if rectangles_overlap(
                    {'x': card_x, 'y': card_y, 'width': 100, 'height': 145},
                    area):
                if is_valid_upper_stack_move(gsetup.selected_card, area):
                    # Dodanie karty do stosu
                    area['stack'].append(gsetup.selected_card)
                    area['card'] = gsetup.selected_card  # Ustawienie wierzchniej karty

                    # Usuń kartę z kolumny źródłowej
                    source_column = next((col for col in gsetup.columns if gsetup.selected_card in col), None)
                    if source_column:
                        source_column.remove(gsetup.selected_card)
                        if len(source_column) > 0:
                            # Odkrywamy kartę pod spodem, jeśli istnieje
                            gsetup.reveal_previous_card(source_column)
                        else:
                            # Jeśli kolumna jest pusta, aktualizujemy placeholder
                            col_index = gsetup.columns.index(source_column)
                            placeholder_area = gsetup.lower_stack_areas[col_index]
                            print(f"Column {col_index + 1} is now empty.")

                    # Umieść kartę na górnym stosie
                    event.widget.place(x=area['x'], y=area['y'])
                    event.widget.lift()

                    # Wyświetlenie komunikatu o ruchu
                    print(f"Moved card {gsetup.selected_card.figure} to foundation stack ({area['suit']}).")
                    valid_move = True

                    # Drukowanie stanu wszystkich stosów
                    print("Current state of all foundation stacks:")
                    for idx, stack_area in enumerate(gsetup.upper_stack_areas, start=1):
                        stack_cards = [card.figure for card in stack_area['stack']]
                        print(f"Foundation stack {idx} ({stack_area['suit']}): {stack_cards}")

                    break

        # Jeśli ruch na górny stos był poprawny, kończymy funkcję
        if valid_move:
            gsetup.selected_card = None
            gsetup.moving_cards = []
            gsetup.game_ui.remove_highlight(event.widget)
            return

        # Obsługa wyciągania kart z górnych stosów
        for area in gsetup.upper_stack_areas:
            if gsetup.selected_card in area['stack']:
                # Jeśli karta pochodzi z górnego stosu, usuwamy ją
                area['stack'].remove(gsetup.selected_card)
                if len(area['stack']) > 0:
                    area['card'] = area['stack'][-1]  # Ustawienie nowej wierzchniej karty
                else:
                    area['card'] = None  # Jeśli stos jest pusty

                # Jeśli ruch jest nieprawidłowy, karta wraca na swoje miejsce
                if not valid_move:
                    event.widget.place(x=area['x'], y=area['y'])
                    print(f"Invalid move: {gsetup.selected_card.figure} from foundation stack ({area['suit']}).")
                    return
                break

        # Szukanie docelowej kolumny, do której karta ma być przeniesiona
        for col_index, column in enumerate(gsetup.columns):
            if not column:  # Jeśli kolumna jest pusta
                placeholder_area = gsetup.lower_stack_areas[col_index]
                if rectangles_overlap(
                        {'x': card_x, 'y': card_y, 'width': 100, 'height': 145},
                        placeholder_area
                ):
                    target_column = col_index
                    break
            else:  # Jeśli kolumna zawiera karty
                last_card = column[-1]
                last_card_position = next(
                    (pos for pos in gsetup.card_positions if pos['card'] == last_card), None
                )
                if last_card_position and rectangles_overlap(
                        {'x': card_x, 'y': card_y, 'width': 100, 'height': 145},
                        last_card_position
                ):
                    target_column = col_index
                    break

        if target_column is not None:
            # Sprawdzamy, czy ruch jest prawidłowy
            if is_valid_move(gsetup, gsetup.selected_card, target_column):
                # Usuwanie kart z poprzedniej kolumny
                source_column = next((column for column in gsetup.columns if gsetup.selected_card in column), None)
                if source_column:
                    card_index = source_column.index(gsetup.selected_card)
                    for card in gsetup.moving_cards:
                        source_column.remove(card)

                # Dodawanie kart do docelowej kolumny
                gsetup.columns[target_column].extend(gsetup.moving_cards)
                for i, card in enumerate(gsetup.moving_cards):
                    card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                    card_label.place(x=gsetup.lower_stack_areas[target_column]['x'],
                                     y=gsetup.lower_stack_areas[target_column]['y'] + (len(gsetup.columns[target_column]) - len(gsetup.moving_cards)) * 30 + i * 30)
                    card_label.lift()  # Ustawienie karty na wierzchu

                # Odkryj kartę pod spodem, jeśli istnieje
                if source_column and len(source_column) > 0:
                    gsetup.reveal_previous_card(source_column)

                # Usunięcie podświetlenia całego stosu
                for card in gsetup.moving_cards:
                    card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                    gsetup.game_ui.remove_highlight(card_label)

                gsetup.moving_cards = []

                # Dodaj obsługę przenoszenia kart ze stosu dobieralnego
                if gsetup.selected_card in gsetup.stock_waste:
                    gsetup.stock_waste.remove(gsetup.selected_card)

                # Wyświetlenie komunikatu w terminalu o odłożeniu karty
                print(f"Placed card: {gsetup.selected_card.figure} of {gsetup.selected_card.suit} in column {target_column + 1}")
                print(f"Current state of columns: {[len(col) for col in gsetup.columns]}")

            else:
                # Zwracanie kart na pierwotne miejsce, jeśli ruch jest nieprawidłowy
                for i, card in enumerate(gsetup.moving_cards):
                    card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                    card_label.place(x=gsetup.original_x, y=gsetup.original_y + i * 30)
                    gsetup.game_ui.remove_highlight(card_label)

                # Wyświetlenie komunikatu w terminalu o nieprawidłowym ruchu
                print(f"Invalid move: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")

        else:
            # Zwracanie kart na pierwotne miejsce, jeśli nie znaleziono docelowej kolumny
            for i, card in enumerate(gsetup.moving_cards):
                card_label = next(label for label in gsetup.card_labels if label.card_object == card)
                card_label.place(x=gsetup.original_x, y=gsetup.original_y + i * 30)
                gsetup.game_ui.remove_highlight(card_label)

            # Wyświetlenie komunikatu w terminalu o braku docelowej kolumny
            print(f"No valid target column for: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")

        # Aktualizowanie pozycji karty
        update_card_position(gsetup, gsetup.selected_card, card_x, card_y)
        gsetup.selected_card = None
        gsetup.moving_cards = []
        gsetup.game_ui.remove_highlight(event.widget)







def on_stock_pile_click(gsetup, event):
    if gsetup.stock_pile:
        # Pobranie karty z wierzchu stosu dobieralnego
        card = gsetup.stock_pile.pop()
        card.reveal()  # Odkrycie karty
        gsetup.stock_waste.append(card)  # Dodanie karty do stosu odpadków

        # Pozycje dla wyświetlenia karty
        waste_x = 270
        waste_y = 153
        card_label = gsetup.game_ui.create_card(waste_x, waste_y, card)
        gsetup.card_labels.append(card_label)

        # Dodanie funkcji obsługi kliknięć i przeciągania dla nowo wyświetlonej karty
        card_label.bind("<ButtonPress-1>", partial(on_card_click, gsetup))
        card_label.bind("<B1-Motion>", partial(on_card_drag, gsetup))
        card_label.bind("<ButtonRelease-1>", partial(on_card_release, gsetup))
        card_label.bind("<Double-1>", partial(on_card_double_click, gsetup))

        # Usunięcie etykiety karty z interfejsu użytkownika
        for label in gsetup.card_labels[:]:
            if label.card_object == card:
                gsetup.card_labels.remove(label)
                label.place_forget()
                break

        # Sprawdzenie, czy stos dobieralny jest pusty
        '''if len(gsetup.stock_pile) == 0:
            if not hasattr(gsetup, 'restore_button'):
                gsetup.restore_button = gsetup.game_ui.create_placeholder(131, 153)
                gsetup.restore_button.bind("<ButtonPress-1>", lambda e: recycle_stock_waste(gsetup))
            else:
                gsetup.restore_button.place(x=131, y=153)'''

        # Wyświetlenie komunikatu w terminalu o pobraniu karty
        print(f"Drew card: {card.figure} of {card.suit}")

    elif gsetup.stock_waste:
        # Przełożenie kart z powrotem na stos dobieralny
        recycle_stock_waste(gsetup)


def on_card_double_click(gsetup, event):
    card = event.widget.card_object
    if not card.revealed:
        return

    card_suit = card.figure.split(' ')[-1]  # Pobiera kolor karty (np. 'clubs', 'hearts')

    for i, area in enumerate(gsetup.upper_stack_areas):
        if area['suit'] == card_suit:  # Dopasowanie koloru do placeholdera
            # Jeśli placeholder jest pusty, umieszczamy Asa
            if not area['stack']:  # Placeholder jest pusty
                if card.points == 1:  # Tylko asy mogą zaczynać stos
                    area['stack'].append(card)
                    area['card'] = card
                    event.widget.place(x=area['x'], y=area['y'])  # Pozycja na ekranie
                    event.widget.lift()  # Podnosi kartę na wierzch (w warstwie)

                    # Usuń kartę z jej kolumny
                    source_column = next((column for column in gsetup.columns if card in column), None)
                    if source_column:
                        source_column.remove(card)
                        # Odkrywanie karty pod spodem
                        if len(source_column) > 0:
                            gsetup.reveal_previous_card(source_column)
                        else:
                            # Jeśli kolumna jest pusta, aktualizujemy placeholder
                            col_index = gsetup.columns.index(source_column)
                            print(f"Column {col_index + 1} is now empty.")

                    print(f"Moved card {card.figure} to foundation stack ({area['suit']}).")

            # Jeśli karta pasuje do wierzchniej na stosie (np. 2 na Asa), to dodajemy ją
            elif area['card'].points == card.points - 1:
                area['stack'].append(card)
                area['card'] = card

                event.widget.place(x=area['x'], y=area['y'])  # Pozycja na ekranie
                event.widget.lift()  # Podnosi kartę na wierzch (w warstwie)

                # Usuń kartę z jej kolumny
                source_column = next((column for column in gsetup.columns if card in column), None)
                if source_column:
                    source_column.remove(card)
                    # Odkrywanie karty pod spodem
                    if len(source_column) > 0:
                        gsetup.reveal_previous_card(source_column)
                    else:
                        # Jeśli kolumna jest pusta, aktualizujemy placeholder
                        col_index = gsetup.columns.index(source_column)
                        print(f"Column {col_index + 1} is now empty.")

                print(f"Moved card {card.figure} to foundation stack ({area['suit']}).")

            # Wyświetlenie stanu wszystkich stosów
            print("Current state of all foundation stacks:")
            for idx, stack_area in enumerate(gsetup.upper_stack_areas, start=1):
                stack_cards = [card.figure for card in stack_area['stack']]
                print(f"Foundation stack {idx} ({stack_area['suit']}): {stack_cards}")

            return

    print(f"Cannot move card {card.figure} to any foundation stack.")













