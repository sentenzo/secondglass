import ttkbootstrap as tb

from .main_frame import MainFrame

MIN_SIZE = (280, 120)
INIT_SIZE = (400, 180)


class AppWindow(tb.Window):
    def __init__(self) -> None:
        super().__init__(
            title="SecondGlass",
            themename="simplex",
            minsize=MIN_SIZE,
            size=INIT_SIZE,
        )
        main_frame = MainFrame(self)
        main_frame.create_all()
        main_frame.pack_all()


if __name__ == "__main__":
    AppWindow().mainloop()
