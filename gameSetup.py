from tkinter import Label, Button
from PIL import Image, ImageTk
from cardDeck import CardDeck
from firstDeal import FirstDeal

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
        card_label.card_object = card

        card_label.bind("<ButtonPress-1>", self.on_card_click)
        card_label.bind("<B1-Motion>", self.on_card_drag)
        card_label.bind("<ButtonRelease-1>", self.on_card_release)

        return card_label

    def display_initial_deal(self, columns):
        y_offset = 378
        y_spacing = 30

        for col in range(7):
            x_position = 131 + col * 140
            for row, card in enumerate(columns[col]):
                y_position = y_offset + row * y_spacing
                card_label = self.create_card(x_position, y_position, card)
                self.card_labels.append(card_label)

    def display_stock_pile(self):
        stock_pile_x, stock_pile_y = 131, 153
        for i in range(len(self.first_deal.columns) * (len(self.first_deal.columns) + 1) // 2, len(self.deck.cards)):
            self.deck.cards[i].hide()
            card_label = self.create_card(stock_pile_x, stock_pile_y, self.deck.cards[i])
            self.card_labels.append(card_label)

    def reset_game(self):
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()

        self.deck = CardDeck()
        self.deck.shuffle_deck()

        self.first_deal = FirstDeal(self.deck)
        columns = self.first_deal.setup_initial_layout()
        self.display_initial_deal(columns)
        self.display_stock_pile()

    def on_card_click(self, event):

        self.selected_card = event.widget.card_object
        self.start_x = event.widget.winfo_x()
        self.start_y = event.widget.winfo_y()
        self.original_x = event.widget.winfo_x()
        self.original_y = event.widget.winfo_y()

        # To jest uzywane do odkladania karty
        self.start_offset_x = event.x
        self.start_offset_y = event.y

        if not self.selected_card.revealed:
            self.selected_card = None


    def on_card_drag(self, event):
        if self.selected_card:
            new_x = event.widget.winfo_x() + (event.x - self.start_offset_x)
            new_y = event.widget.winfo_y() + (event.y - self.start_offset_y)

            event.widget.place(x=new_x, y=new_y)

            self.start_x = new_x
            self.start_y = new_y

    def on_card_release(self, event):
        if self.selected_card:
            if self.is_valid_move():
                self.place_in_column(event.x, event.y)
            else:
                event.widget.place(x=self.original_x, y=self.original_y)

            self.selected_card = None

    def is_valid_move(self):
        # TODO: W następnym sprincie zaimplementuj logikę sprawdzania poprawności ruchu
        return True

    def place_in_column(self, x, y):
        # TODO: W następnym sprincie zaimplementuj logikę umieszczania w kolumnie
        pass