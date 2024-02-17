import tkinter as tk

import ttkbootstrap as tb

from .params import RENDER_DELAY_MS, Params


class Frame(tb.Frame):
    def __init__(
        self, master: tk.Misc | None = None, params: Params | None = None
    ) -> None:
        super().__init__(master)
        if params is None:
            params = Params()
        self.params = params

    def create_all(self) -> None:
        raise NotImplementedError

    def pack_all(self) -> None:
        raise NotImplementedError

    def animate_all(self) -> None:
        self.set_callbacks()
        self.run_animation_loop()

    def run_animation_loop(self) -> None:
        self.params.timer.tick()
        self.update_all()
        self.after(RENDER_DELAY_MS, self.run_animation_loop)

    def set_callbacks(self) -> None:
        pass

    def update_all(self) -> None:
        pass
