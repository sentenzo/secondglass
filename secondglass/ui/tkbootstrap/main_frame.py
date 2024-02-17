import tkinter as tk

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer import Timer  # noqa: F401

from .input_frame import InputFrame
from .params import Params


class MainFrame(tb.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)

        self.params = Params()

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
            relheight=1.01,
            relwidth=1.01,
            relx=0.5,
            rely=0.5,
        )
        self.input_frame.pack_all()

    def animate_all(self) -> None:
        pass

    def animate_timer(self) -> None:
        pass

    # def update(self) -> None:
    #     self.timer.tick()
    #     self.update_progressbar()

    # def update_progressbar(self) -> None:
    #     self.progressbar_var.set(self.timer.progress)


if __name__ == "__main__":
    app = tb.Window(
        title="123",
        themename="simplex",
        minsize=(280, 120),
    )
    mf = MainFrame(app)
    mf.create_all()
    mf.pack_all()
    app.mainloop()
