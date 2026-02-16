import pytest

from pyladdersim.components import Contact, InvertedContact, Output
from pyladdersim.ladder import Rung


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
