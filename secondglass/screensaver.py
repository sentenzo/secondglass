import ctypes
import sys
from typing import Callable


class ScreensaverPreventer:
    def __init__(self) -> None:
        self._is_ss_prevented = False

    @property
    def prevent(self) -> Callable[[bool], None]:
        if sys.platform == "win32":
            return self._win32_prevent
        else:
            return self._dummy_prevent

    @property
    def wake_up(self) -> Callable[[], None]:
        if sys.platform == "win32":
            return self._win32_wake_up
        else:
            return self._dummy_wake_up

    def _win32_wake_up(self) -> None:
        """https://stackoverflow.com/a/77963712/2493536"""
        if not self._is_ss_prevented:
            MOUSEEVENTF_ABSOLUTE = 0x0000
            MOUSEEVENTF_MOVE = 0x0001
            MOUSE_DX = 1
            MOUSE_DY = 0
            MOUSE_DWDATA = 0

            ctypes.windll.user32.mouse_event(
                (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE),
                MOUSE_DX,
                MOUSE_DY,
                MOUSE_DWDATA,
            )

    def _dummy_wake_up(self) -> None:
        pass

    def _win32_prevent(self, value: bool) -> None:
        """https://stackoverflow.com/a/65401303/2493536"""

        assert sys.platform == "win32"

        if value == self._is_ss_prevented:
            return
        if value is True:
            self._is_ss_prevented = value
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        else:
            self._is_ss_prevented = value
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

    def _dummy_prevent(self, value: bool) -> None:
        self._is_ss_prevented = value


SCREENSAVER_PREVENTER = ScreensaverPreventer()
