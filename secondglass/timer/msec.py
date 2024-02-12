from itertools import groupby
from math import ceil
from typing import Any, Tuple

from .exceptions import TimeParseException
from .timeunit import TimeUnit

MSEC_IN_SEC = 1000
SEC_IN_MIN = 60
MIN_IN_H = 60
H_IN_D = 24


class Milliseconds(int):
    def __new__(cls, value: Any) -> "Milliseconds":
        obj = super(Milliseconds, cls).__new__(cls, value)
        if obj < 0:
            raise ValueError("Value must be a nonnegative integer")
        return obj

    def __add__(self, __value: int) -> "Milliseconds":
        return Milliseconds(super().__add__(__value))

    def __sub__(self, __value: int) -> "Milliseconds":
        return Milliseconds(super().__sub__(__value))

    @staticmethod
    def from_seconds(seconds: int) -> "Milliseconds":
        return Milliseconds(seconds * MSEC_IN_SEC)

    @staticmethod
    def from_minutes(minutes: int) -> "Milliseconds":
        return Milliseconds(minutes * SEC_IN_MIN * MSEC_IN_SEC)

    @staticmethod
    def from_hours(hours: int) -> "Milliseconds":
        return Milliseconds(hours * MIN_IN_H * SEC_IN_MIN * MSEC_IN_SEC)

    @staticmethod
    def from_time_unit(value: int, unit: TimeUnit) -> "Milliseconds":
        return {
            TimeUnit.HOUR: Milliseconds.from_hours,
            TimeUnit.MINUTE: Milliseconds.from_minutes,
            TimeUnit.SECOND: Milliseconds.from_seconds,
        }[unit](value)

    @staticmethod
    def from_text(text: str) -> "Milliseconds":
        groups: list[str] = []
        for _, g in groupby(text, str.isnumeric):
            group = "".join(g).strip()
            if group:
                groups.append(group)
        if not groups:
            raise TimeParseException(f"Failed to parse text: {text}")

        if len(groups) == 1 and group[0].isnumeric():
            group = groups[0]
            seconds = int(group)
            return Milliseconds.from_minutes(seconds)
        elif len(groups) % 2 == 0:
            numbers: list[int] = []
            for group in groups[::2]:
                if not group.isnumeric():
                    raise TimeParseException(f"Failed to parse text: {text}")
                numbers.append(int(group))
            units: list[TimeUnit] = []
            for group in groups[1::2]:
                units.append(TimeUnit.parse(group))
            msec: Milliseconds = Milliseconds(0)
            for number, unit in zip(numbers, units):
                msec += Milliseconds.from_time_unit(number, unit)
            return msec
        raise TimeParseException(f"Failed to parse text: {text}")

    def to_time_units_tuple(self) -> Tuple[int, int, int]:
        total_s = ceil(self / MSEC_IN_SEC)
        total_m, s = divmod(total_s, SEC_IN_MIN)
        total_h, m = divmod(total_m, MIN_IN_H)
        return (total_h, m, s)

    def to_text(self) -> str:
        words: list[str] = []
        for number, name in zip(
            self.to_time_units_tuple(), ("hour", "minute", "second")
        ):
            if number == 0 and len(words) == 0:
                continue
            words.append(str(number))
            if number == 1:
                words.append(name)
            else:
                words.append(name + "s")
        if not words:
            return "0 seconds"
        else:
            return " ".join(words)
