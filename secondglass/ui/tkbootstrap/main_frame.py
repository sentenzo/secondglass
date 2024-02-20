import tkinter as tk

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.player import play_beep
from secondglass.progress import IProgressIndicator, ProgressIndicator
from secondglass.timer import Status

from .frame import Frame
from .input_frame import InputFrame
from .params import UI_THEME


class MainFrame(Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.prev_status: Status | None = None

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

        # `hwnd` can change after the first rendering. Therefore:
        #  run `main_frame.update()` before `main_frame.create_all()`
        #  (see ./app.py)
        hwnd = int(self.winfo_toplevel().wm_frame(), 16)
        self.progress_indicator: IProgressIndicator = ProgressIndicator(hwnd)

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

    def set_callbacks(self) -> None:
        self.input_frame.set_callbacks()

    def _put_app_on_top(self) -> None:
        app = self.winfo_toplevel()
        app.wm_deiconify()  # un-minimize
        app.wm_attributes("-topmost", True)
        app.wm_attributes("-topmost", False)

    @staticmethod
    def get_bootstyle_from_status(status: Status) -> str:
        if status in (Status.IDLE, Status.TICKING):
            if UI_THEME in ("cosmo", "litera", "cerculean"):
                return c.PRIMARY
            else:
                return c.INFO
        return {Status.PAUSED: c.WARNING, Status.RANG: c.DANGER}[status]

    def change_bootstyle(self, bootstyle: str) -> None:
        self.progressbar.configure(bootstyle=bootstyle)
        self.input_frame.entry.configure(bootstyle=bootstyle)

    def on_status_change(self, from_: Status | None, to: Status) -> None:
        if to == Status.IDLE:
            self.input_frame.upper_placeholder.configure(text="")
            self.progress_indicator.set_state_normal()
            self.input_frame.entry.configure(
                textvariable=self.params.text_input
            )
        elif to == Status.PAUSED:
            self.progress_indicator.set_state_paused()
        elif to == Status.TICKING:
            self.input_frame.upper_placeholder.configure(text="")
            self.progress_indicator.set_state_normal()
            self.input_frame.entry.configure(
                textvariable=self.params.text_output
            )
        elif to == Status.RANG:
            self.input_frame.upper_placeholder.configure(
                text="Time passed since rang:"
            )
            self.progress_indicator.set_state_error()
            self.input_frame.btn_container._update_btns_visibility()
            self._put_app_on_top()
            play_beep()
        self.change_bootstyle(
            self.get_bootstyle_from_status(to),
        )

    def update_all(self) -> None:
        self.params.progress.set(self.params.timer.progress)
        self.progress_indicator.set_value(self.params.timer.progress)
        if self.params.timer.status == Status.RANG:
            self.params.text_output.set(self.params.timer.time_since_rang_text)
        else:
            self.params.text_output.set(self.params.timer.duration_left_text)

        if self.prev_status != self.params.timer.status:
            self.on_status_change(self.prev_status, self.params.timer.status)
            self.prev_status = self.params.timer.status

        self.input_frame.update_all()
        self.params.update_size((self.winfo_width(), self.winfo_height()))
