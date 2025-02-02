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
    target_column = gsetup.columns[target_column_index]

        # Jeśli kolumna jest pusta, sprawdź czy to król
    if not target_column:
        return selected_card.points == 13  # Król ma 13 punktów

    target_card = target_column[-1]

    if target_card is None or selected_card is None:
        return False

    # Skip if target_card is the same as selected_card
    if selected_card == target_card:
        target_card = gsetup.bugfix_previous_card
    else:
        gsetup.bugfix_previous_card = target_card

    # Ruch z foundation stack na stos dolny
    if selected_card in [area['card'] for area in gsetup.upper_stack_areas]:
        return (
            target_card.points == selected_card.points + 1 and
            ((target_card.color == "red" and selected_card.color == "black") or
             (target_card.color == "black" and selected_card.color == "red"))
        )

    # Standardowy ruch między kolumnami
    return (selected_card.points == target_card.points - 1 and
            ((selected_card.color == "red" and target_card.color == "black") or
             (selected_card.color == "black" and target_card.color == "red")))




def recycle_stock_waste(gsetup):
    # Przenoszenie kart z powrotem do stosu dobieralnego
    if gsetup.stock_waste:
        #print("TEST BUGA 2 ", gsetup.stock_waste)
        while gsetup.stock_waste:
            card = gsetup.stock_waste.pop()
            #print(f"card popped {card}")
            if any(card in area['stack'] for area in gsetup.upper_stack_areas):
                continue
            card.hide()  # Zakrywanie kart
            gsetup.stock_pile.append(card)

            # Usunięcie etykiety karty z interfejsu użytkownika
            for label in gsetup.card_labels[:]:
                if label.card_object == card:
                    gsetup.card_labels.remove(label)
                    label.place_forget()
                    break

        # Ukrywanie przycisku po przeniesieniu kart
        if hasattr(gsetup, 'restore_button'):
            gsetup.restore_button.place_forget()
            del gsetup.restore_button

        # Odświeżenie stosu kart
        gsetup.game_ui.display_stock_pile(gsetup.wyjebane)
        gsetup.game_ui.update_score(-50)
        #print("Recycled stock waste back to stock pile.")

def place_in_column(gsetup, x, y):
    # TODO: Umieszcza kartę w odpowiedniej kolumnie po wykonaniu ruchu.
    pass

def remove_card_from_column(gsetup, card):
    # Znajdź i usuń kartę z odpowiedniej kolumny
    for col_index, column in enumerate(gsetup.columns):
        if card in column:
            column.remove(card)  # Usuń kartę z kolumny
            #print(f"Karta {card.figure} usunięta z kolumny {col_index + 1}")
            break
    else:
        pass
        #print(f"Karta {card.figure} nie została znaleziona w żadnej kolumnie.")

    # Usuń kartę z logiki pozycji
    gsetup.card_positions = [
        pos for pos in gsetup.card_positions if pos['card'] != card
    ]
    #print(f"Pozycja karty {card.figure} usunięta z logiki pozycji.")

    # Debugowanie - wyświetlenie aktualnego stanu kolumn
    #print(f"Aktualny stan kolumn: {[len(col) for col in gsetup.columns]}")



def remove_card_from_positions(gsetup, card):
    gsetup.card_positions = [
        pos for pos in gsetup.card_positions if pos['card'] != card
    ]
    #print(f"Pozycja karty {card.figure} usunięta z logiki pozycji.")

def is_valid_upper_stack_move(card, area):
    # Sprawdza, czy karta pasuje do koloru i kolejności
    if card.figure.split(' ')[-1] != area['suit']:
        return False
    if not area['stack']:
        return card.points == 1  # Tylko asy mogą zaczynać stos
    return card.points == area['stack'][-1].points + 1


def is_game_won(gsetup):
    #print("END GAME DEBUG Ilosc kart w stock_pile: ", len(gsetup.stock_pile))
    #print("END GAME DEBUG Ilosc kart w stock_waste: ", len(gsetup.stock_waste))
    lista = []
    for col in gsetup.columns:
        smalllist = []
        if len(col) == 0:
            smalllist.append(True)
        else:
            for card in col:
                if card.revealed:
                    smalllist.append(True)
                else:
                    smalllist.append(False)
        lista.append(smalllist)

    #print("END GAME DEBUG lista", lista)
    #print("END GAME DEBUG Check", list(map(lambda x: isinstance(x, type(None)) or all(x), lista)))
    # if len(gsetup.stock_pile) == 0 and len(gsetup.stock_waste) == 0 and all(
    #         map(lambda x: isinstance(x, type(None)) or all(x), lista)):
    #     print("WYGRANA !!!")


def is_game_won(gsetup):
    #IF DO TESTOW
    # if gsetup.game_ui.score >= 15:
    #     return True
    #print("END GAME DEBUG Ilosc kart w stock_pile: ", len(gsetup.stock_pile))
    #print("END GAME DEBUG Ilosc kart w stock_waste: ", len(gsetup.stock_waste))
    lista = []
    for col in gsetup.columns:
        smalllist = []
        if len(col) == 0:
            smalllist.append(True)
        else:
            for card in col:
                if card.revealed:
                    smalllist.append(True)
                elif card is None:
                    smalllist.append(True)
                else:
                    smalllist.append(False)
        lista.append(smalllist)

    if len(gsetup.stock_pile) == 0 and len(gsetup.stock_waste) == 0 and all(
            map(lambda x: isinstance(x, type(None)) or all(x), lista)):
        return True
    else:
        return False





def get_highscore():
    import psycopg2
    try:
        #("Start connecting...")
        connection = psycopg2.connect(
            host="195.150.230.208",
            port="5432",
            user="2024_jop_kamil",
            password="pedofil",
            database="2024_jop_kamil"
        )
        #print("Connected successfully!")

        cursor = connection.cursor()
        cursor.execute('''
                        SELECT nickname,score 
                        FROM player
                        ORDER BY score DESC''')
        results = cursor.fetchall()

        connection.close()
        #print("Connection closed.")
        #print(results)
        return results

    except psycopg2.Error as e:
        pass
        #print("Database error:", e)


def add_highscore(nick, points):
    import psycopg2
    try:
        #print("Connecting to the database...")
        connection = psycopg2.connect(
            host="195.150.230.208",
            port="5432",
            user="2024_jop_kamil",
            password="pedofil",
            database="2024_jop_kamil"
        )
        #print("Connected successfully!")

        cursor = connection.cursor()
        # Use parameterized query to prevent SQL injection
        query = "INSERT INTO player (nickname, score) VALUES (%s, %s);"
        cursor.execute(query, (nick, points))

        # Commit the transaction
        connection.commit()
        #print("Highscore added successfully!")

    except psycopg2.Error as e:
        pass
        #print("Database error:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("Connection closed.")
