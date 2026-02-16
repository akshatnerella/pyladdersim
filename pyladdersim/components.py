class Component:
    """Base class for all ladder components."""

    def __init__(self, name):
        self.name = name
        self.state = False

    def evaluate(self):
        return self.state

    def status(self):
        return "TRUE" if self.state else "FALSE"


class Contact(Component):
    """Normally-open contact."""

    def activate(self):
        self.state = True

    def deactivate(self):
        self.state = False


class InvertedContact(Component):
    """Normally-closed contact."""

    def __init__(self, name):
        super().__init__(name)
        self.state = True

    def activate(self):
        self.state = False

    def deactivate(self):
        self.state = True


class RisingEdgeContact(Contact):
    """One-shot contact that is TRUE for one scan on a rising edge."""

    def __init__(self, name):
        super().__init__(name)
        self._previous_state = False

    def evaluate(self, IN=None):
        if IN is not None:
            self.state = bool(IN)

        pulse = self.state and not self._previous_state
        self._previous_state = self.state
        return pulse

    def reset(self):
        self._previous_state = self.state


class FallingEdgeContact(Contact):
    """One-shot contact that is TRUE for one scan on a falling edge."""

    def __init__(self, name):
        super().__init__(name)
        self._previous_state = False

    def evaluate(self, IN=None):
        if IN is not None:
            self.state = bool(IN)

        pulse = self._previous_state and not self.state
        self._previous_state = self.state
        return pulse

    def reset(self):
        self._previous_state = self.state


class Output(Component):
    """Standard output coil."""

    def evaluate(self, input_state):
        self.state = bool(input_state)
        return self.state


class RetentiveOutput(Output):
    """
    Retentive output coil (latch).
    - TRUE input latches the output ON.
    - FALSE input leaves the output unchanged.
    """

    def evaluate(self, input_state=False, IN=None, reset=False, R=False):
        if IN is not None:
            input_state = IN

        if reset or R:
            self.state = False
        elif input_state:
            self.state = True
        return self.state

    def reset(self):
        self.state = False
        return self.state


class FunctionBlock(Component):
    """Base component for PLC blocks that consume an input signal."""

    def update(self, IN):
        return self.evaluate(IN=IN)

    def evaluate(self, IN):
        raise NotImplementedError


class Timer(FunctionBlock):
    """Base timer class with IEC-like PT/ET/Q fields."""

    def __init__(self, name, delay=None, PT=None):
        super().__init__(name)
        if delay is None and PT is None:
            raise ValueError("Timer requires 'delay' or 'PT'.")
        if delay is not None and PT is not None and delay != PT:
            raise ValueError("Provide either 'delay' or matching 'PT'.")

        preset = delay if delay is not None else PT
        if preset < 0:
            raise ValueError("Timer preset must be >= 0.")

        self.PT = int(preset)
        self.ET = 0
        self.Q = False
        self._previous_in = False

    @property
    def state(self):
        return self.Q

    @state.setter
    def state(self, value):
        self.Q = bool(value)

    def reset(self):
        self.ET = 0
        self.Q = False
        self._previous_in = False


class OnDelayTimer(Timer):
    """TON: Q becomes TRUE after IN is TRUE for PT scans."""

    def evaluate(self, IN):
        if IN:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = True
        else:
            self.reset()
        return self.Q


class OffDelayTimer(Timer):
    """TOF: Q stays TRUE for PT scans after IN goes FALSE."""

    def evaluate(self, IN):
        if IN:
            self.Q = True
            self.ET = 0
        else:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = False
        return self.Q


class PulseTimer(Timer):
    """TP: Q pulses TRUE for PT scans on a rising edge of IN."""

    def evaluate(self, IN):
        rising_edge = IN and not self._previous_in
        if rising_edge:
            self.ET = 0
            self.Q = True
        elif self.Q:
            self.ET += 1
            if self.ET >= self.PT:
                self.Q = False

        self._previous_in = IN
        return self.Q


class Counter(FunctionBlock):
    """Base counter with IEC-like PV/CV/Q fields."""

    def __init__(self, name, preset, current_value=0):
        super().__init__(name)
        if preset < 0:
            raise ValueError("Counter preset must be >= 0.")

        self.PV = int(preset)
        self.CV = int(current_value)
        self.Q = False
        self._previous_in = False
        self._update_done()

    @property
    def state(self):
        return self.Q

    @state.setter
    def state(self, value):
        self.Q = bool(value)

    def _update_done(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class CounterUp(Counter):
    """CTU: increments CV on each rising edge, Q is TRUE when CV >= PV."""

    def __init__(self, name, preset, current_value=0):
        super().__init__(name=name, preset=preset, current_value=current_value)

    def _update_done(self):
        self.Q = self.CV >= self.PV

    def evaluate(self, IN=False, CU=None, R=False, PV=None):
        if CU is not None:
            IN = CU
        IN = bool(IN)

        if PV is not None:
            if PV < 0:
                raise ValueError("Counter preset must be >= 0.")
            self.PV = int(PV)

        if R:
            self.CV = 0
        else:
            rising_edge = IN and not self._previous_in
            if rising_edge:
                self.CV += 1

        self._update_done()
        self._previous_in = IN
        return self.Q

    def reset(self):
        self.CV = 0
        self._previous_in = False
        self._update_done()


class CounterDown(Counter):
    """CTD: decrements CV on each rising edge, Q is TRUE when CV <= 0."""

    def __init__(self, name, preset, current_value=None):
        start_value = preset if current_value is None else current_value
        super().__init__(name=name, preset=preset, current_value=start_value)

    def _update_done(self):
        self.Q = self.CV <= 0

    def evaluate(self, IN=False, CD=None, LD=False, R=False, PV=None):
        if CD is not None:
            IN = CD
        IN = bool(IN)

        if PV is not None:
            if PV < 0:
                raise ValueError("Counter preset must be >= 0.")
            self.PV = int(PV)

        if LD or R:
            self.CV = self.PV
        else:
            rising_edge = IN and not self._previous_in
            if rising_edge and self.CV > 0:
                self.CV -= 1

        self._update_done()
        self._previous_in = IN
        return self.Q

    def reset(self):
        self.CV = self.PV
        self._previous_in = False
        self._update_done()
