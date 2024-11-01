# pyladdersim/visualizer.py

import tkinter as tk
from pyladdersim.visualize_shapes import LadderShapes
from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer, OffDelayTimer, PulseTimer

class LadderVisualizer:
    def __init__(self, ladder):
        self.ladder = ladder
        self.window = tk.Tk()  # Ensure this is the only instance of Tk()
        self.window.title("Ladder Logic Visualization")

        # Canvas for drawing ladder and rungs
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="white")
        self.canvas.pack()

        # Bind Q to close the window
        self.window.bind("q", lambda e: self.stop())
        self.window.bind("Q", lambda e: self.stop())

        # Instantiate LadderShapes for drawing components
        self.shapes = LadderShapes(self.canvas)

    def update_visualization(self):
        """Updates the ladder visualization to reflect current states."""
        # Clear the canvas before redrawing
        self.canvas.delete("all")

        # Draw the power rails
        self.canvas.create_line(50, 20, 50, 380, fill="black", width=3)
        self.canvas.create_line(550, 20, 550, 380, fill="black", width=3)

        # Define colors for ON/OFF states
        on_color = "#00FF00"  # Bright green
        off_color = "#FF0000"  # Bright red

        for idx, rung in enumerate(self.ladder.rungs):
            y_position = 50 + idx * 70  # Vertical position for each rung

            # Draw the horizontal line for the rung
            rung_color = on_color if rung.evaluate() else off_color
            self.canvas.create_line(50, y_position, 550, y_position, fill=rung_color, width=2)

            # Position components along the rung
            x_position = 100
            for component in rung.components[:-1]:
                if isinstance(component, OnDelayTimer):
                    self.shapes.draw_timer(x_position, y_position, timer_type="TON", color=on_color if component.Q else off_color)

                elif isinstance(component, OffDelayTimer):
                    self.shapes.draw_timer(x_position, y_position, timer_type="TOF", color=on_color if component.Q else off_color)

                elif isinstance(component, PulseTimer):
                    self.shapes.draw_timer(x_position, y_position, timer_type="TP", color=on_color if component.Q else off_color)

                elif isinstance(component, Contact):
                    self.shapes.draw_contact(x_position, y_position, color=on_color if component.state else off_color)
                    self.canvas.create_text(x_position, y_position - 20, text=component.name, fill=on_color if component.state else off_color)
                elif isinstance(component, InvertedContact):
                    self.shapes.draw_inverted_contact(x_position, y_position, color=on_color if component.state else off_color)
                    self.canvas.create_text(x_position, y_position - 20, text=component.name, fill=on_color if component.state else off_color)
                x_position += 100  # Move x position for the next component

            # Align the output component to the right side
            output_component = rung.components[-1]
            output_color = on_color if output_component.state else off_color
            if isinstance(output_component, Output):
                self.shapes.draw_coil(500, y_position, color=output_color)
                self.canvas.create_text(500, y_position - 20, text=output_component.name, fill=output_color)

        # Update the Tkinter window to reflect changes
        self.window.update_idletasks()
        self.window.update()

    def stop(self):
        """Closes the Tkinter window."""
        self.window.destroy()
