# flake8: noqa
# type: ignore

import tkinter as tk
from cgitb import text
from textwrap import fill
from tkinter.font import Font

import ttkbootstrap as tb
import ttkbootstrap.constants as c

root = tb.Window(
    title="123",
    themename="simplex",
    minsize=(280, 120),
)  # "journal",
# root.title =
# root.geometry = (100, 500)


s = tb.Style()
s.configure("My1.TFrame", background="#a22")
s.configure(
    "My2.TFrame",
    background="#999",
)

tb.Progressbar(
    root,
    maximum=1.0,
    value=0.65,
    bootstyle=c.DEFAULT,
).place(
    anchor=c.CENTER,
    relheight=1.1,
    relwidth=1.1,
    relx=0.5,
    rely=0.5,
)

input_frame = tb.Frame(root)
padding = 16
input_frame.pack(
    expand=c.YES,
    fill=c.BOTH,
    padx=padding,
    pady=padding,
)
input_container = tb.Frame(
    input_frame,
    # style="My2.TFrame",
)
# input_container.pack(
#     # expand=c.YES,
#     fill=c.X,
#     padx=padding,
#     pady=padding,
# )
input_container.place(
    anchor=c.CENTER,
    relx=0.5,
    rely=0.5,
    relwidth=1.0,
    # bordermode=c.INSIDE,
)
tb.Label(input_container).pack(padx=4)  # margin
timer_text = tb.StringVar(value="5 minutes")
tbx = tb.Entry(
    input_container,
    textvariable=timer_text,
    justify=c.CENTER,
    font=Font(size=16),
)
tbx.pack(
    fill=c.X,
    # expand=c.YES,
    padx=4,
)

btn_container = tb.Frame(
    input_container,
    style="My2.TFrame",
)
btn_container.pack(
    # expand=c.YES,
    # fill=c.BOTH,
    side=c.TOP,
)

btn_resume = tb.Button(
    btn_container, text="resume", bootstyle=(c.LINK), cursor="hand2"
)
btn_restart = tb.Button(
    btn_container, text="restart", bootstyle=(c.LINK), cursor="hand2"
)
btn_stop = tb.Button(
    btn_container, text="stop", bootstyle=(c.LINK), cursor="hand2"
)
btn_restart.pack(side=c.LEFT)
btn_resume.pack(side=c.LEFT)
btn_stop.pack(side=c.LEFT)

# frame1 = tb.Frame(style="My1.TFrame", height=100, width=200)
# frame1.pack()
# my_button = tb.Button(frame1, text="click", bootstyle=c.PRIMARY)
# my_button.pack(pady=20, padx=40)
# frame1.pack_propagate(c.NO)

# frame2 = tb.Frame(style="My2.TFrame", height=100, width=200)
# frame2.pack(
#     expand=c.NO,
# )
# my_lable = tb.Label(
#     frame2,
#     text="hhh",
#     font=("Arial", 12),
#     bootstyle=(c.WARNING, c.INVERSE),
# )
# my_lable.pack(pady=50)

root.mainloop()
