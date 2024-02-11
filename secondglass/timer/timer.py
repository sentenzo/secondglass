from enum import Enum, auto
from time import time
from typing import Any

from .exceptions import TimerInvalidAction, TimerValueError
from .msec import MSEC_IN_SEC, Milliseconds

DEFAULT_DURATION = Milliseconds.from_minutes(5)


class Status(Enum):
    IDLE = auto()
    TICKING = auto()
    PAUSED = auto()
    RANG = auto()


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

    def _set_duration(self, duration: str | Milliseconds) -> None:
        if isinstance(duration, str):
            self.init_duration = Milliseconds.from_text(duration)
        elif isinstance(duration, Milliseconds):
            self.init_duration = duration
        else:
            raise TimerValueError(
                f"Attempt to init duration as {type(duration).__name__}"
            )

    def start(self, new_duration: Any | None = None) -> None:
        if self._status != Status.IDLE:
            raise TimerInvalidAction("Attempt to start() without Status.IDLE")
        if new_duration:
            self._set_duration(new_duration)
        self.duration_left = self.init_duration
        self._status = Status.TICKING

    def stop(self) -> None:
        if self._status not in (Status.TICKING, Status.PAUSED, Status.RANG):
            raise TimerInvalidAction(
                "Attempt to stop() without Status.TICKING or Status.PAUSED"
            )
        self.duration_left = self.init_duration
        self.last_tick_time = None
        self.time_since_rang = None
        self._status = Status.IDLE

    def restart(self, new_duration: Any | None = None) -> None:
        if self._status not in (Status.TICKING, Status.PAUSED, Status.RANG):
            raise TimerInvalidAction(
                "Attempt to restart() without Status.TICKING or Status.PAUSED "
                "or Status.RANG"
            )
        if new_duration:
            self._set_duration(new_duration)
        self.duration_left = self.init_duration
        self.last_tick_time = None
        self.time_since_rang = None
        self._status = Status.TICKING

    def pause(self) -> None:
        if self._status != Status.TICKING:
            raise TimerInvalidAction(
                "Attempt to pause() without Status.TICKING"
            )
        self.last_tick_time = None
        self._status = Status.PAUSED

    def resume(self) -> None:
        if self._status != Status.PAUSED:
            raise TimerInvalidAction(
                "Attempt to resume() without Status.PAUSED"
            )
        self._status = Status.TICKING

    def _ring(self) -> None:
        print("RING!")

    def tick(self) -> None:
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
                raise TimerInvalidAction(
                    "Attempt to tick() when self.time_since_rang is None"
                )
            self.time_since_rang += time_passed
        if self.status in (Status.TICKING, Status.RANG):
            self.last_tick_time = now
