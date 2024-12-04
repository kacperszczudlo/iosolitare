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


def is_valid_move(gsetup, card, target_column_index):
    target_column = gsetup.columns[target_column_index]

    if not target_column:  # Jeśli kolumna jest pusta
        result = card.figure.lower().startswith("king")  # Tylko Król może być umieszczony na pusty stos
        print(f"Sprawdzanie pustej kolumny: {'dozwolony' if result else 'zabroniony'} ruch dla karty {card.figure}")
        return result

    last_card = target_column[-1]
    valid_rank = (card.points == last_card.points - 1)
    card_color = card.figure.split(' ')[-1]
    last_card_color = last_card.figure.split(' ')[-1]
    red_suits = ['hearts', 'diamonds']
    black_suits = ['clubs', 'spades']
    # Sprawdzanie, czy karta i ostatnia karta mają różne kolory (np. pik i trefl lub kier i karo)
    valid_color = ((card_color in red_suits and last_card_color in black_suits) or
                   (card_color in black_suits and last_card_color in red_suits))

    result = valid_color and valid_rank
    print(f"Ruch do kolumny {target_column_index + 1}: {'dozwolony' if result else 'zabroniony'} ruch dla karty {card.figure}")
    return result


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

