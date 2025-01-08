import os
from tkinter import *
from PIL import Image, ImageTk
import pygame
from settings import Settings
from gameLogic import get_highscore
from gameSetup import GameSetup
from gameUI import GameUI
from tkinter import Toplevel, Canvas
from ffpyplayer.player import MediaPlayer
import threading


class PasjansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasjans Inżynieria Oprogramowania")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.script_dir, 'resources')
        self.cards_dir = os.path.join(self.resources_dir, 'cards', 'default')
        self.playing_background_music = True
        self.current_theme = "default"
        self.current_gif = 'resources/win/default/fireworks.jpg'
        self.current_background_sound = 'resources/soundtracks/default/cas_music.mp3'
        self.current_card_place_sound = 'resources/soundtracks/default/swipe.mp3'
        self.current_victory_sound = 'resources/soundtracks/default/default.mp3'
        self.game_background_path = os.path.join(self.resources_dir, 'background', 'default_background.jpg')

        self.menu_background_path = os.path.join(self.script_dir, 'resources', 'menu', 'menu.jpg')
        self.corona_image_path = os.path.join(self.script_dir, 'resources', 'menu', 'corona.jpg')
        self.rules_path = os.path.join(self.script_dir, 'resources', 'rules.txt')

        temp_settings = Settings(self.root, self, show=False)

        self.menu_background_image = temp_settings.load_image(self.menu_background_path, (1200, 800))
        self.game_background_image = temp_settings.load_image(self.game_background_path, (1200, 800))
        self.corona_image = temp_settings.load_image(self.corona_image_path, (200, 300))

        self.prepared_foundation_images = temp_settings.prepare_foundation_images()

        self.current_frame = None
        self.show_menu()

        pygame.mixer.init()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Dodaj obsługę zamknięcia głównego okna

    def play_background_music(self):
        pygame.mixer.music.load(self.current_background_sound)
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)

    def show_tutorial(self):
        # Ścieżka do pliku wideo
        video_path = os.path.join(self.resources_dir, "tutorialek.mp4")

        # Ustawienie stałej szerokości i wysokości okna
        window_width = 1200
        window_height = 800

        # Tworzenie okna dla samouczka
        tutorial_window = Toplevel(self.root)
        tutorial_window.title("Samouczek")
        tutorial_window.geometry(f"{window_width}x{window_height}")
        tutorial_window.resizable(False, False)

        # Wyśrodkowanie okna
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        tutorial_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        # Ustawienie okna na najwyższy indeks
        tutorial_window.attributes('-topmost', True)

        # Canvas do wyświetlania wideo
        canvas = Canvas(tutorial_window, width=window_width, height=window_height, bg="black")
        canvas.pack()

        # MediaPlayer dla wideo
        player = MediaPlayer(video_path)

        # Flaga do zatrzymania odtwarzania
        playing = True

        def play_video():
            nonlocal playing
            while playing:
                try:
                    frame, val = player.get_frame()
                    if val == 'eof':  # Koniec wideo
                        break
                    if frame is not None and tutorial_window.winfo_exists():  # Sprawdzanie istnienia okna
                        img, _ = frame
                        img = Image.frombytes('RGB', img.get_size(), img.to_bytearray()[0])
                        img = img.resize((window_width, window_height))  # Skalowanie obrazu
                        imgtk = ImageTk.PhotoImage(image=img)
                        canvas.create_image(0, 0, anchor="nw", image=imgtk)
                        canvas.image = imgtk  # Zapobiega usuwaniu obrazu z pamięci
                except Exception as e:
                   
                    break

        def stop_playback():
            nonlocal playing
            playing = False
            player.close_player()  # Zatrzymanie odtwarzania
            tutorial_window.destroy()

        # Uruchomienie wideo w osobnym wątku
        video_thread = threading.Thread(target=play_video, daemon=True)
        video_thread.start()

        # Obsługa zamykania okna
        tutorial_window.protocol("WM_DELETE_WINDOW", stop_playback)


    def stop_music(self):
        pygame.mixer.music.stop()

    def show_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        background_label = Label(self.current_frame, image=self.menu_background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        corona_label = Label(self.current_frame, image=self.corona_image)
        corona_label.place(x=500, y=300)

        temp_game_ui = GameUI(GameSetup(self.root, self.resources_dir, self.cards_dir, app=self), self.root)
        button_width = 200
        menu_button_y = 400
        button_font = ("Arial", 12, "bold")
        self.create_button(temp_game_ui, "Nowa gra", 130, menu_button_y - 100, button_width, self.start_game, button_font)
        self.create_button(temp_game_ui, "Najlepsze wyniki", 130, menu_button_y - 50, button_width, self.show_highscore, button_font)
        self.create_button(temp_game_ui, "Zasady Gry", 130, menu_button_y, button_width, self.show_game_rules, button_font)
        self.create_button(temp_game_ui, "Samouczek", 130, menu_button_y + 50, button_width, self.show_tutorial, button_font)
        self.create_button(temp_game_ui, "Ustawienia", 130, menu_button_y + 100, button_width, self.show_settings, button_font)

    def create_button(self, game_ui, text, x, y, width, command, font):
        button = Button(self.current_frame, text=text, font=font, fg="white", bd=0, highlightthickness=0, bg="#5C4033", activebackground="#3C2E23", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=40)

    def show_game_rules(self):
        rules_window = Toplevel(self.root)
        rules_window.title("Zasady Gry")
        rules_window.geometry("600x330")
        rules_window.resizable(False, False)

        with open(self.rules_path, 'r', encoding='utf-8') as file:
            rules_text = file.read()

        rules_label = Label(rules_window, text=rules_text, font=("Arial", 12), justify=LEFT, wraplength=580)
        rules_label.pack(pady=20, padx=20, fill=BOTH, expand=True)

    def show_highscore(self):
        wyniki = get_highscore()
        highscore_window = Toplevel(self.root)
        highscore_window.title("Najlepsze wyniki")
        highscore_window.geometry("600x330")
        highscore_window.resizable(False, False)

        highscore_frame = Frame(highscore_window, bg="#5C4033")
        highscore_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = Label(highscore_frame, text="Najlepsze wyniki", font=("Arial", 16, "bold"), fg="white", bg="#5C4033")
        title_label.pack(pady=(0, 10))

        for index, (nickname, score) in enumerate(wyniki[:10]):
            label_text = f"{index + 1}. {nickname}: {score} points"
            label = Label(highscore_frame, text=label_text, font=("Arial", 12), fg="white", bg="#5C4033")
            label.pack(anchor="w")

        for i in range(10 - len(wyniki)):
            label = Label(highscore_frame, text=f"{len(wyniki) + i + 1}. -", font=("Arial", 12), fg="white", bg="#5C4033")
            label.pack(anchor="w")

    def show_settings(self):
        settings = Settings(self.root, self)
        settings.grab_set()

    def music_button_change(self):
        if self.playing_background_music:
            self.stop_music()
            self.playing_background_music = False
        else:
            self.play_background_music()
            self.playing_background_music = True

    def start_game(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        background_label = Label(self.current_frame, image=self.game_background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        foundation_positions = [
            (550, 153),
            (690, 153),
            (830, 153),
            (970, 153),
        ]

        for (x, y), tk_image in zip(foundation_positions, self.prepared_foundation_images):
            label = Label(self.current_frame, image=tk_image, bd=0)
            label.image = tk_image
            label.place(x=x, y=y)

        game_setup = GameSetup(self.root, self.resources_dir, self.cards_dir, app=self)
        user_interface = GameUI(game_setup, self.root)

        user_interface.create_button("Nowa gra", 130, 16, 119, game_setup.reset_game)
        user_interface.create_button("Cofnij", 265, 16, 119, game_setup.undo_move)
        user_interface.create_label("Punkty: 0", 711, 16, 119)
        user_interface.create_label("Ruchy: 0", 846, 16, 119)
        user_interface.create_label("Czas: 00:00", 981, 16, 119)
        user_interface.create_button("Najlepsze wyniki", 16, 753, 200, self.show_highscore)
        user_interface.create_button("Wycisz/Odcisz dzwiek", 975, 753, 200, self.music_button_change)

        for x, y in [(130, 153), (270, 153), (130, 378), (270, 378), (410, 378), (550, 378), (690, 378), (830, 378), (970, 378)]:
            user_interface.create_placeholder(x, y)

        self.stop_music()  # Zatrzymaj bieżącą muzykę tła przed rozpoczęciem nowej gry
        game_setup.reset_game()
        self.play_background_music()  # Uruchom muzykę tła po rozpoczęciu nowej gry

    def on_closing(self):
        self.stop_music()  # Zatrzymaj muzykę przed zamknięciem aplikacji
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = PasjansApp(root)
    root.mainloop()
