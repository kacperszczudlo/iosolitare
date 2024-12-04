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
            {'x': 550, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'hearts'},
            {'x': 690, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'diamonds'},
            {'x': 830, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'clubs'},
            {'x': 970, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'spades'},
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

        columns = self.first_deal.setup_initial_layout()
        self.columns = columns  # Przechowywanie kolumn
        self.card_positions = []

        self.upper_stack_areas = [
            {'x': 550, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'hearts'},
            {'x': 690, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'diamonds'},
            {'x': 830, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'clubs'},
            {'x': 970, 'y': 153, 'width': 100, 'height': 145, 'card': None, 'suit': 'spades'},
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

