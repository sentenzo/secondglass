from enum import Enum, auto

from .exceptions import TimeUnitParseException


class TimeUnit(Enum):
    HOUR = auto()
    MINUTE = auto()
    SECOND = auto()

    @staticmethod
    def parse(text: str) -> "TimeUnit":
        if text.lower() in ("h", "hs", "hour", "hours"):
            return TimeUnit.HOUR
        elif text.lower() in ("m", "ms", "min", "mins", "minute", "minutes"):
            return TimeUnit.MINUTE
        elif text.lower() in ("s", "ss", "sec", "secs", "second", "seconds"):
            return TimeUnit.SECOND
        else:
            raise TimeUnitParseException(f"Failed to parse: {text}")
