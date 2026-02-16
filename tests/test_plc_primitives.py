from pyladdersim.components import (
    Contact,
    CounterDown,
    CounterUp,
    FallingEdgeContact,
    Output,
    RetentiveOutput,
    RisingEdgeContact,
)
from pyladdersim.ladder import Ladder, Rung


def test_rising_edge_contact_pulses_once_per_rising_edge():
    one_shot = RisingEdgeContact("ONS")
    assert one_shot.evaluate() is False

    one_shot.activate()
    assert one_shot.evaluate() is True
    assert one_shot.evaluate() is False

    one_shot.deactivate()
    assert one_shot.evaluate() is False

    one_shot.activate()
    assert one_shot.evaluate() is True


def test_rising_edge_contact_supports_direct_input_evaluation():
    one_shot = RisingEdgeContact("ONS")
    assert one_shot.evaluate(IN=False) is False
    assert one_shot.evaluate(IN=True) is True
    assert one_shot.evaluate(IN=True) is False
    assert one_shot.evaluate(IN=False) is False
    assert one_shot.evaluate(IN=True) is True


def test_falling_edge_contact_pulses_once_per_falling_edge():
    one_shot = FallingEdgeContact("FNS")

    one_shot.activate()
    assert one_shot.evaluate() is False
    assert one_shot.evaluate() is False

    one_shot.deactivate()
    assert one_shot.evaluate() is True
    assert one_shot.evaluate() is False


def test_falling_edge_contact_supports_direct_input_evaluation():
    one_shot = FallingEdgeContact("FNS")
    assert one_shot.evaluate(IN=True) is False
    assert one_shot.evaluate(IN=True) is False
    assert one_shot.evaluate(IN=False) is True
    assert one_shot.evaluate(IN=False) is False


def test_retentive_output_latches_until_reset():
    coil = RetentiveOutput("Latch")
    assert coil.evaluate(False) is False
    assert coil.evaluate(True) is True
    assert coil.evaluate(False) is True
    assert coil.reset() is False


def test_retentive_output_supports_explicit_reset_inputs():
    coil = RetentiveOutput("Latch")
    assert coil.evaluate(IN=True) is True
    assert coil.evaluate(IN=False) is True
    assert coil.evaluate(reset=True) is False
    assert coil.evaluate(IN=True) is True
    assert coil.evaluate(R=True) is False


def test_counter_up_counts_rising_edges():
    counter = CounterUp(name="CTU", preset=2)
    assert counter.evaluate(False) is False
    assert counter.CV == 0

    assert counter.evaluate(True) is False
    assert counter.CV == 1

    # Held high should not increment.
    assert counter.evaluate(True) is False
    assert counter.CV == 1

    assert counter.evaluate(False) is False
    assert counter.evaluate(True) is True
    assert counter.CV == 2

    counter.reset()
    assert counter.CV == 0
    assert counter.state is False


def test_counter_up_supports_cu_reset_and_runtime_preset():
    counter = CounterUp(name="CTU", preset=2)

    assert counter.evaluate(CU=True) is False
    assert counter.CV == 1
    assert counter.evaluate(CU=True) is False
    assert counter.CV == 1
    assert counter.evaluate(CU=False) is False
    assert counter.evaluate(CU=True) is True
    assert counter.CV == 2

    assert counter.evaluate(IN=True, R=True) is False
    assert counter.CV == 0

    assert counter.evaluate(IN=False, PV=1) is False
    assert counter.evaluate(IN=True) is True
    assert counter.CV == 1


def test_counter_down_counts_to_zero():
    counter = CounterDown(name="CTD", preset=3)
    assert counter.CV == 3
    assert counter.state is False

    for expected in (2, 1, 0):
        assert counter.evaluate(True) is (expected == 0)
        assert counter.CV == expected
        assert counter.evaluate(False) is (expected == 0)

    counter.reset()
    assert counter.CV == 3
    assert counter.state is False


def test_counter_down_supports_cd_load_reset_and_runtime_preset():
    counter = CounterDown(name="CTD", preset=2)

    assert counter.evaluate(CD=True) is False
    assert counter.CV == 1
    assert counter.evaluate(CD=True) is False
    assert counter.CV == 1
    assert counter.evaluate(CD=False) is False
    assert counter.evaluate(CD=True) is True
    assert counter.CV == 0

    assert counter.evaluate(IN=False, PV=3) is True
    assert counter.evaluate(LD=True) is False
    assert counter.CV == 3

    assert counter.evaluate(CD=False, R=True) is False
    assert counter.CV == 3


def test_ladder_scan_once_evaluates_single_cycle():
    start = Contact("Start")
    lamp = Output("Lamp")
    rung = Rung([start, lamp])
    ladder = Ladder()
    ladder.add_rung(rung)

    assert ladder.scan_once() is False
    start.activate()
    assert ladder.scan_once() is True
