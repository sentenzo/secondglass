import tkinter as tk
from tkinter.font import Font
from typing import Callable

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer import Status

from .frame import Frame
from .params import (
    BTN_FONT_PROPORTION,
    BTN_PADDING_PROPORTION,
    FONT_FAMILY,
    FONT_INIT_SIZE,
    PADDING,
    UI_THEME,
    Params,
)


class BtnFrame(Frame):
    def __init__(self, master: tk.Misc, params: Params) -> None:
        super().__init__(master, params)

    def create_all(self) -> None:
        self.padding = int(PADDING * BTN_PADDING_PROPORTION)
        self.font = Font(
            family=FONT_FAMILY, size=int(FONT_INIT_SIZE * BTN_FONT_PROPORTION)
        )
        tb.Style(UI_THEME).configure("My.Link.TButton", font=self.font)

        def create_btn(text: str) -> tb.Button:
            return tb.Button(
                self,
                text=text,
                cursor="hand2",
                style="My.Link.TButton",
            )

        self.btn_start = create_btn("start")
        self.btn_pause = create_btn("pause")
        self.btn_resume = create_btn("resume")
        self.btn_restart = create_btn("restart")
        self.btn_stop = create_btn("stop")

        self.btns_ordered = [
            self.btn_start,
            self.btn_pause,
            self.btn_resume,
            self.btn_restart,
            self.btn_stop,
        ]

        self.btns_visibility: dict[Status, tuple[tb.Button, ...]] = {
            Status.IDLE: (self.btn_start,),
            Status.TICKING: (self.btn_pause, self.btn_restart, self.btn_stop),
            Status.PAUSED: (self.btn_resume, self.btn_restart, self.btn_stop),
            Status.RANG: (self.btn_restart, self.btn_stop),
        }

    def pack_all(self) -> None:
        self.pack(side=c.TOP)
        self._update_btns_visibility()

    def _update_btns_visibility(self) -> None:
        visible_bnts = self.btns_visibility[self.params.timer.status]
        for btn in self.btns_ordered:
            btn.pack_forget()
        for btn in visible_bnts:
            btn.pack(
                side=c.LEFT,
                padx=self.padding,
                pady=self.padding // 2,
            )

    def set_callbacks(self) -> None:
        def bind_btn_handler(
            btn: tb.Button,
            change_status: Callable,
            reinit_timer_vlaue: bool = False,
        ) -> None:

            def handler() -> None:
                if reinit_timer_vlaue:
                    timer_vlaue = self.params.text_input.get()
                    change_status(timer_vlaue)
                    self.params.text_input.set(
                        self.params.timer.init_duration_text
                    )
                else:
                    change_status()
                self._update_btns_visibility()
                self.focus_set()  # drop focus

            btn.config(command=handler)

        bind_btn_handler(self.btn_start, self.params.timer.start, True)
        bind_btn_handler(self.btn_pause, self.params.timer.pause)
        bind_btn_handler(self.btn_resume, self.params.timer.resume)
        bind_btn_handler(self.btn_restart, self.params.timer.restart, True)
        bind_btn_handler(self.btn_stop, self.params.timer.stop)

        def on_size_change(name: str, ind: str | int, method: str) -> None:
            new_size = self.params.size.get()
            new_font_size = int(
                FONT_INIT_SIZE * BTN_FONT_PROPORTION * new_size
            )
            self.font.config(size=new_font_size)

            self.padding = int(PADDING * BTN_PADDING_PROPORTION * new_size)
            for btn in self.btns_ordered:
                if btn in self.btns_visibility[self.params.timer.status]:
                    btn.pack_configure(
                        padx=self.padding,
                        pady=self.padding // 2,
                    )

        self.params.size.trace_add("write", on_size_change)
