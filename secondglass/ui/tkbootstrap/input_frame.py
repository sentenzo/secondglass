import tkinter as tk
from tkinter.font import Font

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer import Timer  # noqa: F401

from .params import FONT_FAMILY, FONT_INIT_SIZE, PADDING, Params


class InputFrame(tb.Frame):
    def __init__(self, master: tk.Misc, params: Params) -> None:
        super().__init__(master)

        self.params = params

    def create_all(self) -> None:
        font_size = int(FONT_INIT_SIZE * self.params.size.get())
        font = Font(family=FONT_FAMILY, size=font_size)
        self.inner_container = tb.Frame(self)
        self.upper_placeholder = tb.Label(self.inner_container)
        self.entry = tb.Entry(
            self.inner_container,
            textvariable=self.params.text,
            justify=c.CENTER,
            font=font,
            cursor="xterm",
        )
        self.btn_container = tb.Frame(self.inner_container)

        def create_btn(text: str) -> tb.Button:
            return tb.Button(
                self.btn_container,
                text=text,
                bootstyle=(c.LINK),
                cursor="hand2",
            )

        self.btn_start = create_btn("start")
        self.btn_resume = create_btn("resume")
        self.btn_restart = create_btn("restart")

    def pack_all(self) -> None:
        padding = int(PADDING * self.params.size.get())
        self.pack(
            expand=c.YES,
            fill=c.BOTH,
            padx=padding,
            pady=padding,
        )
        self.inner_container.place(
            anchor=c.CENTER,
            relx=0.5,
            rely=0.5,
            relwidth=1.0,
        )
        self.upper_placeholder.pack(
            # padx=4,
        )  # margin
        self.entry.pack(
            fill=c.X,
            padx=4,
        )
        self.btn_container.pack(
            # expand=c.YES,
            # fill=c.BOTH,
            side=c.TOP,
        )
        self.btn_start.pack(side=c.LEFT)
        self.btn_resume.pack(side=c.LEFT)
        self.btn_restart.pack(side=c.LEFT)

    # def create_entry(self) -> tb.Entry:
    #     entry = tb.Entry(
    #         self.container,
    #         textvariable=self.entry_text,
    #         justify=c.CENTER,
    #         font=Font(size=16),
    #         # insertontime=0,
    #         cursor="xterm",
    #     )
    #     entry.pack(
    #         fill=c.X,
    #     )

    #     def focus_in(event: tk.Event) -> None:
    #         self.entry_text.set("111")
    #         entry.select_range(0, c.END)

    #     def focus_out(event: tk.Event) -> None:
    #         self.entry_text.set("222")

    #     entry.bind("<FocusIn>", focus_in)
    #     entry.bind("<FocusOut>", focus_out)

    #     return entry
