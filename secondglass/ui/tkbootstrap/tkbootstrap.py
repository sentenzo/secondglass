import tkinter as tk
from tkinter.font import Font

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.helpers import pyinstaller_fix_path
from secondglass.progress import IProgressIndicator, ProgressIndicator
from secondglass.timer import Status, Timer

from ..ui import UI

# class InputFrame(tb.Frame):
#     def __init__(self, master: tk.Misc | None = None) -> None:
#         super().__init__(master)

#         self.timer_text = tb.StringVar(value="5 minutes")
#         self.font_size = 16
#         self.padding = tb.IntVar(value=12)

#         self.pack(
#             fill=c.BOTH,
#             expand=c.YES,
#             padx=self.padding,
#             pady=self.padding,
#         )


# class ProgressFrame(tb.Frame):
#     def __init__(self, master: tk.Misc | None = None) -> None:
#         super().__init__(master)

#         self.pack(
#             fill=c.BOTH,
#             expand=c.YES,
#         )
#         tb.Progressbar(
#             self,
#             maximum=1.0,
#             value=0.35,
#             bootstyle=c.DEFAULT,
#         ).pack(
#             # anchor=S,
#             # side=BOTTOM,
#             fill=c.X,
#             expand=c.NO,
#             padx=(2, 2),
#             pady=(1, 2),
#             ipady=1,
#         )


# class MainFrame(tb.Frame):
#     def __init__(self, master: tk.Misc | None = None) -> None:
#         super().__init__(master)

#         self.pack(
#             fill=c.BOTH,
#             expand=c.YES,
#         )
#         InputFrame(self)
#         ProgressFrame(self)


class MyAwesomeApp(tb.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.status: Status = Status.IDLE

        self.pack(
            fill=c.BOTH,
            expand=c.YES,
        )

        self.font_size = tb.IntVar(value=16)
        self.timer_text = tb.StringVar(value="5 minutes")

        self.create_layout()
        # self.font = ("Helvetica", 126)

    def create_input_box(self) -> tb.Entry:
        entry = tb.Entry(
            self,
            textvariable=self.timer_text,
            justify=c.CENTER,
            font=Font(size=16),
        )

        def on_size_change(e: tk.Event) -> None:
            # print(e.width, e.height)
            new_font_size = int(12 * e.width / 240)
            entry.config(font=Font(size=new_font_size))
            # print(new_font_size)

        entry.bind("<Configure>", on_size_change)
        return entry

    def create_buttons(self) -> tb.Frame:
        btn_frame = tb.Frame(
            self,
        )

        def create_button(text: str, style: str = c.PRIMARY) -> tb.Button:
            def cmd() -> None:
                self.timer_text.set(text)

            btn = tb.Button(
                btn_frame,
                text=text,
                bootstyle=(style, c.LINK),  # OUTLINE LINK
                cursor="hand2",
                command=cmd,
            )
            return btn

        btn_start = create_button("start")
        btn_restart = create_button("restart")
        btn_pause = create_button("pause")
        btn_resume = create_button("resume")
        btn_stop = create_button("stop")

        btn_start.pack(side=c.LEFT, padx=2, pady=2)
        btn_restart.pack(side=c.LEFT, padx=2, pady=2)
        btn_pause.pack(side=c.LEFT, padx=2, pady=2)
        btn_resume.pack(side=c.LEFT, padx=2, pady=2)
        btn_stop.pack(side=c.LEFT, padx=2, pady=2)
        return btn_frame

    def create_progress_bar(self) -> tb.Progressbar:
        pbar = tb.Progressbar(
            self,
            maximum=1.0,
            value=0.35,
            bootstyle=c.DEFAULT,
            # phase=1,
        )
        # pbar.start()
        return pbar

    def create_layout(self) -> None:
        ibox = self.create_input_box()
        ibox.pack(
            # anchor=N,
            side=c.TOP,
            fill=c.X,
            expand=c.YES,
            padx=8,
            pady=(2, 1),
        )

        btn_frame = self.create_buttons()
        btn_frame.pack()

        pbar = self.create_progress_bar()
        pbar.pack(
            # anchor=S,
            # side=BOTTOM,
            fill=c.X,
            expand=c.NO,
            padx=(2, 2),
            pady=(1, 2),
            ipady=1,
        )


class TkbUI(UI):
    def __init__(self, timer: Timer) -> None:
        icon_path = pyinstaller_fix_path("secondglass/rec/clock.png")
        self.app = tb.Window(
            title="MyAwesomeApp",
            themename="simplex",  # minty lumen sandstone simplex
            minsize=(240, 100),
            iconphoto=icon_path,
            # resizable=(False, False),
        )
        MyAwesomeApp(self.app)
        self.app.update()
        hwnd = int(self.app.wm_frame(), 16)  # do it only after `.update()`
        # hwnd = self.app.winfo_id()
        # hwnd = int(self.app.frame(), 16)
        self.pind: IProgressIndicator = ProgressIndicator(window_id=hwnd)

    def run(self) -> None:
        self.pind.set_state_normal()
        self.pind.set_value(0.321)
        self.app.mainloop()
