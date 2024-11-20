import os
from card import Card

class CardDeck:
    def __init__(self):
        # Inicjalizuje talię kart.
        self.cards = []
        self.init_deck()

    def init_deck(self):
        # Tworzy pełną talię 52 kart (4 kolory po 13 figur).
        figures = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cards_dir = os.path.join(script_dir, 'resources', 'cards')
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for idx, figure in enumerate(figures):
                points = idx + 1 if idx < 10 else 10
                front_image = os.path.join(cards_dir, f"{figure}_of_{suit}.png")
                back_image = os.path.join(cards_dir, "behind.png")
                card = Card(points, f"{figure} of {suit}", front_image, back_image)
                self.cards.append(card)

    def shuffle_deck(self):
        # Miesza karty w talii.
        from random import shuffle
        shuffle(self.cards)

    def deal_cards(self, columns):
        # Rozdaje karty do podanej liczby kolumn.
        dealt_columns = [[] for _ in range(columns)]
        for idx, card in enumerate(self.cards):
            dealt_columns[idx % columns].append(card)
        return dealt_columns
