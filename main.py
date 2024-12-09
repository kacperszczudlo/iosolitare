import os
from tkinter import *
from PIL import Image, ImageTk
from gameSetup import GameSetup
from gameUI import GameUI

class PasjansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasjans Inzynieria Oprogramowania")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_background_path = os.path.join(self.script_dir, 'resources', 'menu.jpg')
        self.game_background_path = os.path.join(self.script_dir, 'resources', 'background.jpg')
        self.corona_image_path = os.path.join(self.script_dir, 'resources', 'corona.jpg')
        self.rules_path = os.path.join(self.script_dir, 'resources', 'rules.txt')
        self.menu_background_image = ImageTk.PhotoImage(Image.open(self.menu_background_path).resize((1200, 800)))
        self.game_background_image = ImageTk.PhotoImage(Image.open(self.game_background_path).resize((1200, 800)))
        self.corona_image = ImageTk.PhotoImage(Image.open(self.corona_image_path).resize((200, 300)))
        self.current_frame = None
        self.show_menu()

    def show_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        background_label = Label(self.current_frame, image=self.menu_background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        corona_label = Label(self.current_frame, image=self.corona_image)
        corona_label.place(x=500, y=300)
        temp_game_ui = GameUI(GameSetup(self.root))
        button_width = 200
        menu_button_y = 400
        button_font = ("Arial", 12, "bold")
        self.create_button(temp_game_ui, "Nowa gra", 130, menu_button_y - 100, button_width, self.start_game, button_font)
        self.create_button(temp_game_ui, "Najlepsze wyniki", 130, menu_button_y - 50, button_width, None, button_font)
        self.create_button(temp_game_ui, "Zasady Gry", 130, menu_button_y, button_width, self.show_game_rules, button_font)
        self.create_button(temp_game_ui, "Samouczek", 130, menu_button_y + 50, button_width, None, button_font)
        self.create_button(temp_game_ui, "Zmiana Motywu", 130, menu_button_y + 100, button_width, None, button_font)

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

        game_setup = GameSetup(self.root)
        user_interface = GameUI(game_setup)

        user_interface.create_button("Nowa gra", 130, 16, 119, game_setup.reset_game)
        user_interface.create_button("Cofnij", 265, 16, 119)
        user_interface.create_label("Punkty: 1000", 711, 16, 119)
        user_interface.create_label("Ruchy: 230", 846, 16, 119)
        user_interface.create_label("Czas: 00:00", 981, 16, 119)
        user_interface.create_button("Najlepsze wyniki", 16, 753, 200)

        for x, y in [(130, 153), (270, 153), (550, 153), (690, 153), (830, 153), (970, 153),
                     (130, 378), (270, 378), (410, 378), (550, 378), (690, 378), (830, 378), (970, 378)]:
            user_interface.create_placeholder(x, y)

        game_setup.reset_game()

if __name__ == "__main__":
    root = Tk()
    app = PasjansApp(root)
    root.mainloop()
