# pyladdersim/ladder.py

from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer, OffDelayTimer, PulseTimer
from pyladdersim.visualizer import LadderVisualizer  # Import the visualizer
import threading
import time

class Rung:
    """Represents a rung in the ladder logic."""
    def __init__(self, components):
        self.components = components  # List of components (including one Output)
        self.output = None
        self.validate_rung()

    def validate_rung(self):
        """Ensures only one output component exists and checks for output presence."""
        outputs = [comp for comp in self.components if isinstance(comp, Output)]
        if len(outputs) > 1:
            raise ValueError("Rung can have only one output component.")
        elif len(outputs) == 0:
            raise ValueError("Rung must have an output component.")
        self.output = outputs[0]

    def add_component(self, component):
        """Adds a component to the rung in sequence, ensuring only one output."""
        if isinstance(component, Output) and self.output is not None:
            raise ValueError("Only one output allowed per rung.")
        self.components.append(component)
        self.validate_rung()

    def evaluate(self):
        """Evaluate the rung from left to right and update the output state."""
        result = True  # Start with True for AND logic across all components
        for component in self.components:
            if component != self.output:  # Skip the output during input evaluation
                if isinstance(component, (OnDelayTimer, OffDelayTimer, PulseTimer)):
                    result = result and component.evaluate(IN=True)  # Assume IN=True as example
                else:
                    result = result and component.evaluate()
        
        # Pass the final evaluated result to the output
        self.output.evaluate(result)
        return self.output.state  # Return the output's state to check


# pyladdersim/ladder.py

from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer, OffDelayTimer, PulseTimer
from pyladdersim.visualizer import LadderVisualizer
import threading
import time

class Ladder:
    """The main container for ladder rungs, running in a loop."""
    def __init__(self):
        self.rungs = []
        self.running = False
        self.visualizer = None

    def add_rung(self, rung):
        """Add a new rung to the ladder."""
        self.rungs.append(rung)

    def run(self, visualize=False):
        """Run the ladder, creating threads for each rung and handling the control loop."""
        self.running = True
        print("Ladder is running. Press 'Q' to quit.")

        # Initialize the visualizer only once if visualization is enabled
        if visualize and self.visualizer is None:
            self.visualizer = LadderVisualizer(self)

        # Start a separate thread to handle the quit command
        quit_thread = threading.Thread(target=self.wait_for_quit)
        quit_thread.daemon = True
        quit_thread.start()

        try:
            # Main loop for evaluating rungs and visualizing output
            while self.running:
                overall_output = all(rung.evaluate() for rung in self.rungs)
                print(f"Ladder Output: {'TRUE' if overall_output else 'FALSE'}")

                # Update visualization if enabled
                if visualize and self.visualizer:
                    self.visualizer.update_visualization()

                time.sleep(1)  # Simulate PLC scan delay

        except KeyboardInterrupt:
            print("\nLadder simulation interrupted.")
            self.stop()

    def wait_for_quit(self):
        """Listens for 'Q' input in a separate thread to quit the simulation."""
        while self.running:
            user_input = input().strip().upper()
            if user_input == 'Q':
                self.stop()

    def stop(self):
        """Stop the ladder simulation and ensure all threads close."""
        self.running = False
        print("Ladder stopped.")
