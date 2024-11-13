class Card:
    def __init__(self, points, figure, front_image, back_image, revealed=False):
        # Inicjalizuje kartę z punktami, figurą, obrazem frontu i tyłu oraz statusem odkrycia.
        self.points = points
        self.figure = figure
        self.front_image = front_image
        self.back_image = back_image
        self.revealed = revealed

    def reveal(self):
        # Ustawia kartę jako odkrytą (frontem do góry).
        self.revealed = True

    def hide(self):
        # Ustawia kartę jako zakrytą (tyłem do góry).
        self.revealed = False

    def get_image(self):
        # Zwraca odpowiedni obraz w zależności od tego, czy karta jest odkryta czy zakryta.
        return self.front_image if self.revealed else self.back_image

    def __repr__(self):
        # Zwraca reprezentację tekstową karty z jej figurą, punktami i statusem odkrycia.
        return f"{self.figure} (Punkty: {self.points}, Odkryta: {self.revealed})"
