import tkinter as tk

import ttkbootstrap as tb
import ttkbootstrap.constants as c

from secondglass.timer.timer import Status

from .btn_frame import BtnFrame
from .frame import Frame
from .params import FONT_INIT_SIZE, PADDING, TEXT_SINCE_RANG, Params


class InputFrame(Frame):
    def __init__(self, master: tk.Misc, params: Params) -> None:
        super().__init__(master, params)

    def create_all(self) -> None:
        self.inner_container = tb.Frame(self)
        self.upper_placeholder = tb.Label(
            self.inner_container, bootstyle=c.SECONDARY
        )
        self.entry = tb.Entry(
            self.inner_container,
            textvariable=self.params.text_input,
            justify=c.CENTER,
            font=self.params.font_h1,
            cursor="xterm",
        )
        self.btn_container = BtnFrame(self.inner_container, self.params)
        self.btn_container.create_all()
        self.upper_placeholder.configure(font=self.params.font_h2)

    def pack_all(self) -> None:
        self.pack(
            expand=c.YES,
            fill=c.BOTH,
            padx=PADDING,
            pady=PADDING,
        )
        self.inner_container.place(
            anchor=c.CENTER,
            relx=0.5,
            rely=0.5,
            relwidth=1.0,
        )
        self.upper_placeholder.pack(
            pady=(0, PADDING // 2),  # a hack 😑
        )
        self.entry.pack(
            fill=c.X,
            padx=4,
        )
        self.btn_container.pack_all()

    def update_all(self) -> None:
        self.btn_container.update_all()

    def set_callbacks(self) -> None:
        def on_size_change(name: str, ind: str | int, method: str) -> None:
            new_size = self.params.size.get()
            new_padding = int(PADDING * new_size)
            self.pack_configure(
                padx=new_padding,
                pady=new_padding,
            )

            new_font_size = int(FONT_INIT_SIZE * new_size)
            self.params.font_h1.config(size=new_font_size)
            self.params.text_input.set(self.params.text_input.get())
            # - fixes the font alignment issue

            self.upper_placeholder.pack_configure(
                pady=(0, new_padding // 2),  # a hack 😑
            )

        self.params.size.trace_add("write", on_size_change)
        self.btn_container.set_callbacks()

        def entry_select_all(event: tk.Event) -> None:
            self.entry.select_range(0, c.END)
            self.entry.icursor(c.END)

        def entry_focus_in(event: tk.Event) -> None:
            if self.params.timer.status == Status.RANG:
                self.upper_placeholder.configure(text="")
            self.entry.configure(textvariable=self.params.text_input)
            entry_select_all(event)

        def entry_focus_out(event: tk.Event) -> None:
            if self.params.timer.status == Status.RANG:
                self.upper_placeholder.configure(text=TEXT_SINCE_RANG)
            self.entry.configure(textvariable=self.params.text_output)
            self.entry.select_clear()

        self.entry.bind("<FocusIn>", entry_focus_in)
        self.entry.bind("<FocusOut>", entry_focus_out)
        self.entry.bind("<Control-a>", entry_select_all)

        def return_pressed(event: tk.Event) -> None:
            for btn in [
                self.btn_container.btn_start,
                self.btn_container.btn_restart,
            ]:
                if btn.winfo_ismapped():
                    btn.invoke()
            self.focus_set()  # drop focus

        self.entry.bind("<Return>", return_pressed)

        # for every other widget to looses focus:
        # (<Button-1> == onclick event)
        self.bind("<Button-1>", lambda _: self.focus_set())
