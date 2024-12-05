from tkinter import Button

import gameLogic
from gameLogic import *
def on_card_click(gsetup, event):
    # Obsługuje kliknięcie na kartę (zapamiętuje jej pozycję, jeśli jest odkryta).
    card = event.widget.card_object

    # Sprawdzenie, czy kliknięta karta jest ostatnią kartą w kolumnie
    for column in gsetup.columns:
        if column and column[-1] == card:
            gsetup.selected_card = card
            gsetup.start_x = event.widget.winfo_x()
            gsetup.start_y = event.widget.winfo_y()
            gsetup.original_x = event.widget.winfo_x()
            gsetup.original_y = event.widget.winfo_y()

            # To jest używane do odkładania karty
            gsetup.start_offset_x = event.x
            gsetup.start_offset_y = event.y

            # Sprawdzenie, czy karta jest odkryta
            if not gsetup.selected_card.revealed:
                gsetup.selected_card = None

            return  # Wyjdź z pętli, jeśli karta jest ostatnia i odkryta

    # Jeśli karta nie jest ostatnią kartą w kolumnie lub jest zakryta
    gsetup.selected_card = None


def on_card_drag(gsetup, event):
    # Obsługuje przeciąganie karty po planszy.
    if gsetup.selected_card:
        new_x = event.widget.winfo_x() + (event.x - gsetup.start_offset_x)
        new_y = event.widget.winfo_y() + (event.y - gsetup.start_offset_y)
        event.widget.place(x=new_x, y=new_y)
        gsetup.start_x = new_x
        gsetup.start_y = new_y

        # Sprawdzamy, czy karta nachodzi na inną kartę
        overlap_detected = False
        for label in gsetup.card_labels:
            if label != event.widget and rectangles_overlap(
                    {'x': new_x, 'y': new_y, 'width': 100, 'height': 145},
                    {'x': label.winfo_x(), 'y': label.winfo_y(), 'width': 100, 'height': 145}):
                # Sprawdzenie poprawności ruchu
                target_card = label.card_object
                target_column_index = get_column_index(gsetup, target_card)

                if target_card.revealed:
                    # Jeśli ruch jest poprawny podświetl na zielono
                    if target_column_index is not None and is_valid_move(gsetup, gsetup.selected_card,
                                                                         target_column_index):
                        gsetup.game_ui.highlight_card(event.widget, "green")
                        overlap_detected = True
                        break
                    # Jeśli ruch jest błędny podświetl na czerwono
                    elif target_column_index is not None and not is_valid_move(gsetup, gsetup.selected_card,
                                                                               target_column_index):
                        gsetup.game_ui.highlight_card(event.widget, "red")
                        overlap_detected = True
                        break
                    else:
                        gsetup.game_ui.highlight_card(event.widget, "black")
                        overlap_detected = True
                        break
            else:
                gsetup.game_ui.remove_highlight(event.widget)  # Usuwamy podświetlenie, jeśli nie nachodzi

        # Jeśli nie wykryto nachodzenia, możemy ustawić domyślny kolor
        if not overlap_detected:
            gsetup.game_ui.highlight_card(event.widget, "black")  # Ustawiamy czarne obramowanie, gdy nie ma nachodzenia



def on_card_release(gsetup, event):
    if gsetup.selected_card:
        card_x = event.widget.winfo_x()
        card_y = event.widget.winfo_y()

        target_column = None

        # Szukanie docelowej kolumny
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
            if is_valid_move(gsetup, gsetup.selected_card, target_column):
                # Usuwanie karty z poprzedniej kolumny
                source_column = next((column for column in gsetup.columns if gsetup.selected_card in column), None)
                if source_column:
                    source_column.remove(gsetup.selected_card)
                    # Odkryj kartę, która była pod wybraną kartą, jeśli taka istnieje
                    if len(source_column) > 0:
                        gsetup.reveal_previous_card(source_column)

                # Dodanie karty do docelowej kolumny
                gsetup.columns[target_column].append(gsetup.selected_card)
                new_position = gsetup.lower_stack_areas[target_column]['y'] + (len(gsetup.columns[target_column]) - 1) * 30
                event.widget.lift()
                print(f"Karta odłożona na stos {target_column + 1}")
                
                gsetup.card_positions.append({
                    'card': gsetup.selected_card,
                    'x': gsetup.lower_stack_areas[target_column]['x'],
                    'y': new_position
                })
                event.widget.place(x=gsetup.lower_stack_areas[target_column]['x'],
                                   y=new_position)
            else:
                print("Nieprawidłowy ruch. Karta nie została przeniesiona.")
                event.widget.place(x=gsetup.original_x, y=gsetup.original_y)
        else:
            print("Karta nie została odłożona na żaden stos.")
            event.widget.place(x=gsetup.original_x, y=gsetup.original_y)

        update_card_position(gsetup, gsetup.selected_card, card_x, card_y)
        gsetup.selected_card = None
        gsetup.game_ui.remove_highlight(event.widget)


def on_stock_pile_click(gsetup, event):
    if gsetup.stock_pile:
        # Jeżeli stos kart nie jest pusty, pobierz kartę
        card = gsetup.stock_pile.pop()
        card.reveal()
        gsetup.stock_waste.append(card)

        # Wyświetlenie karty na stosie odpadków obok talii
        waste_x = 270
        waste_y = 153
        gsetup.card_labels.append(gsetup.game_ui.create_card(waste_x, waste_y, card))

        event.widget.place_forget()

        if len(gsetup.stock_pile) == 0:
            # Pojawienie się przycisku, gdy stos kart jest pusty
            if not hasattr(gsetup, 'restore_button'):
                gsetup.restore_button = Button(
                    gsetup.window,
                    text="Przełóż karty",
                    command=lambda: recycle_stock_waste(gsetup)
                )
                gsetup.restore_button.place(x=140, y=200)

def on_card_double_click(gsetup, event):
    card = event.widget.card_object
    if not card.revealed:
        return

    card_suit = card.figure.split(' ')[-1]  # Pobiera kolor karty (np. 'clubs', 'hearts')

    for i, area in enumerate(gsetup.upper_stack_areas):
        if area['suit'] == card_suit:  # Dopasowanie koloru do placeholdera
            # Jeśli placeholder jest pusty, umieszczamy Asa
            if area.get('card') is None:  # Placeholder jest pusty
                if card.points == 1:  # Tylko asy mogą zaczynać stos
                    gsetup.upper_stack_areas[i]['card'] = card
                    event.widget.place(x=area['x'], y=area['y'])  # Pozycja na ekranie
                    event.widget.lift()  # Podnosi kartę na wierzch (w warstwie)

                    # Usuń kartę z jej kolumny
                    source_column = next((column for column in gsetup.columns if card in column), None)
                    if source_column:
                        source_column.remove(card)
                        # Odkrywanie karty pod As-em
                        if len(source_column) > 0:
                            gsetup.reveal_previous_card(source_column)

                    print(f"Karta {card.figure} odłożona na stos {i + 1} (placeholder {area}).")
                    return

            # Jeśli karta pasuje do wierzchniej na stosie (np. 2 na Asa), to dodajemy ją
            elif gsetup.upper_stack_areas[i]['card'].points == card.points - 1:
                gsetup.upper_stack_areas[i]['card'] = card

                # Trzymamy karty na stosie w "wirtualnej" kolejności
                stacked_cards = gsetup.upper_stack_areas[i].get('stacked_cards', [])
                stacked_cards.append(card)  # Dodajemy kartę na stos w logice
                gsetup.upper_stack_areas[i]['stacked_cards'] = stacked_cards

                # Usuń kartę z jej kolumny
                source_column = next((column for column in gsetup.columns if card in column), None)
                if source_column:
                    source_column.remove(card)
                    # Odkrywanie karty pod As-em
                    if len(source_column) > 0:
                        gsetup.reveal_previous_card(source_column)

                # Sortowanie kart na stosie w logice gry
                stacked_cards.sort(key=lambda c: c.points, reverse=True)

                # Karta o wyższej wartości powinna być widoczna na wierzchu
                event.widget.place(x=area['x'], y=area['y'])  # Pozostawienie tej samej pozycji na ekranie
                event.widget.lift()  # Podnosi kartę na wierzch (w warstwie)

                print(f"Karta {card.figure} odłożona na stos {i + 1} (placeholder {area}).")
                return

    print(f"Nie można odłożyć karty {card.figure}.")











