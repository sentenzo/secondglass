from time import sleep

import pytest

from secondglass.timer.exceptions import TimerInvalidAction, TimerValueError
from secondglass.timer.msec import MSEC_IN_SEC, Milliseconds
from secondglass.timer.timer import DEFAULT_DURATION, Status, Timer


def test_values() -> None:
    timer = Timer()
    timer.init_duration_text
    timer.duration_left_text
    with pytest.raises(TimerInvalidAction):
        timer.time_since_rang_text
    timer.time_since_rang = Milliseconds(0)
    timer.time_since_rang_text

    timer._status = Status.TICKING
    timer.init_duration = Milliseconds(1000)
    timer.duration_left = Milliseconds(1000)
    assert timer.progress == 0.0
    timer.duration_left = Milliseconds(200)
    assert timer.progress == 0.8
    timer.duration_left = Milliseconds(0)
    assert timer.progress == 1.0


def test_set_duration() -> None:
    timer = Timer()
    new_duration_text = "1m 23s"
    new_duration = Milliseconds.from_text(new_duration_text)
    timer._set_duration(new_duration)
    assert timer.init_duration == new_duration
    timer._set_duration(DEFAULT_DURATION)
    assert timer.init_duration == DEFAULT_DURATION
    timer._set_duration(new_duration_text)
    assert timer.init_duration == new_duration
    timer._set_duration(123)
    with pytest.raises(TimerValueError):
        timer._set_duration(1.23)  # type: ignore


def test_idle_transitions() -> None:
    # init check
    timer = Timer()
    assert timer.status == Status.IDLE
    assert timer.init_duration == timer.duration_left == DEFAULT_DURATION
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None
    assert timer.progress == 0.0

    # invalid actions check
    for action in (timer.stop, timer.restart, timer.pause, timer.resume):
        with pytest.raises(TimerInvalidAction):
            action()  # type: ignore

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


def test_ticking_transitions() -> None:
    # init
    small_duration = Milliseconds(100)  # 0.1 sec
    timer = Timer()
    timer.start(small_duration)

    # invalid actions check
    for action in (timer.start, timer.resume):
        with pytest.raises(TimerInvalidAction):
            action()  # type: ignore

    # tick action
    assert timer.init_duration == timer.duration_left
    timer.tick()
    old_last_tick_time = timer.last_tick_time
    sleep(0.01)
    timer.tick()
    assert timer.last_tick_time > old_last_tick_time  # type: ignore
    assert 0 < timer.progress < 1
    assert timer.init_duration > timer.duration_left
    assert timer.status == Status.TICKING
    assert timer.time_since_rang is None
    sleep(small_duration / MSEC_IN_SEC)
    timer.tick()  # transmission into RANG
    assert timer.status == Status.RANG
    assert timer.time_since_rang is not None
    assert timer.duration_left == Milliseconds(0)

    # re-init
    timer = Timer()
    timer.start(small_duration)

    # pause action
    timer.tick()
    assert timer.last_tick_time is not None
    timer.pause()
    assert timer.status == Status.PAUSED
    assert timer.last_tick_time is None

    # re-init
    timer = Timer()
    timer.start(small_duration)

    # restart action
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.init_duration > timer.duration_left
    assert timer.last_tick_time is not None
    assert timer.status == Status.TICKING
    timer.restart()
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.status == Status.TICKING

    # re-init
    timer = Timer()
    timer.start(small_duration)

    # stop action
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.init_duration > timer.duration_left
    assert timer.last_tick_time is not None
    assert timer.status == Status.TICKING
    timer.stop()
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.status == Status.IDLE


def test_paused_transitions() -> None:
    # init
    small_duration = Milliseconds(100)  # 0.1 sec

    def new_paused_timer(check_assert: bool = False) -> Timer:
        timer = Timer()
        timer.start(small_duration)
        timer.tick()
        sleep(0.01)
        timer.tick()
        if check_assert:
            assert timer.status == Status.TICKING
            assert timer.init_duration > timer.duration_left
            assert timer.last_tick_time is not None
        timer.pause()
        if check_assert:
            assert timer.status == Status.PAUSED
            assert timer.init_duration > timer.duration_left
            assert timer.last_tick_time is None
        return timer

    timer = new_paused_timer(True)  # check init

    # invalid actions check
    for action in (timer.start, timer.pause):
        with pytest.raises(TimerInvalidAction):
            action()  # type: ignore

    # tick action
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.last_tick_time is None
    assert timer.status == Status.PAUSED
    assert 0 < timer.progress < 1

    # resume action
    old_duration_left = timer.duration_left
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.duration_left == old_duration_left
    timer.resume()
    assert timer.status == Status.TICKING
    assert timer.duration_left == old_duration_left
    assert timer.last_tick_time is None
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.last_tick_time is not None
    assert timer.duration_left < old_duration_left

    # restart action
    timer = new_paused_timer()
    assert timer.init_duration > timer.duration_left
    timer.restart()
    assert timer.status == Status.TICKING
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None

    # stop action
    timer = new_paused_timer()
    assert timer.init_duration > timer.duration_left
    timer.stop()
    assert timer.status == Status.IDLE
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None


def test_rang_transitions() -> None:
    # init
    small_duration = Milliseconds(100)  # 0.1 sec

    def new_rang_timer(check_assert: bool = False) -> Timer:
        timer = Timer()
        timer.start(small_duration)
        timer.tick()
        sleep(0.01)
        timer.tick()
        if check_assert:
            assert timer.status == Status.TICKING
            assert timer.init_duration > timer.duration_left
            assert timer.last_tick_time is not None
            assert timer.time_since_rang is None
        sleep(small_duration / MSEC_IN_SEC)
        timer.tick()
        if check_assert:
            assert timer.status == Status.RANG
            assert timer.duration_left == Milliseconds(0)
            assert timer.last_tick_time is not None
            assert timer.time_since_rang is not None
            assert timer.progress == 1.0
        return timer

    timer = new_rang_timer(True)  # check init

    # invalid actions check
    for action in (timer.start, timer.pause, timer.resume):
        with pytest.raises(TimerInvalidAction):
            action()  # type: ignore

    # tick action
    old_last_tick_time = timer.last_tick_time
    old_time_since_rang = timer.time_since_rang
    timer.tick()
    sleep(0.01)
    timer.tick()
    assert timer.last_tick_time > old_last_tick_time  # type: ignore
    assert timer.time_since_rang > old_time_since_rang  # type: ignore
    assert timer.duration_left == Milliseconds(0)

    # restart action
    assert timer.status == Status.RANG
    timer.restart()
    assert timer.status == Status.TICKING
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None

    # stop action
    timer = new_rang_timer()
    timer.stop()
    assert timer.status == Status.IDLE
    assert timer.init_duration == timer.duration_left
    assert timer.last_tick_time is None
    assert timer.time_since_rang is None
