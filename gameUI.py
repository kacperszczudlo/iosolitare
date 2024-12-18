import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import gameEvents
from cardDeck import CardDeck
from firstDeal import FirstDeal
from gameLogic import *

class GameUI:
    def __init__(self, setup,root=None):
        self.gameSetup = setup
        self.score = 0
        self.pause = False
        self.root = root

    def create_button(self, text, x, y, width, command=None):
        button = Button(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                        bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        label = Label(self.gameSetup.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                      bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)
        return label


    def create_placeholder(self, x, y):
        placeholder_path = os.path.join(self.gameSetup.resources_dir, 'placeholders', 'placeholder.png')
        placeholder_image = Image.open(placeholder_path).resize((100, 145))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)
        placeholder_label = Label(self.gameSetup.window, image=placeholder_photo, bd=0)
        placeholder_label.image = placeholder_photo
        placeholder_label.place(x=x, y=y)

    def create_card(self, x, y, card):
        card_image_path = os.path.join(self.gameSetup.cards_dir, os.path.basename(card.get_image()))
        card_image = Image.open(card_image_path).resize((100, 145))
        card_photo = ImageTk.PhotoImage(card_image)
        card_label = Label(self.gameSetup.window, image=card_photo, bd=0)
        card_label.image = card_photo
        card_label.place(x=x, y=y)
        card_label.card_object = card
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
        # print(f"Zmieniono wartosc pkt o {score}")
        self.pause = False
        self.score_label.config(text=f"Punkty: {self.score}")

    def show_centered_box(self):

        self.popup = tk.Toplevel(self.gameSetup.window)
        self.popup.title("Popup Window")
        self.popup.overrideredirect(True)

        initial_width = 10
        initial_height = 10
        final_width = 400
        final_height = 400
        self.popup.geometry(f"{initial_width}x{initial_height}")

        self.popup.grab_set()


        self.popup.resizable(False, False)


        self.gameSetup.window.update_idletasks()
        main_x = self.gameSetup.window.winfo_x()
        main_y = self.gameSetup.window.winfo_y()
        main_width = self.gameSetup.window.winfo_width()
        main_height = self.gameSetup.window.winfo_height()



        x = main_x + (main_width // 2) - (final_width // 2)
        y = main_y + (main_height // 2) - (final_height // 2)


        self.popup.geometry(f"{final_width}x{final_height}+{x}+{y}")

        #Wylacza klikanie rzeczy w tle
        self.gameSetup.window.attributes('-disabled', True)

        border_frame = tk.Frame(self.popup, bd=5, relief=tk.SUNKEN, highlightbackground="black", highlightcolor="black", highlightthickness=5)
        border_frame.pack(fill=tk.BOTH, expand=True)


        bg_image = Image.open("resources/fireworks.jpg")
        bg_image = bg_image.resize((final_width, final_height))
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(border_frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)

        # Zawartosc okienka
        label = Label(border_frame, text="Tu beda wyniki", font=("Arial", 12, "bold"), fg="white", bd=0,
                      highlightthickness=0,
                      bg="#5C4033")
        label.pack(pady=20)

        label = Label(border_frame, text=f"Czas: {self.elapsed_time} sekundy", font=("Arial", 12, "bold"), fg="white", bd=0,
                      highlightthickness=0,
                      bg="#5C4033")
        label.pack(pady=20)

        label = Label(border_frame, text=f"Ruchy: {self.gameSetup.move_counter}", font=("Arial", 12, "bold"),
                      fg="white", bd=0,
                      highlightthickness=0,
                      bg="#5C4033")
        label.pack(pady=20)

        label = Label(border_frame, text=f"Punkty: {self.score} pkt", font=("Arial", 12, "bold"),
                      fg="white", bd=0,
                      highlightthickness=0,
                      bg="#5C4033")
        label.pack(pady=20)

        close_button = tk.Button(border_frame, text="Zamknij okno", font=("Arial", 12, "bold"), fg="white", bd=0,
                        highlightthickness=0,
                        bg="#5C4033", state="normal",command=lambda: self.close_overlay())
        close_button.pack(pady=10)

        restart_button = tk.Button(border_frame, text="Nowa gra", font=("Arial", 12, "bold"), fg="white", bd=0,
                                 highlightthickness=0,
                                 bg="#5C4033", state="normal", command=lambda: self.restart())

        restart_button.pack(pady=10)

        # Wait until the popup is closed
        self.popup.geometry(f"{final_width}x{final_height}+{x}+{y}")
        self.animate_popup(initial_width, initial_height, final_width, final_height, x,y)
        self.popup.wait_window()

    def close_overlay(self):
        self.gameSetup.window.attributes('-disabled', False)
        self.popup.destroy()

    def restart(self):
        self.gameSetup.window.attributes('-disabled', False)
        self.popup.destroy()
        self.gameSetup.reset_game()


    def animate_popup(self,initial_width, initial_height, final_width, final_height, x, y):
        current_width = initial_width
        current_height = initial_height
        step_width = (final_width - initial_width) // 10
        step_height = (final_height - initial_height) // 10

        def step():
            nonlocal current_width, current_height
            if current_width < final_width and current_height < final_height:
                current_width += step_width
                current_height += step_height
                self.popup.geometry(f"{current_width}x{current_height}+{x}+{y}")
                self.popup.after(20, step)

        step()


