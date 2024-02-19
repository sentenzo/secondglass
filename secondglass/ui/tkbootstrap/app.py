import ttkbootstrap as tb

from .main_frame import MainFrame
from .params import UI_THEME, WINDOW_INIT_SIZE, WINDOW_MIN_SIZE


class AppWindow(tb.Window):
    def __init__(self) -> None:
        super().__init__(
            title="SecondGlass",
            themename=UI_THEME,
            minsize=WINDOW_MIN_SIZE,
            size=WINDOW_INIT_SIZE,
        )
        main_frame = MainFrame(self)
        main_frame.create_all()
        main_frame.pack_all()
        main_frame.animate_all()


if __name__ == "__main__":
    AppWindow().mainloop()
