import os
from functools import partial
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import gameEvents
from cardDeck import CardDeck
from firstDeal import FirstDeal
from gameLogic import *
import pygame
import threading



class GameUI:
    def __init__(self, setup, root=None):
        self.gameSetup = setup
        self.score = 0
        self.pause = False
        self.root = root
        self.added = False

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

    def display_stock_pile(self, wyjebane=[]):
        stock_pile_x, stock_pile_y = 131, 153
        for i in range(len(self.gameSetup.first_deal.columns) * (len(self.gameSetup.first_deal.columns) + 1) // 2, len(self.gameSetup.deck.cards)):
            if self.gameSetup.deck.cards[i] not in wyjebane:
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
        self.pause = False
        self.score_label.config(text=f"Punkty: {self.score}")

    def show_centered_box(self):
        self.popup = tk.Toplevel(self.gameSetup.window)
        self.popup.title("Gratulacje wygrałeś!!!")
        final_width = 730
        final_height = 430
        self.popup.geometry(f"{final_width}x{final_height}")
        self.popup.resizable(False, False)

        self.popup.grab_set()

        button_frame = tk.Frame(self.popup, bg="#5C4033")
        button_frame.place(x=0, y=0, relwidth=1, height=45)

        best_scores_button = tk.Button(button_frame, text="Najlepsze wyniki", font=("Arial", 12, "bold"), fg="white",
                                       bg="#5C4033", command=self.show_highscore)
        best_scores_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        label_2 = tk.Label(button_frame, text=f"Czas: {self.elapsed_time} sekundy", font=("Arial", 12, "bold"),
                           fg="white", bg="#5C4033")
        label_2.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        label_3 = tk.Label(button_frame, text=f"Ruchy: {self.gameSetup.move_counter}", font=("Arial", 12, "bold"),
                           fg="white", bg="#5C4033")
        label_3.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        label_4 = tk.Label(button_frame, text=f"Punkty: {self.score} pkt", font=("Arial", 12, "bold"), fg="white",
                           bg="#5C4033")
        label_4.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        restart_button = tk.Button(button_frame, text="Nowa gra", font=("Arial", 12, "bold"), fg="white", bg="#5C4033",
                                   command=lambda: self.restart())
        restart_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

        self.bg_image = ImageTk.PhotoImage(file="resources/win/alternative/palermo.gif", format="gif -index 0")
        self.bg_label = tk.Label(self.popup, image=self.bg_image)
        self.bg_label.image = self.bg_image
        self.bg_label.place(x=0, y=45, relwidth=1, relheight=0.95)

        self.play_music("resources/soundtracks/alternative/palermo.mp3")
        self.animate_gif("resources/win/alternative/palermo.gif")

        # Frame for high score input
        input_frame = tk.Frame(self.popup, bg="#5C4033")
        input_frame.place(relx=0.5, rely=0.85, anchor="center")

        name_label = tk.Label(input_frame, text="Twoje imię:", font=("Arial", 12, "bold"), fg="white", bg="#5C4033")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        submit_button = tk.Button(input_frame, text="Dodaj wynik", font=("Arial", 12, "bold"), fg="white", bg="#5C4033",
                                  command=self.submit_highscore)
        submit_button.grid(row=0, column=2, padx=5, pady=5)

        self.popup.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.stop_music()
        self.popup.destroy()
        self.gameSetup.window.attributes('-disabled', False)

    def animate_gif(self, filepath):
        self.frames = []
        try:
            img = Image.open(filepath)
            while True:
                self.frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(len(self.frames))
        except EOFError:
            pass

        self.current_frame = 0

        def update_frame():
            self.bg_label.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.bg_label.after(20, update_frame)

        update_frame()


    def close_overlay(self):

        self.gameSetup.window.attributes('-disabled', False)
        self.popup.destroy()

    def restart(self):
        self.gameSetup.window.attributes('-disabled', False)
        self.popup.destroy()
        self.gameSetup.reset_game()
        self.stop_music()


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

    def play_music(self,file_path):
        def music():
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        music_thread = threading.Thread(target=music)
        music_thread.start()

    def stop_music(self):
        pygame.mixer.music.stop()

    def show_highscore(self):
        # Temporarily release grab
        self.popup.grab_release()

        # Create a new Toplevel window for the highscore
        wyniki = get_highscore()
        highscore_window = tk.Toplevel(self.gameSetup.window)
        highscore_window.title("Najlepsze wyniki")
        highscore_window.geometry("600x330")
        highscore_window.resizable(False, False)

        # Add a frame for the high scores
        highscore_frame = tk.Frame(highscore_window, bg="#5C4033")
        highscore_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a title label
        title_label = tk.Label(highscore_frame, text="Najlepsze wyniki", font=("Arial", 16, "bold"), fg="white",
                               bg="#5C4033")
        title_label.pack(pady=(0, 10))

        # Display the high scores
        for index, (nickname, score) in enumerate(wyniki[:10]):
            label_text = f"{index + 1}. {nickname}: {score} points"
            label = tk.Label(highscore_frame, text=label_text, font=("Arial", 12), fg="white", bg="#5C4033")
            label.pack(anchor="w")

        # If there are fewer than 10 results, add empty labels for the remaining spots
        for i in range(10 - len(wyniki)):
            label = tk.Label(highscore_frame, text=f"{len(wyniki) + i + 1}. -", font=("Arial", 12), fg="white",
                             bg="#5C4033")
            label.pack(anchor="w")



    def submit_highscore(self):
        player_name = self.name_entry.get().strip()
        if not self.added and player_name:
            self.added = True
            add_highscore(player_name,self.score)
