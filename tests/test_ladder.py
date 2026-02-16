import pytest

from pyladdersim.components import (
    Contact,
    FallingEdgeContact,
    InvertedContact,
    Output,
    RisingEdgeContact,
)
from pyladdersim.ladder import Ladder, Rung


def test_rung_evaluates_series_logic():
    start = Contact("Start")
    stop = InvertedContact("Stop")
    lamp = Output("Lamp")
    rung = Rung([start, stop, lamp])

    assert rung.evaluate() is False

    start.activate()
    assert rung.evaluate() is True

    stop.activate()
    assert rung.evaluate() is False


def test_rung_requires_single_output():
    start = Contact("Start")
    lamp_1 = Output("Lamp1")
    lamp_2 = Output("Lamp2")

    with pytest.raises(ValueError, match="only one output"):
        Rung([start, lamp_1, lamp_2])


def test_rung_requires_output_component():
    start = Contact("Start")
    stop = InvertedContact("Stop")

    with pytest.raises(ValueError, match="must have an output"):
        Rung([start, stop])


def test_ladder_run_requires_positive_cycle_time():
    ladder = Ladder()

    with pytest.raises(ValueError, match="cycle_time"):
        ladder.run(cycle_time=0)


def test_rung_scans_rising_edge_contact_even_when_upstream_is_false():
    upstream = Contact("Upstream")
    one_shot = RisingEdgeContact("ONS")
    lamp = Output("Lamp")
    rung = Rung([upstream, one_shot, lamp])

    assert rung.evaluate() is False

    # Rising edge occurs while upstream is FALSE; it must still be scanned.
    one_shot.activate()
    assert rung.evaluate() is False

    # Enabling upstream later should not create a stale pulse.
    upstream.activate()
    assert rung.evaluate() is False

    # A new rising edge with upstream enabled should pulse once.
    one_shot.deactivate()
    assert rung.evaluate() is False
    one_shot.activate()
    assert rung.evaluate() is True


def test_rung_scans_falling_edge_contact_even_when_upstream_is_false():
    upstream = Contact("Upstream")
    one_shot = FallingEdgeContact("FNS")
    lamp = Output("Lamp")
    rung = Rung([upstream, one_shot, lamp])

    assert rung.evaluate() is False

    # Falling edge occurs while upstream is FALSE; it must still be scanned.
    one_shot.activate()
    assert rung.evaluate() is False
    one_shot.deactivate()
    assert rung.evaluate() is False

    # Enabling upstream later should not create a stale pulse.
    upstream.activate()
    assert rung.evaluate() is False

    # A new falling edge with upstream enabled should pulse once.
    one_shot.activate()
    assert rung.evaluate() is False
    one_shot.deactivate()
    assert rung.evaluate() is True
