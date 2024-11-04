from card import Card

class CardDeck:
    def __init__(self):
        self.cards = []
        self.init_deck()

    def init_deck(self):
        figures = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for idx, figure in enumerate(figures):
                points = idx + 1 if idx < 10 else 10
                front_image = f"resources/cards/{figure}_of_{suit}.png"
                back_image = "resources/cards/behind.png"
                card = Card(points, f"{figure} of {suit}", front_image, back_image)
                self.cards.append(card)

    def shuffle_deck(self):
        from random import shuffle
        shuffle(self.cards)

    def deal_cards(self, columns):
        dealt_columns = [[] for _ in range(columns)]
        for idx, card in enumerate(self.cards):
            dealt_columns[idx % columns].append(card)
        return dealt_columns