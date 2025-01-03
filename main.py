import os
from tkinter import *
from PIL import Image, ImageTk

from gameLogic import get_highscore
from gameSetup import GameSetup
from gameUI import GameUI




class PasjansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasjans Inżynieria Oprogramowania")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.script_dir, 'resources')
        self.cards_dir = os.path.join(self.resources_dir, 'cards', 'default')

        # Flaga do zmiany motywu
        self.current_theme = "default"

        # Ścieżki do obrazów
        self.menu_background_path = os.path.join(self.script_dir, 'resources','menu', 'menu.jpg')
        self.game_background_path = os.path.join(self.script_dir, 'resources','background', 'background.jpg')
        self.corona_image_path = os.path.join(self.script_dir, 'resources','menu', 'corona.jpg')
        self.rules_path = os.path.join(self.script_dir, 'resources', 'rules.txt')

        self.hearts_image_path = os.path.join(self.script_dir, 'resources', 'placeholders', 'hearts_placeholder.png')
        self.diamonds_image_path = os.path.join(self.script_dir, 'resources', 'placeholders', 'diamonds_placeholder.png')
        self.clubs_image_path = os.path.join(self.script_dir, 'resources', 'placeholders', 'clubs_placeholder.png')
        self.spades_image_path = os.path.join(self.script_dir, 'resources', 'placeholders', 'spades_placeholder.png')

        # Wczytanie obrazów
        self.menu_background_image = ImageTk.PhotoImage(Image.open(self.menu_background_path).resize((1200, 800)))
        self.game_background_image = ImageTk.PhotoImage(Image.open(self.game_background_path).resize((1200, 800)))
        self.corona_image = ImageTk.PhotoImage(Image.open(self.corona_image_path).resize((200, 300)))

        # Przygotowanie przetworzonych obrazów stosów końcowych
        self.prepared_foundation_images = self.prepare_foundation_images()

        self.current_frame = None
        self.show_menu()

    def change_theme(self):
        """
        Zmienia motyw kart i tła gry pomiędzy 'alternative' i 'default'.
        """
        if self.current_theme == "alternative":
            self.cards_dir = os.path.join(self.resources_dir, 'cards', 'default')
            self.game_background_path = os.path.join(self.resources_dir, 'background', 'background.jpg')
            self.current_theme = "default"
        else:
            self.cards_dir = os.path.join(self.resources_dir, 'cards', 'alternative')
            self.game_background_path = os.path.join(self.resources_dir, 'background', 'alternative_background3.jpg')
            self.current_theme = "alternative"

        # Załaduj nowe tło
        self.prepared_foundation_images = self.prepare_foundation_images()

        self.game_background_image = ImageTk.PhotoImage(Image.open(self.game_background_path).resize((1200, 800)))

        print(f"Motyw zmieniony na: {self.current_theme}")


        self.show_menu()

    def prepare_foundation_images(self):
        """
        Przygotowuje obrazy dla stosów końcowych (łączy tło z placeholderami) w oparciu o aktualny motyw.
        """
        foundation_positions = [
            (550, 153, self.hearts_image_path),
            (690, 153, self.diamonds_image_path),
            (830, 153, self.clubs_image_path),
            (970, 153, self.spades_image_path),
        ]
        prepared_images = []

        for x, y, image_path in foundation_positions:
            # Wczytaj obraz tła dla aktualnego motywu
            background = Image.open(self.game_background_path).convert("RGBA")
            background = background.crop((x, y, x + 100, y + 145))  # Wytnij fragment tła

            # Wczytaj obraz placeholdera dla aktualnego motywu
            image = Image.open(image_path).convert("RGBA")
            image = image.resize((100, 145), Image.Resampling.LANCZOS)

            # Połącz tło z obrazem placeholdera
            combined = Image.alpha_composite(background, image)

            # Konwersja do PhotoImage
            tk_image = ImageTk.PhotoImage(combined)
            prepared_images.append(tk_image)

        return prepared_images

    def show_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        background_label = Label(self.current_frame, image=self.menu_background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        corona_label = Label(self.current_frame, image=self.corona_image)
        corona_label.place(x=500, y=300)

        temp_game_ui = GameUI(GameSetup(self.root,self.resources_dir, self.cards_dir))
        button_width = 200
        menu_button_y = 400
        button_font = ("Arial", 12, "bold")
        self.create_button(temp_game_ui, "Nowa gra", 130, menu_button_y - 100, button_width, self.start_game, button_font)
        self.create_button(temp_game_ui, "Najlepsze wyniki", 130, menu_button_y - 50, button_width, self.show_highscore, button_font)
        self.create_button(temp_game_ui, "Zasady Gry", 130, menu_button_y, button_width, self.show_game_rules, button_font)
        self.create_button(temp_game_ui, "Samouczek", 130, menu_button_y + 50, button_width, None, button_font)
        self.create_button(temp_game_ui, "Zmiana Motywu", 130, menu_button_y + 100, button_width, self.change_theme, button_font)

    def create_button(self, game_ui, text, x, y, width, command, font):
        button = Button(self.current_frame, text=text, font=font, fg="white", bd=0, highlightthickness=0,
                        bg="#5C4033", activebackground="#3C2E23", state="normal", command=command)
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

    def start_game(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)



        background_label = Label(self.current_frame, image=self.game_background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Wyświetlanie przygotowanych obrazów stosów końcowych
        foundation_positions = [
            (550, 153),
            (690, 153),
            (830, 153),
            (970, 153),
        ]

        for (x, y), tk_image in zip(foundation_positions, self.prepared_foundation_images):
            label = Label(self.current_frame, image=tk_image, bd=0)
            label.image = tk_image  # Zachowaj referencję do obrazu
            label.place(x=x, y=y)

        game_setup = GameSetup(self.root,self.resources_dir, self.cards_dir)
        user_interface = GameUI(game_setup,self.root)

        user_interface.create_button("Nowa gra", 130, 16, 119, game_setup.reset_game)
        user_interface.create_button("Cofnij", 265, 16, 119, game_setup.undo_move)
        user_interface.create_label("Punkty: 0", 711, 16, 119)
        user_interface.create_label("Ruchy: 0", 846, 16, 119)
        user_interface.create_label("Czas: 00:00", 981, 16, 119)
        user_interface.create_button("Najlepsze wyniki", 16, 753, 200)

        for x, y in [(130, 153), (270, 153),
                     (130, 378), (270, 378), (410, 378), (550, 378), (690, 378), (830, 378), (970, 378)]:
            user_interface.create_placeholder(x, y)

        game_setup.reset_game()

    def show_highscore(self):
        # Create a new Toplevel window for the highscore
        wyniki = get_highscore()
        highscore_window = Toplevel(self.root)
        highscore_window.title("Najlepsze wyniki")
        highscore_window.geometry("600x330")
        highscore_window.resizable(False, False)

        # Add a frame for the high scores
        highscore_frame = Frame(highscore_window, bg="#5C4033")
        highscore_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a title label
        title_label = Label(highscore_frame, text="Najlepsze wyniki", font=("Arial", 16, "bold"), fg="white",
                               bg="#5C4033")
        title_label.pack(pady=(0, 10))

        # Display the high scores
        for index, (nickname, score) in enumerate(wyniki[:10]):
            label_text = f"{index + 1}. {nickname}: {score} points"
            label = Label(highscore_frame, text=label_text, font=("Arial", 12), fg="white", bg="#5C4033")
            label.pack(anchor="w")

        # If there are fewer than 10 results, add empty labels for the remaining spots
        for i in range(10 - len(wyniki)):
            label = Label(highscore_frame, text=f"{len(wyniki) + i + 1}. -", font=("Arial", 12), fg="white",
                             bg="#5C4033")
            label.pack(anchor="w")


if __name__ == "__main__":
    root = Tk()
    app = PasjansApp(root)
    root.mainloop()
