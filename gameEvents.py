from gameLogic import *
def on_card_click(gsetup, event):
    # Obsługuje kliknięcie na kartę (zapamiętuje jej pozycję, jeśli jest odkryta).
    gsetup.selected_card = event.widget.card_object
    gsetup.start_x = event.widget.winfo_x()
    gsetup.start_y = event.widget.winfo_y()
    gsetup.original_x = event.widget.winfo_x()
    gsetup.original_y = event.widget.winfo_y()

    # To jest używane do odkładania karty
    gsetup.start_offset_x = event.x
    gsetup.start_offset_y = event.y
    # if gsetup.selected_card and gsetup.selected_card.revealed:
    #     # Usuń kartę z logicznego stosu
    #     for column in gsetup.columns:
    #         if gsetup.selected_card in column:
    #             column.remove(gsetup.selected_card)
    #             break
    if not gsetup.selected_card.revealed:
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
                target_column_index = get_column_index(gsetup,target_card)

                if target_card.revealed:
                    # Jeśli ruch jest poprawny podświetl na zielono
                    if target_column_index is not None and is_valid_move(gsetup,gsetup.selected_card,
                                                                                target_column_index):
                        gsetup.game_ui.highlight_card(event.widget, "green")
                        overlap_detected = True
                        break
                    # Jeśli ruch jest błedny podświetl na czerwono
                    elif target_column_index is not None and not is_valid_move(gsetup,gsetup.selected_card,
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
        for col_index, column in enumerate(gsetup.columns):
            if column:
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
            else:
                placeholder_area = gsetup.lower_stack_areas[col_index]
                if rectangles_overlap(
                        {'x': card_x, 'y': card_y, 'width': 100, 'height': 145},
                        placeholder_area
                ):
                    target_column = col_index
                    break

        if target_column is not None:
            if is_valid_move(gsetup, gsetup.selected_card, target_column):
                gsetup.columns[target_column].append(gsetup.selected_card)
                new_position = gsetup.lower_stack_areas[target_column]['y'] + (len(gsetup.columns[target_column]) - 1) * 30
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






