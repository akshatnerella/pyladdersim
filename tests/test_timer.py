from pyladdersim.components import OffDelayTimer, OnDelayTimer, PulseTimer


def test_on_delay_timer_turns_on_after_preset():
    timer = OnDelayTimer(name="TON", delay=3)

    assert timer.evaluate(False) is False
    assert timer.evaluate(True) is False
    assert timer.evaluate(True) is False
    assert timer.evaluate(True) is True
    assert timer.state is True

    assert timer.evaluate(False) is False
    assert timer.ET == 0
    assert timer.state is False


def test_off_delay_timer_turns_off_after_preset():
    timer = OffDelayTimer(name="TOF", delay=2)

    assert timer.evaluate(True) is True
    assert timer.state is True
    assert timer.ET == 0

    assert timer.evaluate(False) is True
    assert timer.ET == 1
    assert timer.evaluate(False) is False
    assert timer.ET == 2

    assert timer.evaluate(True) is True
    assert timer.ET == 0


def test_pulse_timer_holds_true_for_preset_duration():
    timer = PulseTimer(name="TP", delay=3)

    assert timer.evaluate(True) is True
    assert timer.ET == 0
    assert timer.state is True

    assert timer.evaluate(False) is True
    assert timer.ET == 1
    assert timer.evaluate(False) is True
    assert timer.ET == 2
    assert timer.evaluate(False) is False
    assert timer.ET == 3
    assert timer.state is False


def test_timer_update_alias_matches_evaluate():
    timer = OnDelayTimer(name="TON", delay=2)

    assert timer.update(True) is False
    assert timer.update(True) is True
