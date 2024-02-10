class TimerException(Exception):
    pass


class TimeParseException(TimerException):
    pass


class TimeUnitParseException(TimeParseException):
    pass


class TimerInvalidAction(TimerException):
    pass


class TimerValueError(TimerException):
    pass
