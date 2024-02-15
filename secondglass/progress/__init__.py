import sys
from typing import Type

from .indicator import Dummy, IProgressIndicator
from .win import TaskbarProgressIndicatorWin

if sys.platform == "win32":
    ProgressIndicator: Type[TaskbarProgressIndicatorWin] = (
        TaskbarProgressIndicatorWin
    )
else:
    ProgressIndicator: Type[Dummy] = Dummy

__all__ = [
    "IProgressIndicator",
    "ProgressIndicator",
    "TaskbarProgressIndicatorWin",
]
