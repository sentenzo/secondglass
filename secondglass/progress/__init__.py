import sys
from typing import Type

from .indicator import Dummy, IProgressIndicator
from .win import ProgressIndicatorWin

ProgressIndicator: Type[IProgressIndicator] = Dummy
if sys.platform == "win32":
    ProgressIndicator = ProgressIndicatorWin

__all__ = ["IProgressIndicator", "ProgressIndicator", "ProgressIndicatorWin"]
