from tkinter import Label, Button
from PIL import Image, ImageTk
from cardDeck import CardDeck
from firstDeal import FirstDeal


class GameSetup:
    def __init__(self, window):
        self.selected_card_object = None
        self.window = window
        self.card_labels = []
        self.deck = CardDeck()
        self.selected_card = None
        self.start_x = 0
        self.start_y = 0
        self.start_click_x = 0
        self.start_click_y = 0
        self.selected_stack = []
        self.columns = [[] for _ in range(7)]  # 7 tableau columns
        self.foundations = [[] for _ in range(4)]  # 4 foundation piles

        # Define foundation positions as class attribute
        self.foundation_positions = [
            (550, 153),  # x, y for first foundation pile
            (690, 153),  # x, y for second foundation pile
            (830, 153),  # x, y for third foundation pile
            (970, 153)   # x, y for fourth foundation pile
        ]

    def create_button(self, text, x, y, width, command=None):
        button = Button(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                        bg="#5C4033", state="normal", command=command)
        button.place(x=x, y=y, width=width, height=31)

    def create_label(self, text, x, y, width):
        label = Label(self.window, text=text, font=("Arial", 12, "bold"), fg="white", bd=0, highlightthickness=0,
                      bg="#5C4033")
        label.place(x=x, y=y, width=width, height=31)

    def create_placeholder(self, x, y):
        placeholder_image = Image.open("resources/placeholder.png").resize((100, 145))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)
        placeholder_label = Label(self.window, image=placeholder_photo, bd=0)
        placeholder_label.image = placeholder_photo
        placeholder_label.place(x=x, y=y)

    def create_card(self, x, y, card):
        card_image_path = card.get_image()
        card_image = Image.open(card_image_path).resize((100, 145))
        card_photo = ImageTk.PhotoImage(card_image)
        card_label = Label(self.window, image=card_photo, bd=0)
        card_label.image = card_photo
        card_label.place(x=x, y=y)

        # Associate the Card object with the Label widget
        card_label.card_object = card

        # Bind the mouse events for dragging
        card_label.bind("<Button-1>", self.on_card_click)
        card_label.bind("<B1-Motion>", self.on_card_drag)
        card_label.bind("<ButtonRelease-1>", self.on_card_release)
        return card_label

    def display_initial_deal(self, columns):
        y_offset = 378
        y_spacing = 30

        for col in range(7):
            x_position = 131 + col * 140
            for row, card in enumerate(columns[col]):
                y_position = y_offset + row * y_spacing
                card_label = self.create_card(x_position, y_position, card)
                self.card_labels.append(card_label)
                self.columns[col].append(card_label)

    def display_stock_pile(self):
        stock_pile_x, stock_pile_y = 131, 153
        for i in range(len(self.first_deal.columns) * (len(self.first_deal.columns) + 1) // 2, len(self.deck.cards)):
            self.deck.cards[i].hide()
            card_label = self.create_card(stock_pile_x, stock_pile_y, self.deck.cards[i])
            self.card_labels.append(card_label)

    def reset_game(self):
        for label in self.card_labels:
            label.place_forget()
        self.card_labels.clear()

        self.deck = CardDeck()
        self.deck.shuffle_deck()

        self.first_deal = FirstDeal(self.deck)
        columns = self.first_deal.setup_initial_layout()
        self.display_initial_deal(columns)
        self.display_stock_pile()

    def on_card_click(self, event):
        self.selected_card = event.widget
        self.selected_card_object = getattr(self.selected_card, 'card_object', None)

        if self.selected_card_object is not None and self.selected_card_object.revealed:
            # Store initial position of the card and initial click position
            self.start_x = self.selected_card.winfo_x()
            self.start_y = self.selected_card.winfo_y()
            self.start_click_x = event.x_root
            self.start_click_y = event.y_root
            self.selected_stack = self.get_revealed_stack(self.selected_card_object)

    def on_card_drag(self, event):
        if self.selected_card and self.selected_card_object.revealed:
            # Calculate new position based on the absolute position of the mouse
            dx = event.x_root - self.start_click_x
            dy = event.y_root - self.start_click_y
            for i, card_label in enumerate(self.selected_stack):
                x = self.start_x + dx
                y = self.start_y + dy + i * 30
                card_label.place(x=x, y=y)

    def on_card_release(self, event):
        dropped_x, dropped_y = self.selected_card.winfo_x(), self.selected_card.winfo_y()

        if self.is_valid_move(dropped_x, dropped_y, self.selected_card_object):
            self.place_card_in_column(dropped_x, dropped_y, self.selected_card_object)
        else:
            # Return cards to their original position if the move is invalid
            for i, card_label in enumerate(self.selected_stack):
                card_label.place(x=self.start_x, y=self.start_y + i * 30)

        # After moving the selected stack, reveal the last card in the original column if necessary
        original_column = self.get_column_from_position(self.start_x, self.start_y)
        if original_column and len(original_column) > 0:
            last_card_label = original_column[-1]
            last_card = last_card_label.card_object
            if not last_card.revealed:
                last_card.reveal()  # Reveal the card
                # Update the image to show the front of the card
                card_image = Image.open(last_card.get_image()).resize((100, 145))
                card_photo = ImageTk.PhotoImage(card_image)
                last_card_label.configure(image=card_photo)
                last_card_label.image = card_photo  # Keep a reference to avoid garbage collection

        # Reset the selected card and stack variables
        self.selected_card = None
        self.selected_card_object = None
        self.selected_stack = []

    def is_valid_move(self, x, y, card):
        """
        Check if the card move is valid based on Solitaire rules.
        """
        target_column = self.get_column_from_position(x, y)
        if target_column is not None:
            return self.is_valid_tableau_move(card, target_column)
        else:
            return self.is_valid_foundation_move(card, x, y)

    def is_valid_tableau_move(self, card, target_column):
        """
        Validate moves within tableau columns (alternating colors and descending order).
        """
        if len(target_column) == 0:
            return card.figure.startswith("king")  # Only allow Kings in empty tableau columns

        top_card = target_column[-1].card_object
        return (
                self.is_alternating_color(card, top_card) and
                card.points == top_card.points - 1
        )

    def is_valid_foundation_move(self, card, x, y):
        """
        Validate moves to the foundation piles (ascending order, same suit).
        """
        target_foundation = self.get_foundation_from_position(x, y)
        if target_foundation is None:
            return False

        # If the foundation pile is empty, only allow Aces
        if len(target_foundation) == 0:
            return card.figure.lower().startswith("ace")

        # Ensure the move is in the same suit and in ascending order
        top_card = target_foundation[-1].card_object
        return (
                card.figure.split()[-1] == top_card.figure.split()[-1] and  # Same suit
                card.points == top_card.points + 1  # Ascending order
        )

    def place_card_in_column(self, x, y, card):
        """
        Place the card in the specified column or foundation pile and update internal structure.
        """
        target_column = self.get_column_from_position(x, y)
        if target_column is not None:
            # Place in tableau column
            for card_label in self.selected_stack:
                # Remove from old column
                for col in self.columns:
                    if card_label in col:
                        col.remove(card_label)
                card_label.place_forget()
                target_column.append(card_label)

            # Position each card in the column slightly overlapping the previous card
            base_x = 131 + self.columns.index(target_column) * 140
            if len(target_column) > len(self.selected_stack):
                last_card_y = target_column[-len(self.selected_stack) - 1].winfo_y()
                base_y = last_card_y + 25  # Set overlap offset to 25 pixels
            else:
                base_y = 378  # Default starting y-position for an empty column

            for i, card_label in enumerate(target_column[-len(self.selected_stack):]):
                card_label.place(x=base_x, y=base_y + i * 25)  # 25px offset for the hover effect
        else:
            # Place in foundation pile
            target_foundation = self.get_foundation_from_position(x, y)
            if target_foundation is not None:
                for card_label in self.selected_stack:
                    # Remove from old column
                    for col in self.columns:
                        if card_label in col:
                            col.remove(card_label)
                    card_label.place_forget()
                    target_foundation.append(card_label)

                # Position all cards in the foundation at the same coordinates
                foundation_index = self.foundations.index(target_foundation)
                foundation_x, foundation_y = self.foundation_positions[foundation_index]
                for card_label in target_foundation:
                    card_label.place(x=foundation_x, y=foundation_y)

    def get_column_from_position(self, x, y):
        """
        Determine which tableau column the (x, y) position corresponds to.
        Expands the hitbox for easier placement.
        """
        for col_index, col in enumerate(self.columns):
            column_x = 131 + col_index * 140  # Starting x-coordinate for each column
            # Increase the hitbox to 150px width and 300px height
            if column_x - 25 <= x < column_x + 125 and 378 <= y < 678:
                return col
        return None

    def get_foundation_from_position(self, x, y):
        """
        Determine which foundation pile the (x, y) position corresponds to.
        Expands the hitbox for easier placement.
        """
        # Define the foundation positions as set in the __init__ method
        foundation_positions = self.foundation_positions

        # Increase hitbox to 150px width and 200px height for easier placement
        for foundation, (fx, fy) in zip(self.foundations, foundation_positions):
            if fx - 25 <= x < fx + 125 and fy - 25 <= y < fy + 175:
                return foundation
        return None

    def is_alternating_color(self, card1, card2):
        """
        Check if two cards are of alternating colors.
        """
        red_suits = ["hearts", "diamonds"]
        black_suits = ["clubs", "spades"]

        card1_color = "red" if any(suit in card1.figure for suit in red_suits) else "black"
        card2_color = "red" if any(suit in card2.figure for suit in red_suits) else "black"

        return card1_color != card2_color

    def get_revealed_stack(self, card):
        """
        Find all revealed cards in the stack under the selected card.
        """
        stack = []
        found = False

        # Loop through each column to find the card
        for col in self.columns:
            for card_label in col:
                # Check if we've reached the selected card in this column
                if card_label.card_object == card:
                    found = True

                # If the selected card or any subsequent revealed cards are found, add them to the stack
                if found and card_label.card_object.revealed:
                    stack.append(card_label)

            # Stop once the stack has been built
            if found:
                break

        return stack