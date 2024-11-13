import os
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from cardDeck import CardDeck
from firstDeal import FirstDeal

class GameSetup:
    def __init__(self, window):
        # Inicjalizuje grę, okno oraz talię kart.
        self.window = window
        self.card_labels = []
        self.deck = CardDeck()
        self.card_positions = []

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(script_dir, 'resources')
        self.cards_dir = os.path.join(self.resources_dir, 'cards')

        self.lower_stack_areas = [
    {'x': 130, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 270, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 410, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 550, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 690, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 830, 'y': 378, 'width': 100, 'height': 145},  
    {'x': 970, 'y': 378, 'width': 100, 'height': 145}, 
]

        self.upper_stack_areas = [
    {'x': 130, 'y': 153, 'width': 100, 'height': 145},
    {'x': 270, 'y': 153, 'width': 100, 'height': 145},
    {'x': 550, 'y': 153, 'width': 100, 'height': 145},
    {'x': 690, 'y': 153, 'width': 100, 'height': 145},
    {'x': 830, 'y': 153, 'width': 100, 'height': 145},
    {'x': 970, 'y': 153, 'width': 100, 'height': 145},
]

    def create_button(self, text, x, y, width, command=None):
        # Tworzy przycisk w interfejsie użytkownika.
        button = Button(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        # Tworzy etykietę tekstową w interfejsie użytkownika.
        label = Label(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)

    def create_placeholder(self, x, y):
        # Umieszcza obraz zastępczy w interfejsie.
        placeholder_path = os.path.join(self.resources_dir, 'placeholder.png')
        placeholder_image = Image.open(placeholder_path).resize((100, 145))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)
        placeholder_label = Label(self.window, image=placeholder_photo, bd=0)
        placeholder_label.image = placeholder_photo
        placeholder_label.place(x=x, y=y)
    
    def create_card(self, x, y, card):
        # Tworzy i wyświetla kartę na planszy gry.
        card_image_path = os.path.join(self.cards_dir, os.path.basename(card.get_image()))
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
        # Wyświetla początkowy układ kart na planszy gry.
        y_offset = 378
        y_spacing = 30

        for col in range(7):
            x_position = 131 + col * 140
            for row, card in enumerate(columns[col]):
                y_position = y_offset + row * y_spacing
                card_label = self.create_card(x_position, y_position, card)
                self.card_labels.append(card_label)
                self.update_card_position(card, x_position, y_position)

    def display_stock_pile(self):
        # Wyświetla stos kart rezerwowych (niewykorzystane karty).
        stock_pile_x, stock_pile_y = 131, 153
        for i in range(len(self.first_deal.columns) * (len(self.first_deal.columns) + 1) // 2, len(self.deck.cards)):
            self.deck.cards[i].hide()
            card_label = self.create_card(stock_pile_x, stock_pile_y, self.deck.cards[i])
            self.card_labels.append(card_label)

    def reset_game(self):
        # Usunięcie wszystkich kart z planszy
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()
        self.deck = CardDeck()
        self.deck.shuffle_deck()
        self.first_deal = FirstDeal(self.deck)

        columns = self.first_deal.setup_initial_layout()
        errors = self.first_deal.validate_initial_layout()

        if errors:
            ignore = messagebox.askyesno(
                "Błąd układu początkowego",
                f"Znaleziono błędy:\n{'\n'.join(errors)}\nCzy chcesz kontynuować mimo to?"
            )
            if not ignore:
                return
            
        self.display_initial_deal(columns)
        self.display_stock_pile()

        self.update_lower_stack_areas()


    def on_card_click(self, event):
        # Obsługuje kliknięcie na kartę (zapamiętuje jej pozycję, jeśli jest odkryta).
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
        # Obsługuje przeciąganie karty po planszy.
        if self.selected_card:
            new_x = event.widget.winfo_x() + (event.x - self.start_offset_x)
            new_y = event.widget.winfo_y() + (event.y - self.start_offset_y)
            event.widget.place(x=new_x, y=new_y)
            self.start_x = new_x
            self.start_y = new_y
    
    def update_lower_stack_areas(self):
        # Definicja stałych miejsc na dole (placeholdery)
        placeholder_positions = [
            {'x': 130, 'y': 378, 'width': 100, 'height': 145},
            {'x': 270, 'y': 378, 'width': 100, 'height': 145},
            {'x': 410, 'y': 378, 'width': 100, 'height': 145},
            {'x': 550, 'y': 378, 'width': 100, 'height': 145},
            {'x': 690, 'y': 378, 'width': 100, 'height': 145},
            {'x': 830, 'y': 378, 'width': 100, 'height': 145},
            {'x': 970, 'y': 378, 'width': 100, 'height': 145},
        ]

        self.lower_stack_areas = placeholder_positions

        for position in self.card_positions:
            area = {
                'x': position['x'],
                'y': position['y'],
                'width': position['width'],
                'height': position['height'],
                'card': position['card']
            }
            self.lower_stack_areas.append(area)

    def on_card_release(self, event):
        # Obsługuje zdarzenie zwolnienia karty przez użytkownika po przeciągnięciu.
        if self.selected_card:
            card_x = event.widget.winfo_x()
            card_y = event.widget.winfo_y()
            card_width = event.widget.winfo_width()
            card_height = event.widget.winfo_height()

            card_rect = {'x': card_x, 'y': card_y, 'width': card_width, 'height': card_height}

            collision_found = False

            for area in self.lower_stack_areas:
                if 'card' in area and area['card'] == self.selected_card:
                    continue
                if self.rectangles_overlap(card_rect, area):
                    collision_found = True
                    print('true')
                    break

            if not collision_found:
                print('false')

            self.lower_stack_areas = [
                area for area in self.lower_stack_areas if 'card' not in area or area['card'] != self.selected_card
            ]

            new_area = {'x': card_x, 'y': card_y, 'width': card_width, 'height': card_height, 'card': self.selected_card}
            self.lower_stack_areas.append(new_area)
            self.update_card_position(self.selected_card, card_x, card_y)
            self.selected_card = None
    
    def update_card_position(self, card, x, y):
        # Usuń starą pozycję karty
        self.card_positions = [
            position for position in self.card_positions if position['card'] != card
        ]

        self.card_positions.append({
            'card': card,
            'x': x,
            'y': y,
            'width': 100,  
            'height': 145 
        })

    def update_column_positions(self, column_index):
        # Aktualizuje pozycje kart w podanej kolumnie
        y_offset = 378
        y_spacing = 30
        x_position = 131 + column_index * 140

        for row_index, card in enumerate(self.first_deal.columns[column_index]):
            y_position = y_offset + row_index * y_spacing
            for label in self.card_labels:
                if label.card_object == card:
                    label.place(x=x_position, y=y_position)
                    break

    def rectangles_overlap(self, rect1, rect2):
        # Sprawdza, czy dwa prostokąty nachodzą się w osi X i Y
        overlap_x = rect1['x'] < rect2['x'] + rect2['width'] and rect1['x'] + rect1['width'] > rect2['x']
        overlap_y = rect1['y'] < rect2['y'] + rect2['height'] and rect1['y'] + rect1['height'] > rect2['y']
        return overlap_x and overlap_y

    def is_valid_move(self):
        # TODO: Sprawdza poprawność ruchu karty.
        return True

    def place_in_column(self, x, y):
        # TODO: Umieszcza kartę w odpowiedniej kolumnie po wykonaniu ruchu.
        pass
    
   
