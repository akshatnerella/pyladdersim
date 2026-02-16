import threading
import time

from pyladdersim.components import FunctionBlock, Output


class Rung:
    """Represents a rung in the ladder logic."""

    def __init__(self, components):
        self.components = components  # List of components (including one Output)
        self.output = None
        self.validate_rung()

    def validate_rung(self):
        """Ensure exactly one output component exists in the rung."""
        outputs = [comp for comp in self.components if isinstance(comp, Output)]
        if len(outputs) > 1:
            raise ValueError("Rung can have only one output component.")
        if len(outputs) == 0:
            raise ValueError("Rung must have an output component.")
        self.output = outputs[0]

    def add_component(self, component):
        """Add a component to the rung, preserving output constraints."""
        if isinstance(component, Output) and self.output is not None:
            raise ValueError("Only one output allowed per rung.")
        self.components.append(component)
        self.validate_rung()

    def evaluate(self):
        """Evaluate components from left to right, then set output."""
        result = True
        for component in self.components:
            if component is self.output:
                continue
            if isinstance(component, FunctionBlock):
                result = component.evaluate(IN=result)
            else:
                # Evaluate every scan to keep stateful contacts in sync,
                # then apply ladder power-flow (AND) semantics.
                component_result = component.evaluate()
                result = result and component_result

        self.output.evaluate(result)
        return self.output.state


class Ladder:
    """The main container for ladder rungs, running in a loop."""

    def __init__(self):
        self.rungs = []
        self.running = False
        self.visualizer = None

    def add_rung(self, rung):
        """Add a new rung to the ladder."""
        self.rungs.append(rung)

    def scan_once(self, visualize=False):
        """Execute one PLC scan cycle and return the ladder output."""
        overall_output = all(rung.evaluate() for rung in self.rungs)

        if visualize:
            if self.visualizer is None:
                from pyladdersim.visualizer import LadderVisualizer

                self.visualizer = LadderVisualizer(self)
            self.visualizer.update_visualization()

        return overall_output

    def run(self, visualize=False, cycle_time=1.0):
        """Run the ladder continuously until stopped."""
        if cycle_time <= 0:
            raise ValueError("cycle_time must be > 0.")

        self.running = True
        print("Ladder is running. Press 'Q' to quit.")

        if visualize and self.visualizer is None:
            # Lazy import keeps Tk dependencies optional for headless environments.
            from pyladdersim.visualizer import LadderVisualizer

            self.visualizer = LadderVisualizer(self)

        quit_thread = threading.Thread(target=self.wait_for_quit, daemon=True)
        quit_thread.start()

        try:
            while self.running:
                overall_output = self.scan_once(visualize=visualize)
                print(f"Ladder Output: {'TRUE' if overall_output else 'FALSE'}")
                time.sleep(cycle_time)
        except KeyboardInterrupt:
            print("\nLadder simulation interrupted.")
            self.stop()

    def wait_for_quit(self):
        """Listen for 'Q' in a separate thread and stop the ladder."""
        while self.running:
            user_input = input().strip().upper()
            if user_input == "Q":
                self.stop()

    def stop(self):
        """Stop the ladder simulation and ensure all threads close."""
        self.running = False
        print("Ladder stopped.")
