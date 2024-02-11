from time import sleep

import pytest

from secondglass.timer.exceptions import TimerInvalidAction, TimerValueError
from secondglass.timer.msec import Milliseconds
from secondglass.timer.timer import DEFAULT_DURATION, Status, Timer


def test_values() -> None:
    timer = Timer()
    timer.init_duration_text
    timer.duration_left_text
    with pytest.raises(TimerInvalidAction):
        timer.time_since_rang_text
    timer.time_since_rang = Milliseconds(0)
    timer.time_since_rang_text


def test_set_duration() -> None:
    timer = Timer()
    new_duration_text = "1m 23s"
    new_duration = Milliseconds.from_text(new_duration_text)
    timer._set_duration(new_duration)
    assert timer.init_duration == timer.duration_left == new_duration
    timer._set_duration(DEFAULT_DURATION)
    assert timer.init_duration == timer.duration_left == DEFAULT_DURATION
    timer._set_duration(new_duration_text)
    assert timer.init_duration == timer.duration_left == new_duration
    with pytest.raises(TimerValueError):
        timer._set_duration(1.23)  # type: ignore


def test_idle_transitions() -> None:
    # init check
    timer = Timer()
    assert timer.status == Status.IDLE
    assert timer.init_duration == timer.duration_left == DEFAULT_DURATION
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None

    # invalid actions check
    for action in (timer.stop, timer.restart, timer.pause, timer.resume):
        with pytest.raises(TimerInvalidAction):
            print(action)
            action()

    # passive tick check
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None
    assert timer.status == Status.IDLE

    # start action check (active tick)
    new_duration_text = "1m 23s"
    new_duration = Milliseconds.from_text(new_duration_text)
    timer.start(new_duration_text)
    assert timer.init_duration == timer.duration_left == new_duration
    assert timer.status == Status.TICKING
    assert timer.time_since_rang is None
