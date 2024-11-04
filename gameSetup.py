from tkinter import Label, Button
from PIL import Image, ImageTk
from cardDeck import CardDeck

class GameSetup:
    def __init__(self, window):
        self.window = window
        self.card_labels = []
        self.deck = CardDeck()

    def create_button(self, text, x, y, width, command=None):
        button = Button(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        label = Label(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)

    def create_placeholder(self, x, y):
        placeholder_image = Image.open("resources/placeholder.png").resize((100, 145))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)
        placeholder_label = Label(self.window, image=placeholder_photo, bd=0)
        placeholder_label.image = placeholder_photo
        placeholder_label.place(x=x, y=y)

    def create_card(self, x, y, card):
        card_image_path = card.get_image()
        card_image = Image.open(card_image_path).resize((100, 145))
        card_photo = ImageTk.PhotoImage(card_image)
        card_label = Label(self.window, image=card_photo, bd=0)
        card_label.image = card_photo
        card_label.place(x=x, y=y)
        return card_label




