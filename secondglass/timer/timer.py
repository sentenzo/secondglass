from enum import Enum, auto
from functools import wraps
from time import time
from typing import Any, Callable

from .exceptions import TimerException, TimerInvalidAction, TimerValueError
from .msec import MSEC_IN_SEC, Milliseconds

DEFAULT_DURATION = Milliseconds.from_minutes(5)


class Status(Enum):
    IDLE = auto()
    TICKING = auto()
    PAUSED = auto()
    RANG = auto()


def _requires_state(*allowed_statuses: Status) -> Callable:

    def requires_state_decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self: "Timer", *args, **kwargs):  # type: ignore
            if self._status not in allowed_statuses:
                raise TimerInvalidAction(
                    f"Invalid status: {self._status}.\n"
                    f"Method {method.__name__} requires one of these statuses:"
                    f" {allowed_statuses}"
                )
            return method(self, *args, **kwargs)

        return wrapper

    return requires_state_decorator


def _reset_all(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self: "Timer", *args, **kwargs):  # type: ignore
        result = method(self, *args, **kwargs)
        self.duration_left = self.init_duration
        self.last_tick_time = None
        self.time_since_rang = None
        return result

    return wrapper


class Timer:
    def __init__(self) -> None:
        self.init_duration: Milliseconds = DEFAULT_DURATION
        self.duration_left: Milliseconds = self.init_duration
        self._status: Status = Status.IDLE
        self.last_tick_time: Milliseconds | None = None
        self.time_since_rang: Milliseconds | None = None

    @property
    def status(self) -> Status:
        return self._status

    @property
    def init_duration_text(self) -> str:
        return self.init_duration.to_text()

    @property
    def duration_left_text(self) -> str:
        return self.duration_left.to_text()

    @property
    def time_since_rang_text(self) -> str:
        if self.time_since_rang is None:
            raise TimerInvalidAction(
                "Attempt to get time_since_rang_text "
                "while time_since_rang is None"
            )
        return self.time_since_rang.to_text()

    @property
    def progress(self) -> float:
        if self._status == Status.RANG:
            return 1.0
        elif self._status in (Status.TICKING, Status.PAUSED):
            value = (
                self.init_duration - self.duration_left
            ) / self.init_duration
            assert 0.0 <= value <= 1.0
            return value
        elif self._status == Status.IDLE:
            return 0.0
        else:
            raise TimerException(f"Unknown status: {self._status}")

    def _set_duration(self, duration: str | int) -> None:
        if isinstance(duration, str):
            self.init_duration = Milliseconds.from_text(duration)
        elif isinstance(duration, int):
            self.init_duration = Milliseconds(duration)
        else:
            raise TimerValueError(
                f"Attempt to init duration as {type(duration).__name__}"
            )

    @_requires_state(Status.IDLE)
    @_reset_all
    def start(self, new_duration: Any | None = None) -> None:
        if new_duration:
            self._set_duration(new_duration)
        self._status = Status.TICKING

    @_requires_state(Status.TICKING, Status.PAUSED, Status.RANG)
    @_reset_all
    def stop(self) -> None:
        self._status = Status.IDLE

    @_requires_state(Status.TICKING, Status.PAUSED, Status.RANG)
    @_reset_all
    def restart(self, new_duration: Any | None = None) -> None:
        if new_duration:
            self._set_duration(new_duration)
        self._status = Status.TICKING

    @_requires_state(Status.TICKING)
    def pause(self) -> None:
        self.last_tick_time = None
        self._status = Status.PAUSED

    @_requires_state(Status.PAUSED)
    def resume(self) -> None:
        self._status = Status.TICKING

    def _ring(self) -> None:
        pass

    def _tick(self) -> None:
        print("\033[A\033[0K", end="")  # clear the last line
        print("\033[A\033[0K", end="")  # clear the last line
        print("Progress:", self.progress)
        print("Time left:", self.duration_left_text)

    @_requires_state(Status.IDLE, Status.TICKING, Status.PAUSED, Status.RANG)
    def tick(self) -> None:
        self._tick()
        now: Milliseconds = Milliseconds(time() * MSEC_IN_SEC)
        if self.last_tick_time is None:
            if self.status in (Status.TICKING, Status.RANG):
                self.last_tick_time = now
            return
        time_passed: Milliseconds = now - self.last_tick_time
        if self.status == Status.TICKING:
            if time_passed >= self.duration_left:
                self.duration_left = Milliseconds(0)
                self._ring()
                self._status = Status.RANG
                self.time_since_rang = time_passed - self.duration_left
            else:
                self.duration_left -= time_passed
        elif self.status == Status.RANG:
            if self.time_since_rang is None:
                raise TimerValueError(
                    "Attempt to tick() when self.time_since_rang is None"
                )
            self.time_since_rang += time_passed
        if self.status in (Status.TICKING, Status.RANG):
            self.last_tick_time = now
