import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from gameUI import GameUI
from cardDeck import CardDeck
from firstDeal import FirstDeal
import gameEvents
import copy

class GameSetup:
    def __init__(self, window, resources_dir, cards_dir, app):
        self.resources_dir = resources_dir
        self.cards_dir = cards_dir
        self.app = app
        self.bugfix_previous_card = None
        self.previous_state = None
        self.window = window
        self.card_labels = []
        self.deck = CardDeck(self.cards_dir)
        self.card_positions = []
        self.stock_pile = []
        self.stock_waste = []
        self.move_counter = 0
        self.selected_card = None
        self.game_ui = GameUI(self)
        self.wyjebane = []
        self.columns = [[] for _ in range(7)]

        self.lower_stack_areas = [
            {'x': 130, 'y': 378, 'width': 100, 'height': 145},
            {'x': 270, 'y': 378, 'width': 100, 'height': 145},
            {'x': 410, 'y': 378, 'width': 100, 'height': 145},
            {'x': 550, 'y': 378, 'width': 100, 'height': 145},
            {'x': 690, 'y': 378, 'width': 100, 'height': 145},
            {'x': 830, 'y': 378, 'width': 100, 'height': 145},
            {'x': 970, 'y': 378, 'width': 100, 'height': 145},
        ]
        self.upper_stack_areas = [
            {'x': 550, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'hearts', 'stack': []},
            {'x': 690, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'diamonds', 'stack': []},
            {'x': 830, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'clubs', 'stack': []},
            {'x': 970, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'spades', 'stack': []},
        ]

    def reset_game(self):
        #print("zresetowano gre")
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()
        self.deck = CardDeck(self.cards_dir)
        self.deck.shuffle_deck()
        self.first_deal = FirstDeal(self.deck)
        self.stock_pile = self.deck.cards[28:]
        self.stock_waste = []
        self.move_counter = 0

        columns = self.first_deal.setup_initial_layout()
        self.columns = columns
        self.card_positions = []

        self.upper_stack_areas = [
            {'x': 550, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'hearts', 'stack': []},
            {'x': 690, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'diamonds', 'stack': []},
            {'x': 830, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'clubs', 'stack': []},
            {'x': 970, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'spades', 'stack': []},
        ]
        errors = self.first_deal.validate_initial_layout()

        if errors:
            ignore = messagebox.askyesno(
                "Błąd układu początkowego",
                f"Znaleziono błędy:\n{', '.join(errors)}\nCzy chcesz kontynuować mimo to?"
            )
            if not ignore:
                return

        self.game_ui = GameUI(self)
        self.game_ui.display_initial_deal(columns)
        self.game_ui.display_stock_pile()
        self.game_ui.won = False

        self.update_lower_stack_areas()
        self.game_ui.init_score()
        self.game_ui.start_timer()
        self.game_ui.update_move_counter(self.move_counter)
        self.save_game_state()

    def update_lower_stack_areas(self):
        placeholder_positions = [
            {'x': 130, 'y': 378, 'width': 100, 'height': 145},
            {'x': 270, 'y': 378, 'width': 100, 'height': 145},
            {'x': 410, 'y': 378, 'width': 100, 'height': 145},
            {'x': 550, 'y': 378, 'width': 100, 'height': 145},
            {'x': 690, 'y': 378, 'width': 100, 'height': 145},
            {'x': 830, 'y': 378, 'width': 100, 'height': 145},
            {'x': 970, 'y': 378, 'width': 100, 'height': 145},
        ]

        self.lower_stack_areas = placeholder_positions

        for position in self.card_positions:
            area = {
                'x': position['x'],
                'y': position['y'],
                'width': position['width'],
                'height': position['height'],
                'card': position['card']
            }
            self.lower_stack_areas.append(area)

    def reveal_previous_card(self, source_column):
        if source_column:
            previous_card = source_column[-1]
            previous_card.reveal()
            card_label = next(label for label in self.card_labels if label.card_object == previous_card)
            card_image_path = os.path.join(self.cards_dir, os.path.basename(previous_card.get_image()))
            card_image = Image.open(card_image_path).resize((100, 145))
            card_photo = ImageTk.PhotoImage(card_image)
            card_label.config(image=card_photo)
            card_label.image = card_photo

    def save_game_state(self, points_added=0):
        current_state = self.get_current_state()

        if self.previous_state is None or self.previous_state.get('state') != current_state:
            #print("Zapisuję nowy stan gry...")
            self.previous_state = {
                'state': current_state,
                'points_added': points_added,  # Punkty dodane w ruchu
                'current_score': self.game_ui.score  # Aktualny wynik
            }
        else:
            pass
            #("Stan gry nie zmienił się. Pomijam zapis.")




    def restore_game_state(self):
        if self.previous_state is not None:
            #print("Przywracam stan gry z restore_game_state...")

            # Przywrócenie stanu gry
            self.columns = copy.deepcopy(self.previous_state['state']['columns'])
            self.stock_pile = copy.deepcopy(self.previous_state['state']['stock_pile'])
            self.stock_waste = copy.deepcopy(self.previous_state['state']['stock_waste'])
            self.upper_stack_areas = copy.deepcopy(self.previous_state['state']['upper_stack_areas'])
            self.card_positions = copy.deepcopy(self.previous_state['state']['card_positions'])

            # Usunięcie podświetlenia
            for label in self.card_labels:
                self.game_ui.remove_highlight(label)

            # Przywrócenie wyniku
            restored_score = self.previous_state.get('current_score', self.game_ui.score)
            self.game_ui.update_score(restored_score - self.game_ui.score)
            #print(f"Przywrócono wynik: {restored_score}")

            # Odświeżenie UI
            self.refresh_ui_after_restore()

            # Wyczyszczenie poprzedniego stanu
            self.previous_state = None
        else:
            #print("Brak stanu do przywrócenia.")
            pass






    def refresh_ui_after_restore(self):
        for label in self.card_labels:
            label.place_forget()
            self.game_ui.remove_highlight(label)  # Usuń podświetlenie
        self.card_labels.clear()

        from gameUI import GameUI
        from functools import partial
        import gameEvents
        from gameLogic import update_card_position

        self.selected_card = None
        self.moving_cards = []

        # Placeholdery
        for x, y in [
            (130, 153), (270, 153),
            (130, 378), (270, 378), (410, 378), (550, 378), (690, 378), (830, 378), (970, 378)
        ]:
            self.game_ui.create_placeholder(x, y)

        y_offset = 378
        y_spacing = 30

        # Odtwarzanie kolumn
        for col_index, column in enumerate(self.columns):
            x_position = 131 + col_index * 140
            for row, card in enumerate(column):
                card_label = self.game_ui.create_card(x_position, y_offset + row * y_spacing, card)
                card_label.bind("<ButtonPress-1>", partial(gameEvents.on_card_click, self))
                card_label.bind("<B1-Motion>", partial(gameEvents.on_card_drag, self))
                card_label.bind("<ButtonRelease-1>", partial(gameEvents.on_card_release, self))
                self.card_labels.append(card_label)
                update_card_position(self, card, x_position, y_offset + row * y_spacing)

        # stock_pile
        stock_pile_x, stock_pile_y = 131, 153
        for card in self.stock_pile:
            card_label = self.game_ui.create_card(stock_pile_x, stock_pile_y, card)
            card_label.bind("<Button-1>", partial(gameEvents.on_stock_pile_click, self))
            self.card_labels.append(card_label)
            update_card_position(self, card, stock_pile_x, stock_pile_y)

        # stock_waste
        waste_x, waste_y = 270, 153
        for card in self.stock_waste:
            card_label = self.game_ui.create_card(waste_x, waste_y, card)
            card_label.bind("<ButtonPress-1>", partial(gameEvents.on_card_click, self))
            card_label.bind("<B1-Motion>", partial(gameEvents.on_card_drag, self))
            card_label.bind("<ButtonRelease-1>", partial(gameEvents.on_card_release, self))
            self.card_labels.append(card_label)
            update_card_position(self, card, waste_x, waste_y)

        # Foundation
        for area in self.upper_stack_areas:
            if area['stack']:
                top_card = area['stack'][-1]
                card_label = self.game_ui.create_card(area['x'], area['y'], top_card)
                card_label.bind("<ButtonPress-1>", partial(gameEvents.on_card_click, self))
                card_label.bind("<B1-Motion>", partial(gameEvents.on_card_drag, self))
                card_label.bind("<ButtonRelease-1>", partial(gameEvents.on_card_release, self))
                self.card_labels.append(card_label)
                update_card_position(self, top_card, area['x'], area['y'])




    def undo_move(self):
        if self.previous_state is not None:
            #print("Przywracam stan gry z undo_move...")
            self.restore_game_state()
            #print("Cofnięto ostatni ruch.")
        else:
            #print("Brak ruchu do cofnięcia.")
            pass

    def get_current_state(self):
        return {
            'columns': copy.deepcopy(self.columns),
            'stock_pile': copy.deepcopy(self.stock_pile),
            'stock_waste': copy.deepcopy(self.stock_waste),
            'upper_stack_areas': copy.deepcopy(self.upper_stack_areas),
            'card_positions': copy.deepcopy(self.card_positions),
        }
