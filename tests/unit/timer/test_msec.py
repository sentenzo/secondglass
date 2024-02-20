from typing import Any, Tuple, Type

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
        ("42", 2520000),
        ("1h 2m 3s", 3723000),
        ("1h2m3s", 3723000),
        ("3 sec 2m1h", 3723000),
        ("1 hour 2 minutes", 3720000),
        ("0 hour 62 minutes", 3720000),
        ("51h", 183600000),
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


@pytest.mark.parametrize(
    "test_input,expected_tuple,expected_text",
    [
        ("0", (0, 0, 0), "0 seconds"),
        ("0h", (0, 0, 0), "0 seconds"),
        ("0s", (0, 0, 0), "0 seconds"),
        ("1s", (0, 0, 1), "1 second"),
        ("42", (0, 42, 0), "42 minutes"),
        ("51h", (51, 0, 0), "51 hours"),
        ("121s", (0, 2, 1), "2 minutes 1 second"),
        ("54001s", (15, 0, 1), "15 hours 1 second"),
        ("51h 4min", (51, 4, 0), "51 hours 4 minutes"),
        ("12 hour 34m 56 sec", (12, 34, 56), "12 hours 34 minutes 56 seconds"),
        ("1h 2m 3s", (1, 2, 3), "1 hour 2 minutes 3 seconds"),
        ("3h 1m 1s", (3, 1, 1), "3 hours 1 minute 1 second"),
    ],
)
def test_to_text(
    test_input: str, expected_tuple: Tuple[int, int, int], expected_text: str
) -> None:
    val = Milliseconds.from_text(test_input)
    assert val.to_time_units_tuple() == expected_tuple
    assert val.to_text() == expected_text
