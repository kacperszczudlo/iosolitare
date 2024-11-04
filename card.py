class Card:
    def __init__(self,points,figure, front_image, back_image, revealed=False):
        self.points = points
        self.figure = figure
        self.front_image = front_image
        self.back_image = back_image
        self.revealed = revealed

    def reveal(self):
        self.revealed = True

    def hide(self):
        self.revealed = False

    def get_image(self):
        return self.front_image if self.revealed else self.back_image

    def __repr__(self):
        return f"{self.figure} (Points: {self.points}, Revealed: {self.revealed})"


