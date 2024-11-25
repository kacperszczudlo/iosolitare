import os
from tkinter import *
from PIL import Image, ImageTk
from gameSetup import GameSetup
from gameUI import  GameUI

script_dir = os.path.dirname(os.path.abspath(__file__))

width, height = 1200, 800
window = Tk()
window.title("Pasjans Inzynieria Oprogramowania")
window.geometry(f"{width}x{height}")
window.resizable(False, False)

background_path = os.path.join(script_dir, 'resources', 'background.jpg')
background = Image.open(background_path).resize((width, height))
background_image = ImageTk.PhotoImage(background)
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

game_setup  = GameSetup(window)
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

window.mainloop()