from typing import Any, Type

import pytest

from secondglass.timer.exceptions import (
    TimeParseException,
    TimeUnitParseException,
)
from secondglass.timer.msec import Milliseconds


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, 0), (12, 12), (102938, 102938)],
)
def test_new(test_input: int, expected: int) -> None:
    assert Milliseconds(test_input) == expected


def test_add_sub() -> None:
    a = Milliseconds(10)
    b = Milliseconds(30)
    assert isinstance(a + b, Milliseconds)
    b += a
    assert isinstance(b, Milliseconds)
    b -= a
    assert isinstance(b, Milliseconds)
    assert isinstance(b - a, Milliseconds)
    with pytest.raises(ValueError):
        _ = a - b
    with pytest.raises(ValueError):
        a -= b


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, 0), (12, 12_000), (102938, 102938_000)],
)
def test_from_sec(test_input: int, expected: int) -> None:
    assert Milliseconds.from_seconds(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, 0), (12, 720000), (102938, 6176280000)],
)
def test_from_min(test_input: int, expected: int) -> None:
    assert Milliseconds.from_minutes(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, 0), (12, 43200000), (102938, 370576800000)],
)
def test_from_hour(test_input: int, expected: int) -> None:
    assert Milliseconds.from_hours(test_input) == expected


@pytest.mark.parametrize(
    "test_input,exception_type",
    [(-12, ValueError), (None, TypeError)],
)
def test_from_smh_exception(test_input: Any, exception_type: Type) -> None:
    for from_method in (
        Milliseconds.from_seconds,
        Milliseconds.from_minutes,
        Milliseconds.from_hours,
    ):
        with pytest.raises(exception_type):
            from_method(test_input)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("42", 42_000),
        ("1h 2m 3s", 3723000),
        ("1h2m3s", 3723000),
        ("3 sec 2m1h", 3723000),
        ("1 hour 2 minutes", 3720000),
        ("0 hour 62 minutes", 3720000),
    ],
)
def test_from_text(test_input: str, expected: int) -> None:
    assert Milliseconds.from_text(test_input) == expected


@pytest.mark.parametrize(
    "test_input,exception_type",
    [
        ("-12", TimeParseException),
        ("  ", TimeParseException),
        ("h4", TimeParseException),
        ("abc", TimeParseException),
        ("4 f", TimeUnitParseException),
        ("4 ss 12 hour 8 dd", TimeUnitParseException),
    ],
)
def test_from_text_exception(test_input: str, exception_type: Type) -> None:
    with pytest.raises(exception_type):
        Milliseconds.from_text(test_input)
