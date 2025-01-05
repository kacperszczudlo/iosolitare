import tkinter as tk
from PIL import Image, ImageTk
import os

class Settings(tk.Toplevel):
    def __init__(self, parent, app, show=True):
        super().__init__(parent)
        self.app = app
        if not show:
            self.withdraw()  # Ukryj okno jeśli `show` jest ustawione na False
        self.title("Settings")
        self.geometry("375x250")
        self.resizable(False, False)

        self.soundtrack_index = 0
        self.soundtracks = [ ('default', 'resources/soundtracks/default/default.mp3', 'resources/win/default/fireworks.jpg'), 
                            ('alternative', 'resources/soundtracks/alternative/palermo.mp3', 'resources/win/alternative/palermo.gif') ]

        self.hearts_image_path = os.path.join(self.app.script_dir, 'resources', 'placeholders', 'hearts_placeholder.png')
        self.diamonds_image_path = os.path.join(self.app.script_dir, 'resources', 'placeholders', 'diamonds_placeholder.png')
        self.clubs_image_path = os.path.join(self.app.script_dir, 'resources', 'placeholders', 'clubs_placeholder.png')
        self.spades_image_path = os.path.join(self.app.script_dir, 'resources', 'placeholders', 'spades_placeholder.png')

        self.settings_frame = tk.Frame(self)
        self.settings_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.populate_settings_frame()

    def create_button(self, text, row, width, command, font):
        button = tk.Button(self.settings_frame, text=text, font=font, fg="white", bd=0, highlightthickness=0, bg="#5C4033", activebackground="#3C2E23", command=command, width=width)
        button.grid(row=row, column=0, padx=10, pady=10, sticky="w")
        return button

    def populate_settings_frame(self):
        button_font = ("Arial", 12, "bold")
        button_width = 15

        self.create_button("Zmień motyw", 0, button_width, self.change_theme, button_font)

        self.theme_preview_frame = tk.Frame(self.settings_frame)
        self.theme_preview_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.card_back_preview = tk.Label(self.theme_preview_frame)
        self.card_back_preview.grid(row=0, column=0, padx=5)

        self.card_king_preview = tk.Label(self.theme_preview_frame)
        self.card_king_preview.grid(row=0, column=1, padx=5)

        self.create_button("Zmień tło", 1, button_width, self.change_background, button_font)

        self.background_preview = tk.Label(self.settings_frame)
        self.background_preview.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.create_button("Zmień dźwięk", 2, button_width, self.change_soundtrack, button_font)

        self.soundtrack_preview = tk.Label(self.settings_frame, text=self.soundtracks[self.soundtrack_index][0])
        self.soundtrack_preview.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.update_previews()


    def change_soundtrack(self):
        self.soundtrack_index = (self.soundtrack_index + 1) % len(self.soundtracks)
        soundtrack_name, soundtrack, gif = self.soundtracks[self.soundtrack_index]

        if soundtrack_name == 'default':
            self.app.current_card_place_sound = 'resources/soundtracks/default/swipe.mp3'
            self.app.current_victory_sound = 'resources/soundtracks/default/default.mp3'
            self.app.current_background_sound = 'resources/soundtracks/default/cas_music.mp3'
        elif soundtrack_name == 'alternative':
            self.app.current_card_place_sound = 'resources/soundtracks/alternative/augh.mp3'
            self.app.current_victory_sound = 'resources/soundtracks/alternative/palermo.mp3'
            self.app.current_background_sound = 'resources/soundtracks/alternative/temperatura.mp3'

        self.app.current_gif = gif

        print(f"Ścieżka dźwiękowa zmieniona na: {soundtrack_name}")
        print(f"GIF zmieniony na: {self.app.current_gif}")

        self.soundtrack_preview.config(text=soundtrack_name)
        self.update_previews()

        # Zatrzymaj bieżącą muzykę tła i uruchom nową
        self.app.stop_background_music()
        self.app.play_background_music()




    def update_previews(self):
        # Aktualizuj podgląd dla motywu kart
        card_back_path = os.path.join(self.app.cards_dir, 'behind.png')
        card_king_path = os.path.join(self.app.cards_dir, 'king_of_spades.png')
        card_back_image = self.load_image(card_back_path, (50, 70))
        card_king_image = self.load_image(card_king_path, (50, 70))
        self.card_back_preview.config(image=card_back_image)
        self.card_back_preview.image = card_back_image
        self.card_king_preview.config(image=card_king_image)
        self.card_king_preview.image = card_king_image

        # Aktualizuj podgląd dla tła
        background_image = self.load_image(self.app.game_background_path, (100, 50))
        self.background_preview.config(image=background_image)
        self.background_preview.image = background_image

    def change_theme(self):
        if self.app.current_theme == "alternative":
            self.app.cards_dir = os.path.join(self.app.resources_dir, 'cards', 'default')
            self.app.current_theme = "default"
        else:
            self.app.cards_dir = os.path.join(self.app.resources_dir, 'cards', 'alternative')
            self.app.current_theme = "alternative"

        print(f"Motyw zmieniony na: {self.app.current_theme}")
        self.update_previews()

    def change_background(self):
        backgrounds = [
            'default_background.jpg',
            'alternative1_background.jpg',
            'alternative2_background.jpg',
            'alternative3_background.jpg'
        ]

        current_background = os.path.basename(self.app.game_background_path)
        current_index = backgrounds.index(current_background)
        next_index = (current_index + 1) % len(backgrounds)
        self.app.game_background_path = os.path.join(self.app.resources_dir, 'background', backgrounds[next_index])

        self.app.game_background_image = self.load_image(self.app.game_background_path, (1200, 800))
        print(f"Tło zmienione na: {self.app.game_background_path}")
        self.update_previews()
        self.prepare_foundation_images()

    def load_image(self, image_path, size):
        try:
            return ImageTk.PhotoImage(Image.open(image_path).resize(size))
        except Exception as e:
            print(f"Error loading image from {image_path}: {e}")
            return None

    def prepare_foundation_images(self):
        foundation_positions = [
            (550, 153, self.hearts_image_path),
            (690, 153, self.diamonds_image_path),
            (830, 153, self.clubs_image_path),
            (970, 153, self.spades_image_path),
        ]
        prepared_images = []
        for x, y, image_path in foundation_positions:
            background = Image.open(self.app.game_background_path).convert("RGBA")
            background = background.crop((x, y, x + 100, y + 145))  # Wytnij fragment tła
            image = Image.open(image_path).convert("RGBA")
            image = image.resize((100, 145), Image.Resampling.LANCZOS)
            combined = Image.alpha_composite(background, image)
            tk_image = ImageTk.PhotoImage(combined)
            prepared_images.append(tk_image)
        self.app.prepared_foundation_images = prepared_images
        return prepared_images
