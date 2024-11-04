import tkinter as tk
from PIL import Image, ImageTk
width = 1200
height = 800
window = tk.Tk()
window.title("Pasjans Inzynieria Oprogramowania")
window.geometry(f"{width}x{height}")
window.resizable(False, False)
background = Image.open("resources/background.jpg")
background = background.resize((width,height))
background = ImageTk.PhotoImage(background)

background_label = tk.Label(window, image=background)
background_label.pack()


window.mainloop()