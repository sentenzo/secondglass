import ttkbootstrap as tb

from secondglass.helpers import pyinstaller_fix_path

from .main_frame import MainFrame
from .params import UI_THEME, WINDOW_INIT_SIZE, WINDOW_MIN_SIZE


class AppWindow(tb.Window):
    def __init__(self) -> None:
        icon_path = pyinstaller_fix_path(
            "secondglass/resources/icons/clock_24.png"
        )
        super().__init__(
            title="SecondGlass",
            themename=UI_THEME,
            minsize=WINDOW_MIN_SIZE,
            size=WINDOW_INIT_SIZE,
            iconphoto=icon_path,
        )
        main_frame = MainFrame(self)
        main_frame.update()  # to get a correct hwnd in ProgressIndicator
        main_frame.create_all()
        main_frame.pack_all()
        main_frame.animate_all()


if __name__ == "__main__":
    AppWindow().mainloop()
