import os
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from cardDeck import CardDeck
from firstDeal import FirstDeal
class GameUI:
    def __init__(self,setup):
        self.gameSetup = setup

    def create_button(self, text, x, y, width, command=None):
        # Tworzy przycisk w interfejsie użytkownika.
        button = Button(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                        bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        # Tworzy etykietę tekstową w interfejsie użytkownika.
        label = Label(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                      bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)

    def create_placeholder(self, x, y):
        # Umieszcza obraz zastępczy w interfejsie.
        placeholder_path = os.path.join(self.gameSetup.resources_dir, 'placeholder.png')
        placeholder_image = Image.open(placeholder_path).resize((100, 145))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)
        placeholder_label = Label(self.gameSetup.window, image=placeholder_photo, bd=0)
        placeholder_label.image = placeholder_photo
        placeholder_label.place(x=x, y=y)


