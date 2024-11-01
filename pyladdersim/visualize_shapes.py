class LadderShapes:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_contact(self, x, y, color="black"):
        # Contact shape as before
        self.canvas.create_line(x - 10, y, x + 10, y, width=2, fill=color)
        self.canvas.create_line(x - 10, y - 10, x - 10, y + 10, width=2, fill=color)
        self.canvas.create_line(x + 10, y - 10, x + 10, y + 10, width=2, fill=color)

    def draw_inverted_contact(self, x, y, color="black"):
        # Inverted contact with a slash
        self.draw_contact(x, y, color)
        self.canvas.create_line(x - 8, y - 8, x + 8, y + 8, width=2, fill=color)

    def draw_coil(self, x, y, color="black"):
        # Coil as before
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, width=2, fill=color)

    def draw_timer(self, x, y, timer_type="TON", color="black"):
        """Draw a timer with labeled I/O points based on IEC 61131-3 standards."""
        # Rectangle for timer
        self.canvas.create_rectangle(x - 30, y - 10, x + 30, y + 30, width=2, fill=color)
        # Label for timer type (TON, TOF, TP)
        self.canvas.create_text(x, y - 20, text=timer_type, fill=color)

        # Input labels on the left
        self.canvas.create_text(x - 35, y - 10, text="IN", anchor="e", fill=color)
        self.canvas.create_text(x - 35, y + 10, text="PT", anchor="e", fill=color)

        # Output labels on the right
        self.canvas.create_text(x + 35, y - 10, text="Q", anchor="w", fill=color)
        self.canvas.create_text(x + 35, y + 10, text="ET", anchor="w", fill=color)
