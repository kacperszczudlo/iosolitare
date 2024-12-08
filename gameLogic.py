def get_column_index(gsetup, card):
    # Find the column index where the card is located
    for col_index, column in enumerate(gsetup.columns):
        if card in column:
            return col_index
    return None


def update_card_position(gsetup, card, x, y):
    # Usuń starą pozycję karty
    gsetup.card_positions = [
        position for position in gsetup.card_positions if position['card'] != card
    ]

    gsetup.card_positions.append({
        'card': card,
        'x': x,
        'y': y,
        'width': 100,
        'height': 145
    })

def rectangles_overlap(rect1, rect2):
    # Sprawdza, czy dwa prostokąty nachodzą się w osi X i Y
    overlap_x = rect1['x'] < rect2['x'] + rect2['width'] and rect1['x'] + rect1['width'] > rect2['x']
    overlap_y = rect1['y'] < rect2['y'] + rect2['height'] and rect1['y'] + rect1['height'] > rect2['y']
    return overlap_x and overlap_y

def is_valid_move(gsetup, selected_card, target_column_index):
    # Pobieramy docelową kolumnę
    target_column = gsetup.columns[target_column_index]

    # Jeśli docelowa kolumna jest pusta, sprawdzamy, czy wybrana karta to król
    if not target_column:
        return selected_card.figure.lower().startswith("king")

    # Pobieramy wierzchnią kartę z docelowej kolumny
    target_card = target_column[-1]
    
    # Sprawdzamy, czy wybrana karta może być przeniesiona na docelową kartę
    return (selected_card.points == target_card.points - 1 and
            ((selected_card.color == "red" and target_card.color == "black") or
             (selected_card.color == "black" and target_card.color == "red")))

def recycle_stock_waste(gsetup):
    # Przenoszenie kart z powrotem do stosu dobieralnego
    if gsetup.stock_waste:
        while gsetup.stock_waste:
            card = gsetup.stock_waste.pop()
            card.hide()  # Zakrywanie kart
            gsetup.stock_pile.append(card)

        # Ukrywanie przycisku po przeniesieniu kart
        if hasattr(gsetup, 'restore_button'):
            gsetup.restore_button.place_forget()
            del gsetup.restore_button

        # Odświeżenie stosu kart
        gsetup.game_ui.display_stock_pile()
        print("Recycled stock waste back to stock pile.")

def place_in_column(gsetup, x, y):
    # TODO: Umieszcza kartę w odpowiedniej kolumnie po wykonaniu ruchu.
    pass

def remove_card_from_column(gsetup, card):
    # Znajdź i usuń kartę z odpowiedniej kolumny
    for col_index, column in enumerate(gsetup.columns):
        if card in column:
            column.remove(card)  # Usuń kartę z kolumny
            print(f"Karta {card.figure} usunięta z kolumny {col_index + 1}")
            break
    else:
        print(f"Karta {card.figure} nie została znaleziona w żadnej kolumnie.")

    # Usuń kartę z logiki pozycji
    gsetup.card_positions = [
        pos for pos in gsetup.card_positions if pos['card'] != card
    ]
    print(f"Pozycja karty {card.figure} usunięta z logiki pozycji.")

    # Debugowanie - wyświetlenie aktualnego stanu kolumn
    print(f"Aktualny stan kolumn: {[len(col) for col in gsetup.columns]}")



def remove_card_from_positions(gsetup, card):
    gsetup.card_positions = [
        pos for pos in gsetup.card_positions if pos['card'] != card
    ]
    print(f"Pozycja karty {card.figure} usunięta z logiki pozycji.")


def find_first_empty_stack(gsetup):
    for stack in gsetup.upper_stack_areas:
        if stack['empty']:
            return stack
    return None  # Brak pustych stosów

def reset_stack(stack):
    stack['cards'].clear()
    stack['empty'] = True
    print("Stos został zresetowany.")

def print_final_stacks(gsetup):
    for i, stack in enumerate(gsetup.upper_stack_areas):
        cards_in_stack = [card.figure for card in stack['cards']]
        print(f"Stos {i + 1}: {cards_in_stack}")


def is_valid_move_to_stack(gsetup, card, stack):
    if not stack['cards']:  # Jeśli stos jest pusty
        return card.points == 1  # Tylko As może być pierwszą kartą
    last_card = stack['cards'][-1]
    return last_card.suit == card.suit and last_card.points == card.points - 1





