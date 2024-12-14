import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk

import gameEvents
from cardDeck import CardDeck
from firstDeal import FirstDeal
from gameLogic import *

class GameUI:
    def __init__(self, setup):
        self.gameSetup = setup
        self.score = 0
        self.pause = False


    def create_button(self, text, x, y, width, command=None):
        button = Button(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                        bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        label = Label(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                      bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)
        return label

    def create_placeholder(self, x, y, suit=None):
        # Pobierz preładowany obraz dla danego suit lub ogólny placeholder
        if suit:
            placeholder_image = self.gameSetup.preloaded_images[f"{suit}_placeholder"]
        else:
            placeholder_image = self.gameSetup.preloaded_images["general_placeholder"]

        placeholder_label = Label(self.gameSetup.window, image=placeholder_image, bd=0)
        placeholder_label.image = placeholder_image  # Referencja do obrazu
        placeholder_label.place(x=x, y=y)

        print(f"Stworzono placeholder dla {suit if suit else 'ogólny'} na pozycji ({x}, {y})")
        return placeholder_label

        print(f"Created placeholder for suit {suit} at ({x}, {y})")  # Debugowanie
        return placeholder_label

    def create_card(self, x, y, card):
        # Pobierz obraz karty z preładowanych obrazów
        card_image = self.gameSetup.preloaded_images[card.figure] if card.revealed else self.gameSetup.preloaded_images[
            "behind"]
        card_label = Label(self.gameSetup.window, image=card_image, bd=0)
        card_label.image = card_image  # Referencja do obrazu
        card_label.place(x=x, y=y)
        card_label.card_object = card

        # Obsługa zdarzeń
        card_label.bind("<ButtonPress-1>", partial(gameEvents.on_card_click, self.gameSetup))
        card_label.bind("<B1-Motion>", partial(gameEvents.on_card_drag, self.gameSetup))
        card_label.bind("<ButtonRelease-1>", partial(gameEvents.on_card_release, self.gameSetup))
        card_label.bind("<Double-1>", partial(gameEvents.on_card_double_click, self.gameSetup))

        return card_label

    def display_initial_deal(self, columns):
        y_offset = 378
        y_spacing = 30
        for col in range(7):
            x_position = 131 + col * 140
            for row, card in enumerate(columns[col]):
                y_position = y_offset + row * y_spacing
                card_label = self.create_card(x_position, y_position, card)
                self.gameSetup.card_labels.append(card_label)
                update_card_position(self.gameSetup, card, x_position, y_position)

    def display_stock_pile(self):
        stock_pile_x, stock_pile_y = 131, 153
        for i in range(len(self.gameSetup.first_deal.columns) * (len(self.gameSetup.first_deal.columns) + 1) // 2, len(self.gameSetup.deck.cards)):
            self.gameSetup.deck.cards[i].hide()
            card_label = self.create_card(stock_pile_x, stock_pile_y, self.gameSetup.deck.cards[i])
            self.gameSetup.card_labels.append(card_label)
            card_label.bind("<Button-1>", partial(gameEvents.on_stock_pile_click, self.gameSetup))

    def highlight_card(self, card_label, color):
        card_label.config(bd=0, relief="solid", highlightbackground=color, highlightthickness=3)

    def remove_highlight(self, card_label):
        card_label.config(bd=0, highlightthickness=0)

    def start_timer(self):
        self.elapsed_time = 0
        self.timer_label = Label(self.gameSetup.window, text="Czas: 00:00", font=("Arial", 12, "bold"), fg="white", bg="#5C4033")
        self.timer_label.place(x=981, y=16, width=119, height=31)
        self.update_timer()

    def update_timer(self):
        minutes, seconds = divmod(self.elapsed_time, 60)
        time_display = f"Czas: {minutes:02}:{seconds:02}"
        self.timer_label.config(text=time_display)
        self.elapsed_time += 1
        if self.elapsed_time % 15 == 0 and not self.pause:
            self.pause = True
            self.update_score(-2)
        self.gameSetup.window.after(1000, self.update_timer)

    def update_move_counter(self, count):
        self.move_counter_label = Label(self.gameSetup.window, text=f"Ruchy: {count}", font=("Arial", 12, "bold"), fg="white", bg="#5C4033")
        self.move_counter_label.place(x=846, y=16, width=119, height=31)

    def init_score(self):
        self.score = 0
        self.score_label = Label(self.gameSetup.window, text=f"Punkty: 0", font=("Arial", 12, "bold"), fg="white", bg="#5C4033")
        self.score_label.place(x=711, y=16, width=119, height=31)


    def update_score(self, score):
        self.score += score
        if self.score < 0:
            self.score = 0
        print(f"Zmieniono wartosc pkt o {score}")
        self.pause = False
        self.score_label.config(text=f"Punkty: {self.score}")
