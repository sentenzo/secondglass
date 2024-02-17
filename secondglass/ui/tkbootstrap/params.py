from dataclasses import dataclass, field

import ttkbootstrap as tb

from secondglass.timer import Timer

FONT_INIT_SIZE = 16
FONT_FAMILY = "Areal"
PADDING = 10
RENDER_DELAY_MS = 50  # 0.05 sec


@dataclass
class Params:
    timer: Timer = field(default_factory=Timer)
    progress: tb.DoubleVar = field(
        default_factory=lambda: tb.DoubleVar(value=0.6)
    )
    text: tb.StringVar = field(
        default_factory=lambda: tb.StringVar(value="text")
    )
    size: tb.DoubleVar = field(default_factory=lambda: tb.DoubleVar(value=1.0))
