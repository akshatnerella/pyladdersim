# pyladdersim/ladder.py

from pyladdersim.components import OpenContact, ClosedContact, Output
import threading
import time


# pyladdersim/ladder.py

# pyladdersim/ladder.py

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
                result = result and component.evaluate()
        
        # Pass the final evaluated result to the output
        self.output.evaluate(result)
        return self.output.state  # Return the output's state to check


class Ladder:
    """The main container for ladder rungs, running in a loop."""
    def __init__(self):
        self.rungs = []
        self.running = False
        self.rung_threads = []  # Track threads for each rung

    def add_rung(self, rung):
        """Add a new rung to the ladder."""
        self.rungs.append(rung)

    def run(self):
        """Run the ladder, creating threads for each rung and handling the control loop."""
        self.running = True
        print("Ladder is running. Press 'Q' to quit.")

        # Start a thread for each rung
        for rung in self.rungs:
            rung_thread = threading.Thread(target=self.run_rung, args=(rung,))
            rung_thread.daemon = True  # Ensures threads close when the program exits
            rung_thread.start()
            self.rung_threads.append(rung_thread)

        try:
            # Main loop for displaying output and checking quit condition
            while self.running:
                for idx, rung in enumerate(self.rungs):
                    print(f"Rung {idx + 1} output: {rung.output.status()}")
                time.sleep(1)  # Simulate PLC scan delay

                # Check for quit input
                user_input = input("Press 'Q' to quit: ").strip().upper()
                if user_input == 'Q':
                    self.stop()
        except KeyboardInterrupt:
            print("\nLadder simulation interrupted.")
            self.stop()

    def run_rung(self, rung):
        """Continuously evaluate a single rung."""
        while self.running:
            rung.evaluate()
            time.sleep(0.1)  # Simulate scan delay for each rung

    def stop(self):
        """Stop the ladder simulation and ensure all threads close."""
        self.running = False
        print("Ladder stopped.")
