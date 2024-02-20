from dataclasses import dataclass, field

import ttkbootstrap as tb

from secondglass.timer import Timer

UI_THEME = "litera"  # litera cosmo cerculean / superhero darkly
WINDOW_MIN_SIZE = (280, 126)
WINDOW_INIT_SIZE = (400, 180)
FONT_INIT_SIZE = 18
FONT_FAMILY = "Calibri Light"
BTN_FONT_PROPORTION = 0.7
PADDING = 10
RENDER_DELAY_MS = 30  # 0.03 sec
INIT_TEXT = "5 minutes"
WH_RATIO_THRESHOLD = 2.6


@dataclass
class Params:
    timer: Timer = field(default_factory=Timer)
    progress: tb.DoubleVar = field(
        default_factory=lambda: tb.DoubleVar(value=0.0)
    )
    text_input: tb.StringVar = field(
        default_factory=lambda: tb.StringVar(value=INIT_TEXT)
    )
    text_output: tb.StringVar = field(default_factory=lambda: tb.StringVar())
    size: tb.DoubleVar = field(default_factory=lambda: tb.DoubleVar(value=1.0))

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
