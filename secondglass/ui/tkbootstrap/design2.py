import tkinter as tk
from tkinter.font import Font

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer import Timer


class MainFrame(tb.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.pack(
            expand=c.YES,
            fill=c.BOTH,
        )
        self.input_frame = InputFrame(self)
        self.progress_var = tb.DoubleVar(value=0.0)
        self.create_progressbar()

        self.timer = Timer()

        InputFrame(self)

    def create_progressbar(self) -> None:
        tb.Progressbar(
            self,
            maximum=1.0,
            value=0.65,
            # variable=self.progress_var,
            bootstyle=c.DEFAULT,
        ).place(
            anchor=c.CENTER,
            relheight=1.01,
            relwidth=1.01,
            relx=0.5,
            rely=0.5,
        )

    def update(self) -> None:
        self.timer.tick()
        self.update_progressbar()

    def update_progressbar(self) -> None:
        self.progress_var.set(self.timer.progress)


class InputFrame(tb.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.pack(
            expand=c.YES,
            fill=c.BOTH,
            # padx=padding,
            # pady=padding,
        )

        # self.user_input = tb.StringVar(value="user_input")
        # self.timer_output = tb.StringVar(value="user_input")
        self.entry_text = tb.StringVar(value="entry_text")

        self.container = tb.Frame(self)
        self.container.place(
            anchor=c.CENTER,
            relx=0.5,
            rely=0.5,
            relwidth=1.0,
            # bordermode=c.INSIDE,
        )
        self.entry = self.create_entry()

        # tb.Label(self.container, text="123").pack(padx=4)  # margin

    def create_entry(self) -> tb.Entry:
        entry = tb.Entry(
            self.container,
            textvariable=self.entry_text,
            justify=c.CENTER,
            font=Font(size=16),
            # insertontime=0,
            cursor="xterm",
        )
        entry.pack(
            fill=c.X,
        )

        def focus_in(event: tk.Event) -> None:
            self.entry_text.set("111")
            entry.select_range(0, c.END)

        def focus_out(event: tk.Event) -> None:
            self.entry_text.set("222")

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)

        return entry

    def change_font_size(self) -> None:
        pass

    def update(self, timer: Timer) -> None:
        pass


if __name__ == "__main__":
    app = tb.Window(
        title="123",
        themename="simplex",
        minsize=(280, 120),
    )
    MainFrame(app)
    app.mainloop()
