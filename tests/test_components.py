from pyladdersim.components import Contact, InvertedContact, Output


def test_contact_state_transitions():
    contact = Contact("Start")
    assert contact.evaluate() is False

    contact.activate()
    assert contact.evaluate() is True

    contact.deactivate()
    assert contact.evaluate() is False


def test_inverted_contact_state_transitions():
    contact = InvertedContact("Stop")
    assert contact.evaluate() is True

    contact.activate()
    assert contact.evaluate() is False

    contact.deactivate()
    assert contact.evaluate() is True


def test_output_tracks_input():
    output = Output("Lamp")
    assert output.evaluate(True) is True
    assert output.evaluate(False) is False
