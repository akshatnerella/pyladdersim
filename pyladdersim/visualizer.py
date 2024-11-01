# pyladdersim/visualize_ladder.py

import tkinter as tk
from pyladdersim.visualize_shapes import LadderShapes
from pyladdersim.components import Contact, InvertedContact, Output

class LadderVisualizer:
    def __init__(self, ladder):
        self.ladder = ladder
        self.window = tk.Tk()
        self.window.title("Ladder Logic Visualization")

        # Canvas for drawing ladder and rungs
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="white")
        self.canvas.pack()
        
        #Close when Q is pressed
        self.window.bind("q", lambda e: self.window.destroy())
        self.window.bind("Q", lambda e: self.window.destroy())

        # Instantiate LadderShapes for drawing components
        self.shapes = LadderShapes(self.canvas)

        # Draw the vertical power rails (left and right edges)
        self.canvas.create_line(50, 20, 50, 380, fill="black", width=3)
        self.canvas.create_line(550, 20, 550, 380, fill="black", width=3)

        # Start the initial drawing and schedule periodic updates
        self.draw_rungs()

    def draw_rungs(self):
        """Draws each rung with updated colors based on component states."""
        # Clear the canvas before redrawing
        self.canvas.delete("all")

        # Redraw the vertical power rails
        self.canvas.create_line(50, 20, 50, 380, fill="black", width=3)
        self.canvas.create_line(550, 20, 550, 380, fill="black", width=3)

        # Define bright colors for ON/OFF states
        on_color = "#00FF00"  # Bright green
        off_color = "#FF0000"  # Bright red

        for idx, rung in enumerate(self.ladder.rungs):
            y_position = 50 + idx * 70  # Vertical position for each rung

            # Draw the horizontal line for the rung
            rung_color = on_color if rung.evaluate() else off_color  # Determine color based on rung state
            self.canvas.create_line(50, y_position, 550, y_position, fill=rung_color, width=2)

            # Position components along the rung
            x_position = 100  # Starting position for the contacts
            for component in rung.components[:-1]:  # Place all components except the last one
                if isinstance(component, Contact):
                    # Draw contact with the state color
                    self.shapes.draw_contact(x_position, y_position, color=on_color if component.state else off_color)
                    # Create label with appropriate color
                    self.canvas.create_text(x_position, y_position - 20, text=component.name, fill=on_color if component.state else off_color)
                elif isinstance(component, InvertedContact):
                    # Draw inverted contact with the state color
                    self.shapes.draw_inverted_contact(x_position, y_position, color=on_color if component.state else off_color)
                    # Create label with appropriate color
                    self.canvas.create_text(x_position, y_position - 20, text=component.name, fill=on_color if component.state else off_color)
                x_position += 100  # Move x position for the next component

            # Align the output component to the right side
            output_component = rung.components[-1]
            output_color = on_color if output_component.state else off_color  # Determine color based on state
            if isinstance(output_component, Output):
                # Draw coil with the state color
                self.shapes.draw_coil(500, y_position, color=output_color)
                # Create label with appropriate color
                self.canvas.create_text(500, y_position - 20, text=output_component.name, fill=output_color)

        # Schedule the next update of the entire ladder diagram
        self.window.after(1000, self.draw_rungs)  # Refresh every 1 second

    def run(self):
        """Start the visualization loop."""
        self.window.mainloop()