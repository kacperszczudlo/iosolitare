from tkinter import Button
from functools import partial
from gameLogic import *
def on_card_click(gsetup, event):
    if is_game_won(gsetup):
        award_points_for_lower_columns(gsetup)
        gsetup.game_ui.show_centered_box()
    card = event.widget.card_object
    if not card.revealed:
        return
    # Karta na foundation
    for area in gsetup.upper_stack_areas:
        if area['card'] == card:
            gsetup.start_x = event.widget.winfo_x()
            gsetup.start_y = event.widget.winfo_y()
            gsetup.original_x = gsetup.start_x
            gsetup.original_y = gsetup.start_y
            gsetup.start_offset_x = event.x
            gsetup.start_offset_y = event.y
            gsetup.moving_cards = [card]
            print(f"Selected card {card.figure} from foundation stack ({area['suit']}).")
            return

    # Karta w kolumnie lub stock_waste
    for column in gsetup.columns:
        if card in column:
            card_index = column.index(card)
            gsetup.start_x = event.widget.winfo_x()
            gsetup.start_y = event.widget.winfo_y()
            gsetup.original_x = gsetup.start_x
            gsetup.original_y = gsetup.start_y
            gsetup.start_offset_x = event.x
            gsetup.start_offset_y = event.y
            gsetup.moving_cards = column[card_index:]
            print(f"Selected card {card.figure} from column {gsetup.columns.index(column) + 1}.")
            return

    if card in gsetup.stock_waste:
        gsetup.start_x = event.widget.winfo_x()
        gsetup.start_y = event.widget.winfo_y()
        gsetup.original_x = gsetup.start_x
        gsetup.original_y = gsetup.start_y
        gsetup.start_offset_x = event.x
        gsetup.start_offset_y = event.y
        gsetup.moving_cards = [card]
        print(f"Selected card {card.figure} from stock waste.")


def on_card_drag(gsetup, event):
    target_column_index = None
    if gsetup.selected_card is None:
        try:
            gsetup.selected_card = next(label.card_object for label in gsetup.card_labels if label == event.widget)
        except StopIteration:
            gsetup.selected_card = None
            return
    if gsetup.selected_card:
        for i, card in enumerate(gsetup.moving_cards):
            card_label = next(label for label in gsetup.card_labels if label.card_object == card)
            card_label.lift()  # Bring the card to the top

        delta_x = event.x - gsetup.start_offset_x
        delta_y = event.y - gsetup.start_offset_y

        for i, card in enumerate(gsetup.moving_cards):
            card_label = next(label for label in gsetup.card_labels if label.card_object == card)
            card_label.place(x=gsetup.start_x + delta_x, y=gsetup.start_y + delta_y + i * 30)

        gsetup.start_x += delta_x
        gsetup.start_y += delta_y

        overlap_detected = False

        for label in gsetup.card_labels:
            if label != event.widget and rectangles_overlap(
                    {'x': gsetup.start_x, 'y': gsetup.start_y, 'width': 100, 'height': 145 + 30*(len(gsetup.moving_cards)-1)},
                    {'x': label.winfo_x(), 'y': label.winfo_y(), 'width': 100, 'height': 145}):
                target_card = label.card_object
                if target_column_index == None:
                    target_column_index = get_column_index(gsetup, target_card)

                if target_card.revealed:
                    if target_column_index is not None and is_valid_move(gsetup, gsetup.selected_card, target_column_index):
                        for card in gsetup.moving_cards:
                            c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                            gsetup.game_ui.highlight_card(c_label, "green")
                        overlap_detected = True
                        break
                    elif target_column_index is not None:
                        for card in gsetup.moving_cards:
                            c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                            gsetup.game_ui.highlight_card(c_label, "red")
                        overlap_detected = True
                        break

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
            for card in gsetup.moving_cards:
                c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                gsetup.game_ui.highlight_card(c_label, "black")
        # print(f"Dragging card: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")


def on_card_release(gsetup, event):
    if gsetup.selected_card:
        card_x = event.widget.winfo_x()
        card_y = event.widget.winfo_y()

        target_column = None
        valid_move = False

        # Foundation
        for area in gsetup.upper_stack_areas:
            if rectangles_overlap({'x': card_x, 'y': card_y, 'width': 100, 'height': 145}, area):
                if is_valid_upper_stack_move(gsetup.selected_card, area):
                    # Zapis stanu PRZED zmianą
                    gsetup.save_game_state()

                    gsetup.move_counter += 1
                    gsetup.game_ui.update_move_counter(gsetup.move_counter)

                    source_column = next((col for col in gsetup.columns if gsetup.selected_card in col), None)
                    if source_column:
                        source_column.remove(gsetup.selected_card)
                        if len(source_column) > 0:
                            gsetup.reveal_previous_card(source_column)
                            gsetup.game_ui.update_score(5)
                        else:
                            col_index = gsetup.columns.index(source_column)
                            print(f"Column {col_index+1} is now empty.")
                    elif gsetup.selected_card in gsetup.stock_waste:
                        gsetup.stock_waste.remove(gsetup.selected_card)
                        gsetup.wyjebane.append(gsetup.selected_card)

                    area['stack'].append(gsetup.selected_card)
                    area['card'] = gsetup.selected_card

                    event.widget.place(x=area['x'], y=area['y'])
                    event.widget.lift()
                    if is_game_won(gsetup):
                        award_points_for_lower_columns(gsetup)
                        gsetup.game_ui.show_centered_box()
                    print(f"Moved card {gsetup.selected_card.figure} to foundation stack ({area['suit']}).")
                    valid_move = True
                    gsetup.game_ui.update_score(10)
                    gsetup.game_ui.play_card_place_sound()  # Dodaj wywołanie funkcji dźwięku
                    print("Current state of all foundation stacks:")
                    for idx, stack_area in enumerate(gsetup.upper_stack_areas, start=1):
                        stack_cards = [c.figure for c in stack_area['stack']]
                        print(f"Foundation stack {idx} ({stack_area['suit']}): {stack_cards}")

                break

        if valid_move:
            gsetup.moving_cards = []
            gsetup.game_ui.remove_highlight(event.widget)
            gsetup.selected_card = None
            return

        # Karta z foundation wyciągnięta i niepoprawnie położona
        for area in gsetup.upper_stack_areas:
            if gsetup.selected_card in area['stack']:
                area['stack'].remove(gsetup.selected_card)
                if len(area['stack']) > 0:
                    area['card'] = area['stack'][-1]
                else:
                    area['card'] = None

                if not valid_move:
                    event.widget.place(x=area['x'], y=area['y'])
                    print(f"Invalid move: {gsetup.selected_card.figure} from foundation stack ({area['suit']}).")
                    gsetup.selected_card = None
                    gsetup.moving_cards = []
                    return
                break

        # Docelowa kolumna
        for col_index, column in enumerate(gsetup.columns):
            if not column:
                placeholder_area = gsetup.lower_stack_areas[col_index]
                if rectangles_overlap({'x': card_x, 'y': card_y, 'width':100, 'height':145}, placeholder_area):
                    target_column = col_index
                    break
            else:
                last_card = column[-1]
                last_card_position = next((pos for pos in gsetup.card_positions if pos['card']==last_card), None)
                if last_card_position and rectangles_overlap(
                    {'x': card_x, 'y': card_y, 'width':100,'height':145}, last_card_position):
                    target_column = col_index
                    break
        # print(f"DEBUG TARGET COLUMN: {target_column} ")
        if target_column is not None:
            if is_valid_move(gsetup, gsetup.selected_card, target_column):
                # Zapis stanu PRZED zmianą, bo ruch jest poprawny
                gsetup.save_game_state()

                gsetup.move_counter += 1
                gsetup.game_ui.update_move_counter(gsetup.move_counter)

                source_column = next((column for column in gsetup.columns if gsetup.selected_card in column), None)
                if source_column:
                    for card in gsetup.moving_cards:
                        source_column.remove(card)
                elif gsetup.selected_card in gsetup.stock_waste:
                    # print(f"TEST BUGA1 {gsetup.selected_card}")
                    gsetup.stock_waste.remove(gsetup.selected_card)
                    gsetup.wyjebane.append(gsetup.selected_card)
                    # gsetup.deck.cards.remove(gsetup.selected_card)
                    print(gsetup.stock_waste)
                gsetup.columns[target_column].extend(gsetup.moving_cards)
                for i, card in enumerate(gsetup.moving_cards):
                    card_label = next(l for l in gsetup.card_labels if l.card_object == card)
                    card_label.place(
                        x=gsetup.lower_stack_areas[target_column]['x'],
                        y=gsetup.lower_stack_areas[target_column]['y'] +
                          (len(gsetup.columns[target_column]) - len(gsetup.moving_cards)) * 30 + i * 30
                    )
                    card_label.lift()

                if source_column and len(source_column) > 0:
                    gsetup.reveal_previous_card(source_column)
                    gsetup.game_ui.update_score(5)

                for card in gsetup.moving_cards:
                    c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                    gsetup.game_ui.remove_highlight(c_label)

                gsetup.moving_cards = []

                if gsetup.selected_card in gsetup.stock_waste:
                    gsetup.stock_waste.remove(gsetup.selected_card)
                    gsetup.wyjebane.append(gsetup.selected_card)
                if gsetup.selected_card.foundation:
                    gsetup.game_ui.update_score(-15)
                else:
                    if gsetup.selected_card.moved:
                        gsetup.game_ui.update_score(-1)
                    else:
                        gsetup.game_ui.update_score(5)
                        gsetup.selected_card.moved = True
                if is_game_won(gsetup):
                    award_points_for_lower_columns(gsetup)
                    gsetup.game_ui.show_centered_box()
                print(f"Placed card: {gsetup.selected_card.figure} of {gsetup.selected_card.suit} in column {target_column+1}")
                print(f"Current state of columns: {[len(col) for col in gsetup.columns]}")
                gsetup.game_ui.play_card_place_sound()  # Dodaj wywołanie funkcji dźwięku
            else:
                # Ruch niepoprawny
                for i, card in enumerate(gsetup.moving_cards):
                    c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                    c_label.place(x=gsetup.original_x, y=gsetup.original_y + i * 30)
                    gsetup.game_ui.remove_highlight(c_label)

                print(f"Invalid move: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")
        else:
            # Brak docelowej kolumny
            for i, card in enumerate(gsetup.moving_cards):
                c_label = next(l for l in gsetup.card_labels if l.card_object == card)
                c_label.place(x=gsetup.original_x, y=gsetup.original_y + i * 30)
                gsetup.game_ui.remove_highlight(c_label)

            print(f"No valid target column for: {gsetup.selected_card.figure} of {gsetup.selected_card.suit}")

        update_card_position(gsetup, gsetup.selected_card, card_x, card_y)
        gsetup.selected_card = None
        gsetup.moving_cards = []
        gsetup.game_ui.remove_highlight(event.widget)



def on_stock_pile_click(gsetup, event):
    if gsetup.stock_pile:
        # Ruch poprawny - zapis stanu PRZED dobraniem karty
        gsetup.save_game_state()

        gsetup.move_counter += 1
        gsetup.game_ui.update_move_counter(gsetup.move_counter)

        card = gsetup.stock_pile.pop()
        card.reveal()
        gsetup.stock_waste.append(card)

        # Najpierw usuń starą etykietę zakrytej karty
        for label in gsetup.card_labels[:]:
            if label.card_object == card:
                gsetup.card_labels.remove(label)
                label.place_forget()
                break

        waste_x = 270
        waste_y = 153
        card_label = gsetup.game_ui.create_card(waste_x, waste_y, card)
        gsetup.card_labels.append(card_label)

        card_label.bind("<ButtonPress-1>", partial(on_card_click, gsetup))
        card_label.bind("<B1-Motion>", partial(on_card_drag, gsetup))
        card_label.bind("<ButtonRelease-1>", partial(on_card_release, gsetup))
        # card_label.bind("<Double-1>", partial(on_card_double_click, gsetup))

        if len(gsetup.stock_pile) == 0:
            if not hasattr(gsetup, 'restore_button'):
                gsetup.restore_button = Button(
                    gsetup.window,
                    command=lambda: recycle_stock_waste(gsetup),
                    bg="#919191",
                    bd=0
                )
                gsetup.restore_button.place(x=130, y=153, width=101, height=145)

        print(f"Drew card: {card.figure} of {card.suit}")

    elif gsetup.stock_waste:
        recycle_stock_waste(gsetup)

#
# def on_card_double_click(gsetup, event):
#     card = event.widget.card_object
#     if not card.revealed:
#         return
#
#     card_suit = card.figure.split(' ')[-1]
#
#     for i, area in enumerate(gsetup.upper_stack_areas):
#         if area['suit'] == card_suit:
#             # As na pusty foundation
#             if not area['stack'] and card.points == 1:
#                 # Ruch poprawny
#                 gsetup.save_game_state()
#
#                 gsetup.move_counter += 1
#                 gsetup.game_ui.update_move_counter(gsetup.move_counter)
#
#                 area['stack'].append(card)
#                 area['card'] = card
#                 event.widget.place(x=area['x'], y=area['y'])
#                 event.widget.lift()
#
#                 source_column = next((column for column in gsetup.columns if card in column), None)
#                 if source_column:
#                     source_column.remove(card)
#                     if len(source_column) > 0:
#                         gsetup.reveal_previous_card(source_column)
#                         gsetup.game_ui.update_score(5)
#                     else:
#                         col_index = gsetup.columns.index(source_column)
#                         print(f"Column {col_index + 1} is now empty.")
#                 elif card in gsetup.stock_waste:
#                     gsetup.stock_waste.remove(gsetup.selected_card)
#                     gsetup.wyjebane.append(gsetup.selected_card)
#
#                 gsetup.game_ui.update_score(10)
#                 card.foundation = True
#                 if is_game_won(gsetup):
#                     gsetup.game_ui.show_centered_box()
#                 print(f"Moved card {card.figure} to foundation stack ({area['suit']}).")
#
#                 print("Current state of all foundation stacks:")
#                 for idx, stack_area in enumerate(gsetup.upper_stack_areas, start=1):
#                     stack_cards = [c.figure for c in stack_area['stack']]
#                     print(f"Foundation stack {idx} ({stack_area['suit']}): {stack_cards}")
#                 return
#
#             # Kolejna karta na foundation
#             elif area['stack'] and area['card'].points == card.points - 1:
#                 gsetup.save_game_state()
#
#                 gsetup.move_counter += 1
#                 gsetup.game_ui.update_move_counter(gsetup.move_counter)
#
#                 area['stack'].append(card)
#                 area['card'] = card
#                 event.widget.place(x=area['x'], y=area['y'])
#                 event.widget.lift()
#
#                 source_column = next((column for column in gsetup.columns if card in column), None)
#                 if source_column:
#                     source_column.remove(card)
#                     if len(source_column) > 0:
#                         gsetup.reveal_previous_card(source_column)
#                         gsetup.game_ui.update_score(5)
#                     else:
#                         col_index = gsetup.columns.index(source_column)
#                         print(f"Column {col_index + 1} is now empty.")
#                 elif card in gsetup.stock_waste:
#                     gsetup.stock_waste.remove(gsetup.selected_card)
#                     gsetup.wyjebane.append(gsetup.selected_card)
#                 gsetup.game_ui.update_score(10)
#                 if is_game_won(gsetup):
#                     gsetup.game_ui.show_centered_box()
#                 print(f"Moved card {card.figure} to foundation stack ({area['suit']}).")
#
#                 print("Current state of all foundation stacks:")
#                 for idx, stack_area in enumerate(gsetup.upper_stack_areas, start=1):
#                     stack_cards = [c.figure for c in stack_area['stack']]
#                     print(f"Foundation stack {idx} ({stack_area['suit']}): {stack_cards}")
#                 return
#
#     # Ruch niepoprawny - nie zapisujemy stanu
#     print(f"Cannot move card {card.figure} to any foundation stack.")

def award_points_for_lower_columns(gsetup):
    total_cards = sum(len(column) for column in gsetup.columns)
    points_to_add = total_cards * 10
    gsetup.game_ui.update_score(points_to_add)
