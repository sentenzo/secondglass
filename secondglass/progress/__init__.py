import sys
from typing import Type

from .indicator import Dummy, IProgressIndicator
from .win import ProgressIndicatorWin

if sys.platform == "win32":
    ProgressIndicator: Type[ProgressIndicatorWin] = ProgressIndicatorWin
else:
    ProgressIndicator: Type[Dummy] = Dummy

__all__ = ["IProgressIndicator", "ProgressIndicator", "ProgressIndicatorWin"]
