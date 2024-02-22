from dataclasses import dataclass, field
from tkinter.font import Font

import ttkbootstrap as tb

from secondglass.config import SETTINGS
from secondglass.timer import Timer

FONT_INIT_SIZE = SETTINGS.getint("STATIC", "font_init_size")
FONT_FAMILY = SETTINGS.get("STATIC", "font_family")
RENDER_DELAY_MS = SETTINGS.getint("STATIC", "render_delay_ms")
WH_RATIO_THRESHOLD = SETTINGS.getfloat("STATIC", "wh_ratio_threshold")

TEXT_INIT = SETTINGS.get("DYNAMIC", "init_text_input")

WINDOW_MIN_SIZE = (280, 126)
WINDOW_INIT_SIZE = (400, 180)
BTN_FONT_PROPORTION = 0.7
PADDING = 10
BTN_PADDING_PROPORTION = 0.2
TEXT_SINCE_RANG = "Time passed since rang:"


@dataclass
class Params:
    timer: Timer = field(default_factory=Timer)
    progress: tb.DoubleVar = field(
        default_factory=lambda: tb.DoubleVar(value=0.0)
    )
    text_input: tb.StringVar = field(
        default_factory=lambda: tb.StringVar(value=TEXT_INIT)
    )
    text_output: tb.StringVar = field(default_factory=lambda: tb.StringVar())
    text_message: tb.StringVar = field(default_factory=lambda: tb.StringVar())
    size: tb.DoubleVar = field(default_factory=lambda: tb.DoubleVar(value=1.0))

    font_h1: Font = field(
        default_factory=lambda: Font(family=FONT_FAMILY, size=FONT_INIT_SIZE)
    )
    font_h2: Font = field(
        default_factory=lambda: Font(
            family=FONT_FAMILY, size=int(FONT_INIT_SIZE * BTN_FONT_PROPORTION)
        )
    )

    @staticmethod
    def _calc_size(width: int, height: int) -> float:
        wh_ratio_threshold = WH_RATIO_THRESHOLD
        wh_ratio = width / height
        if wh_ratio > wh_ratio_threshold:
            width = int(height * wh_ratio_threshold)
        return width / WINDOW_INIT_SIZE[0]

    def update_size(self, current_size: tuple[int, int]) -> None:
        old_size = self.size.get()
        new_size = self._calc_size(*current_size)
        if old_size != new_size:
            self.size.set(new_size)
