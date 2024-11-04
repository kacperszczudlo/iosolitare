class FirstDeal:
    def __init__(self, deck):
        self.deck = deck
        self.columns = [[] for _ in range(7)]

    def setup_initial_layout(self):

        index = 0
        for col in range(7):
            for row in range(col + 1):
                card = self.deck.cards[index]

                if row == col:
                    card.reveal()
                self.columns[col].append(card)
                index += 1
        return self.columns
