import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from gameUI import  GameUI
import gameUI
from cardDeck import CardDeck
from firstDeal import FirstDeal
import  gameEvents
class GameSetup:
    def __init__(self, window):
        # Inicjalizuje grę, okno oraz talię kart.
        self.window = window
        self.card_labels = []
        self.deck = CardDeck()
        self.card_positions = []
        self.stock_pile = []
        self.stock_waste = []
        self.selected_card = None
        self.game_ui = GameUI(self)
        self.columns = [[] for _ in range(7)]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(script_dir, 'resources')
        self.cards_dir = os.path.join(self.resources_dir, 'cards')
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
        print("zresetowano gre")
    # Usunięcie wszystkich kart z planszy
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()
        self.deck = CardDeck()
        self.deck.shuffle_deck()
        self.first_deal = FirstDeal(self.deck)
        self.stock_pile = self.deck.cards[28:]
        self.stock_waste = []

        columns = self.first_deal.setup_initial_layout()
        self.columns = columns  # Przechowywanie kolumn
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
                f"Znaleziono błędy:\n{'\n'.join(errors)}\nCzy chcesz kontynuować mimo to?"
            )
            if not ignore:
                return

        self.game_ui = gameUI.GameUI(self)
        self.game_ui.display_initial_deal(columns)
        self.game_ui.display_stock_pile()

        self.update_lower_stack_areas()

        self.game_ui.start_timer()

    def update_lower_stack_areas(self):
        # Definicja stałych miejsc na dole (placeholdery)
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
        # Odkrywa kartę, która znajduje się bezpośrednio pod ostatnią odkrytą kartą.
        if source_column:
            previous_card = source_column[-1]
            previous_card.reveal()
            card_label = next(label for label in self.card_labels if label.card_object == previous_card)
            card_image_path = os.path.join(self.cards_dir, os.path.basename(previous_card.get_image()))
            card_image = Image.open(card_image_path).resize((100, 145))
            card_photo = ImageTk.PhotoImage(card_image)
            card_label.config(image=card_photo)
            card_label.image = card_photo  # Zapisanie referencji do obrazu, aby nie został usunięty przez GC






