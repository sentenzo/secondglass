import tkinter as tk
from enum import Enum
from tkinter.font import Font  # noqa: F401

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from .frame import Frame
from .params import FONT_FAMILY, FONT_INIT_SIZE, PADDING, Params  # noqa: F401


class Btn(Enum):
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    RESTART = "restart"
    STOP = "stop"


btn_info = {
    Btn.START: (
        "start",
        (c.LINK),
    )
}


class BtnFrame(Frame):
    def __init__(self, master: tk.Misc, params: Params) -> None:
        super().__init__(master, params)

    def create_all(self) -> None:
        self.btns: dict[Btn, tb.Button] = {}
        self.btns[Btn.START] = tb.Button(
            self, text="start", bootstyle=(c.LINK), cursor="hand2"
        )
        self.btns[Btn.PAUSE] = tb.Button(
            self, text="pause", bootstyle=(c.LINK), cursor="hand2"
        )
        self.btns[Btn.RESUME] = tb.Button(
            self, text="resume", bootstyle=(c.LINK), cursor="hand2"
        )
        self.btns[Btn.RESTART] = tb.Button(
            self, text="restart", bootstyle=(c.LINK), cursor="hand2"
        )
        self.btns[Btn.STOP] = tb.Button(
            self, text="stop", bootstyle=(c.LINK), cursor="hand2"
        )

    def pack_all(self) -> None:
        self.pack(
            # expand=c.YES,
            # fill=c.BOTH,
            side=c.TOP,
        )
        btn: tb.Button
        for btn in self.btns.values():
            btn.pack(side=c.LEFT)
