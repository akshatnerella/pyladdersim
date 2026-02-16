

#### This is the base class for all ladder components ####
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



##### This is the timer class, this is a general piece of code to initiate all three types of timers #####
class Timer:
    """Base Timer class with shared attributes and methods for PLC timers."""
    def __init__(self, name, delay):
        self.name = name
        self.PT = delay  # Preset Time in seconds
        self.ET = 0  # Elapsed Time in seconds
        self.Q = False  # Q (done output)

    @property
    def state(self):
        """Compatibility alias used by existing examples/tests."""
        return self.Q

    def reset(self):
        """Resets the timer's internal state."""
        self.ET = 0
        self.Q = False

    def update(self, IN):
        """Compatibility alias that mirrors evaluate(IN)."""
        return self.evaluate(IN)

    def evaluate(self, IN):
        """This method should be overridden in subclasses."""
        pass


class OnDelayTimer(Timer):
    """ON-Delay Timer (TON) - Activates after a delay when input turns ON."""
    def evaluate(self, IN):
        if IN:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = True
        else:
            self.reset()
        return self.Q  # Return the done output state


class OffDelayTimer(Timer):
    """OFF-Delay Timer (TOF) - Deactivates after a delay when input turns OFF."""
    def evaluate(self, IN):
        if IN:
            self.Q = True
            self.ET = 0  # Reset elapsed time when input is ON
        else:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = False
        return self.Q  # Return the done output state


class PulseTimer(Timer):
    """Pulse Timer (TP) - Activates for a fixed duration when input turns ON."""
    def evaluate(self, IN):
        if IN and not self.Q:
            self.ET = 0
            self.Q = True
        elif self.Q:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = False
        return self.Q  # Return the pulse output state
