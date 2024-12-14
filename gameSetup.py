import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from gameUI import GameUI
import gameUI
from cardDeck import CardDeck
from firstDeal import FirstDeal
import gameEvents
import copy

class GameSetup:
    def __init__(self, window):
        self.previous_state = None
        self.window = window
        self.card_labels = []
        self.deck = CardDeck()
        self.card_positions = []
        self.stock_pile = []
        self.stock_waste = []
        self.move_counter = 0
        self.selected_card = None
        self.game_ui = GameUI(self)
        self.columns = [[] for _ in range(7)]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(script_dir, 'resources')
        self.cards_dir = os.path.join(self.resources_dir, 'cards')
        self.preloaded_images = self.preload_images()
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
        self.upper_stack_placeholders = []
        self.initialize_upper_stack_placeholders()

    def preload_images(self):
        preloaded = {}

        # Ładowanie obrazów kart
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for figure in ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']:
                card_name = f"{figure} of {suit}"  # Klucz w formacie używanym przez Card
                card_path = os.path.join(self.cards_dir, f"{figure}_of_{suit}.png")
                preloaded[card_name] = ImageTk.PhotoImage(Image.open(card_path).resize((100, 145)))

        # Ładowanie tyłu kart
        back_path = os.path.join(self.cards_dir, "behind.png")
        preloaded["behind"] = ImageTk.PhotoImage(Image.open(back_path).resize((100, 145)))

        # Ładowanie obrazów placeholderów z tłem
        background_path = os.path.join(self.resources_dir, 'background.jpg')
        background_image = Image.open(background_path).resize((100, 145)).convert("RGBA")

        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            placeholder_path = os.path.join(self.resources_dir, f'{suit}_placeholder.png')
            placeholder_image = Image.open(placeholder_path).resize((100, 145)).convert("RGBA")
            combined_image = Image.alpha_composite(background_image, placeholder_image)
            preloaded[f"{suit}_placeholder"] = ImageTk.PhotoImage(combined_image)

        # Placeholder ogólny
        general_placeholder_path = os.path.join(self.resources_dir, 'placeholder.png')
        placeholder_image = Image.open(general_placeholder_path).resize((100, 145)).convert("RGBA")
        combined_image = Image.alpha_composite(background_image, placeholder_image)
        preloaded["general_placeholder"] = ImageTk.PhotoImage(combined_image)

        print("Preładowano wszystkie obrazy, w tym placeholdery z tłem.")
        return preloaded

    def initialize_upper_stack_placeholders(self):
        for area in self.upper_stack_areas:
            suit = area['suit']
            placeholder_label = self.game_ui.create_placeholder(area['x'], area['y'], suit=suit)
            self.upper_stack_placeholders.append(placeholder_label)
            placeholder_label.place_forget()

    def reset_game(self):
        print("zresetowano gre")
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()
        self.deck = CardDeck()
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
        for i, area in enumerate(self.upper_stack_areas):
            placeholder_label = self.upper_stack_placeholders[i]
            placeholder_label.place(x=area['x'], y=area['y'])
            placeholder_label.lift()  # Wymuszenie na wierzchu
        errors = self.first_deal.validate_initial_layout()

        if errors:
            ignore = messagebox.askyesno(
                "Błąd układu początkowego",
                f"Znaleziono błędy:\n{'\n'.join(errors)}\nCzy chcesz kontynuować mimo to?"
            )
            if not ignore:
                return

        self.game_ui = gameUI.GameUI(self)
        self.game_ui.display_initial_deal(columns)
        self.game_ui.display_stock_pile()

        self.update_lower_stack_areas()
        self.game_ui.init_score()
        self.game_ui.start_timer()
        self.game_ui.update_move_counter(self.move_counter)

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
            card_image = self.preloaded_images[previous_card.figure]  # Zamiast ponownie otwierać obraz
            card_label.config(image=card_image)
            card_label.image = card_image

    def save_game_state(self):
        state = {
            'columns': copy.deepcopy(self.columns),
            'stock_pile': copy.deepcopy(self.stock_pile),
            'stock_waste': copy.deepcopy(self.stock_waste),
            'upper_stack_areas': copy.deepcopy(self.upper_stack_areas),
            'card_positions': copy.deepcopy(self.card_positions),
        }
        self.previous_state = state

    def restore_game_state(self):
        if self.previous_state is not None:
            self.columns = copy.deepcopy(self.previous_state['columns'])
            self.stock_pile = copy.deepcopy(self.previous_state['stock_pile'])
            self.stock_waste = copy.deepcopy(self.previous_state['stock_waste'])
            self.upper_stack_areas = copy.deepcopy(self.previous_state['upper_stack_areas'])
            self.card_positions = copy.deepcopy(self.previous_state['card_positions'])

            self.refresh_ui_after_restore()
            self.previous_state = None

    def refresh_ui_after_restore(self):
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()

        from gameUI import GameUI

        from functools import partial
        import gameEvents
        from gameLogic import update_card_position

        self.selected_card = None
        self.moving_cards = []

        self.game_ui = GameUI(self)
        # Górne stosy - użycie istniejących placeholderów
        for i, area in enumerate(self.upper_stack_areas):
            placeholder_label = self.upper_stack_placeholders[i]
            placeholder_label.place(x=area['x'], y=area['y'])
            placeholder_label.lift()  # Podnieś placeholder na wierzch

        # Dolne stosy - placeholdery dla pustych kolumn
        for area in self.lower_stack_areas:
            placeholder_label = self.game_ui.create_placeholder(area['x'], area['y'])
            placeholder_label.place(x=area['x'], y=area['y'])

        y_offset = 378
        y_spacing = 30

        all_cards = []
        for col in self.columns:
            all_cards.extend(col)
        all_cards.extend(self.stock_pile)
        all_cards.extend(self.stock_waste)
        for area in self.upper_stack_areas:
            if area['stack']:
                all_cards.extend(area['stack'])

        all_cards = list(set(all_cards))  # Usuwa duplikaty bez ręcznego iterowania


        # Kolumny
        for col_index, column in enumerate(self.columns):
            x_position = 131 + col_index * 140
            for row, card in enumerate(column):
                card_label = self.game_ui.create_card(x_position, y_offset + row * y_spacing, card)
                card_label.bind("<ButtonPress-1>", partial(gameEvents.on_card_click, self))
                card_label.bind("<B1-Motion>", partial(gameEvents.on_card_drag, self))
                card_label.bind("<ButtonRelease-1>", partial(gameEvents.on_card_release, self))
                card_label.bind("<Double-1>", partial(gameEvents.on_card_double_click, self))
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
            card_label.bind("<Double-1>", partial(gameEvents.on_card_double_click, self))
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
                card_label.bind("<Double-1>", partial(gameEvents.on_card_double_click, self))
                self.card_labels.append(card_label)
                update_card_position(self, top_card, area['x'], area['y'])

    def undo_move(self):
        if self.previous_state is not None:
            self.restore_game_state()
            print("Cofnięto ostatni ruch.")
        else:
            print("Brak ruchu do cofnięcia.")
