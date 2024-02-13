from tkinter import Misc

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, TOP, YES

from secondglass.progress import IProgressIndicator, ProgressIndicator
from secondglass.timer import Status, Timer

from .ui import UI


class MyAwesomeApp(ttk.Frame):
    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)
        self.status: Status = Status.IDLE

        self.pack(fill=BOTH, expand=YES)

        self.running = ttk.BooleanVar(value=False)
        self.afterid = ttk.StringVar()
        self.elapsed = ttk.IntVar()
        self.timer_text = ttk.StringVar(value="00:00:00")

        self.create_layout()

    def create_layout(self) -> None:
        """Create the stopwatch number display"""
        lbl = ttk.Label(
            master=self,
            font="-size 32",
            anchor=CENTER,
            textvariable=self.timer_text,
            # background="#f00",
        )
        lbl.pack(side=TOP, fill=BOTH, padx=0, pady=0)
        pbar = ttk.Progressbar(
            master=self,
            maximum=1.0,
            value=0.35,
            bootstyle="success",
            phase=1,
        )
        pbar.pack(side=TOP, fill=BOTH, padx=0, pady=0)
        pbar.start()


class TkbUI(UI):
    def __init__(self, timer: Timer) -> None:
        self.app = ttk.Window(
            title="MyAwesomeApp",
            themename="cosmo",
            minsize=(240, 64),
            # resizable=(False, False),
        )
        MyAwesomeApp(self.app)
        hwnd = self.app.winfo_id()  # int(app.wm_frame(), 16)
        self.pind: IProgressIndicator = ProgressIndicator(window_id=hwnd)

    def run(self) -> None:
        self.pind.set_state_normal()
        self.pind.set_value(0.321)
        self.app.mainloop()
