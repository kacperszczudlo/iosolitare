import os
from card import Card

class CardDeck:
    def __init__(self, cards_path):
        # Inicjalizuje talię kart.
        self.cards = []
        self.cards_path = cards_path
        self.init_deck()

    def init_deck(self):
        # Tworzy pełną talię 52 kart (4 kolory po 13 figur).
        figures = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for idx, figure in enumerate(figures):
                points = idx + 1 if idx < 13 else 13
                front_image = os.path.join(self.cards_path, f"{figure}_of_{suit}.png")
                back_image = os.path.join(self.cards_path, "behind.png")
                if not os.path.exists(front_image) or not os.path.exists(back_image):
                    #print(f"Image not found for {figure} of {suit}")
                    continue
                card = Card(points, f"{figure} of {suit}", front_image, back_image)
                self.cards.append(card)
                #print(f"Initialized card: {card.figure}")

    def shuffle_deck(self):
        # Miesza karty w talii.
        from random import shuffle
        shuffle(self.cards)

    def deal_cards(self, columns):
        # Rozdaje karty do podanej liczby kolumn.
        dealt_columns = [[] for _ in range(columns)]
        for idx, card in enumerate(self.cards):
            dealt_columns[idx % columns].append(card)
            #print(f"Dealt card: {card.figure} to column {idx % columns + 1}")
        return dealt_columns
