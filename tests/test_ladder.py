# pyladdersim/run_ladder.py

from pyladdersim.components import Contact, InvertedContact, Output
from pyladdersim.ladder import Ladder, Rung
import time
from pyladdersim.visualizer import LadderVisualizer

def setup_ladder():
    # Initialize Ladder
    ladder = Ladder()

    # Define components for the first rung
    input1 = Contact("StartSwitch")
    #input1.activate()  # Activate input1 for testing
    input2 = InvertedContact("StopSwitch")
    output1 = Output("OutputLight1")

    # Create the first rung and add it to the ladder
    rung1 = Rung([input1, input2, output1])
    ladder.add_rung(rung1)

    # Define components for a second rung (optional example)
    input3 = Contact("OverrideSwitch")
    output2 = Output("WarningLight")
    rung2 = Rung([input3, output2])
    ladder.add_rung(rung2)

    return ladder, input1, input2  # Return ladder and inputs for control

# Start the ladder simulation
if __name__ == "__main__":
    ladder, input1, input2 = setup_ladder()
    visualizer = LadderVisualizer(ladder)
    # Run the ladder
    ladder.run()  # Runs in main thread; user-friendly and simple
    visualizer.run()  # Runs in separate thread; visualizes ladder components
