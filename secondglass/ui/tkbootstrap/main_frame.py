import tkinter as tk

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer import Status, Timer  # noqa: F401

from .input_frame import InputFrame
from .params import RENDER_DELAY_MS, Params


class MainFrame(tb.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)

        self.params = Params()
        self.params.timer.start()  # dbg

    def create_all(self) -> None:
        self.progressbar = tb.Progressbar(
            self,
            maximum=1.0,
            variable=self.params.progress,
            bootstyle=c.DEFAULT,
        )
        # the order IS important
        # InputFrame should go after Progressbar
        self.input_frame = InputFrame(self, self.params)
        self.input_frame.create_all()

    def pack_all(self) -> None:
        self.pack(
            expand=c.YES,
            fill=c.BOTH,
        )
        self.progressbar.place(
            anchor=c.CENTER,
            relheight=1.01,  # aliasing fix
            relwidth=1.005,  # aliasing fix
            relx=0.5,  # center X
            rely=0.5,  # center Y
        )
        self.input_frame.pack_all()

    def animate_all(self) -> None:
        self.params.timer.tick()
        self.update_all()
        self.after(RENDER_DELAY_MS, self.animate_all)

    def update_all(self) -> None:
        self.params.progress.set(self.params.timer.progress)
