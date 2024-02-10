from enum import Enum, auto

from .msec import Milliseconds

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

    @property
    def status(self) -> Status:
        return self.status

    def set_duration(self, duration: str | Milliseconds) -> None:
        if isinstance(duration, str):
            self.init_duration = Milliseconds.from_text(duration)
        elif isinstance(duration, Milliseconds):
            self.init_duration = duration
        else:
            raise ValueError
        self.duration_left = self.init_duration

    def start(self) -> None:
        self._status = Status.TICKING

    def restart(self) -> None:
        self.duration_left = self.init_duration
        self.start()

    def pause(self) -> None:
        self._status = Status.PAUSED

    def stop(self) -> None:
        self.duration_left = self.init_duration
        self._status = Status.IDLE

    def _ring(self) -> None:
        pass

    def tick(self, time_passed: Milliseconds) -> None:
        if self.status == Status.TICKING:
            if time_passed >= self.duration_left:
                self.duration_left = Milliseconds(0)
                self._ring()
                self._status = Status.RANG
            else:
                self.duration_left -= time_passed
