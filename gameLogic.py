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
    # Sprawdza poprawność ruchu.
    target_column = gsetup.columns[target_column_index]
    if not target_column:
        return True

    last_card = target_column[-1]
    valid_color = (card.figure.split(' ')[-1] != last_card.figure.split(' ')[-1])
    valid_rank = (card.points == last_card.points - 1)

    return valid_color and valid_rank

def recycle_stock_waste(gsetup):
    # Przenoszenie kart z powrotem do stock_pile
    if gsetup.stock_waste:
        while gsetup.stock_waste:
            card = gsetup.stock_waste.pop()
            card.hide()  # Zakrywanie kart
            gsetup.stock_pile.append(card)

        for label in gsetup.card_labels[:]:
            if label.card_object in gsetup.stock_pile:
                label.place_forget()
                gsetup.card_labels.remove(label)

        # Ukrywanie przycisku po przeniesieniu kart
        gsetup.restore_button.place_forget()
        del gsetup.restore_button

        # Odświeżenie stosu kart
        gsetup.game_ui.display_stock_pile()
        print("Karty zostały przełożone z powrotem na stos kart.")

def place_in_column(gsetup, x, y):
    # TODO: Umieszcza kartę w odpowiedniej kolumnie po wykonaniu ruchu.
    pass