# pyladdersim/visualize_shapes.py

import tkinter as tk

class LadderShapes:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_contact(self, x, y, color="black"):
        """Draw a regular contact."""
        # Horizontal bar for contact
        self.canvas.create_line(x - 10, y, x + 10, y, width=2, fill=color)
        # Vertical lines for the contact ends
        self.canvas.create_line(x - 10, y - 10, x - 10, y + 10, width=2, fill=color)
        self.canvas.create_line(x + 10, y - 10, x + 10, y + 10, width=2, fill=color)
        # Label
        #self.canvas.create_text(x, y - 20, text=label)

    def draw_inverted_contact(self, x, y, color="black"):
        """Draw an inverted contact."""
        # Horizontal bar with a diagonal slash
        self.draw_contact(x, y, color)
        # Diagonal slash to indicate inverted contact
        self.canvas.create_line(x - 8, y - 8, x + 8, y + 8, width=2, fill=color)

    def draw_coil(self, x, y, color="black"):
        """Draw a regular coil."""
        # Circle for coil
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, width=2, fill=color)