# pyladdersim/components.py

class Component:
    """Base class for all ladder components."""
    def __init__(self, name):
        self.name = name
        self.state = False  # Default state is False

    def evaluate(self):
        """Evaluate the component state."""
        return self.state

    def status(self):
        """Return the component's status as a string."""
        return "TRUE" if self.state else "FALSE"


class Contact(Component):
    """An open contact that passes the signal if activated."""
    def __init__(self, name):
        super().__init__(name)

    def activate(self):
        self.state = True

    def deactivate(self):
        self.state = False


class InvertedContact(Component):
    """A closed contact that blocks the signal if deactivated."""
    def __init__(self, name):
        super().__init__(name)
        self.state = True  # Default state for closed contact is True

    def activate(self):
        self.state = False

    def deactivate(self):
        self.state = True


class Output(Component):
    """An output component that displays the result based on the input state."""
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self, input_state):
        """Set the output state based on the input state."""
        self.state = input_state
        return self.state
