# pyladdersim/tests/test_ladder.py

from pyladdersim.components import OpenContact, ClosedContact, Output
from pyladdersim.ladder import Ladder, Rung
import threading

def test_components():
    print("Testing Components...")

    # Test OpenContact
    input1 = OpenContact("StartSwitch")
    assert input1.evaluate() == False  # Default state is False
    input1.activate()
    assert input1.evaluate() == True
    input1.deactivate()
    assert input1.evaluate() == False
    print("OpenContact passed.")

    # Test ClosedContact
    input2 = ClosedContact("StopSwitch")
    assert input2.evaluate() == True  # Default state is True
    input2.activate()
    assert input2.evaluate() == False
    input2.deactivate()
    assert input2.evaluate() == True
    print("ClosedContact passed.")

    # Test Output
    output = Output("OutputLight")
    assert output.evaluate(input_state=True) == True
    assert output.evaluate(input_state=False) == False
    print("Output passed.")

def test_rung():
    print("\nTesting Rung...")

    # Create components
    input1 = OpenContact("StartSwitch")
    input2 = ClosedContact("StopSwitch")
    output = Output("OutputLight")

    # Create and validate rung with components
    rung1 = Rung([input1, input2, output])
    assert rung1.evaluate() == False  # No inputs activated
    input1.activate()  # Activate input1
    assert rung1.evaluate() == True  # With input1 active and input2 by default, rung passes
    input1.deactivate()
    assert rung1.evaluate() == False  # Deactivating input1 should deactivate rung again
    print("Rung passed.")

# Run tests
if __name__ == "__main__":
    test_components()
    test_rung()