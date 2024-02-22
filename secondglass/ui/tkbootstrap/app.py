import ttkbootstrap as tb

from secondglass.config import SETTINGS, save_settings
from secondglass.helpers import pyinstaller_fix_path

from ..ui import UI
from .main_frame import MainFrame
from .params import WINDOW_INIT_SIZE, WINDOW_MIN_SIZE


class AppWindow(tb.Window):
    def __init__(self) -> None:
        icon_path = pyinstaller_fix_path("resources/icons/clock_24.png")
        super().__init__(
            title="SecondGlass",
            themename=SETTINGS["DYNAMIC"]["ui_theme"],
            minsize=WINDOW_MIN_SIZE,
            size=WINDOW_INIT_SIZE,
            iconphoto=icon_path,
        )
        main_frame = MainFrame(self)
        main_frame.update()  # to get a correct hwnd in ProgressIndicator
        main_frame.create_all()
        main_frame.pack_all()
        main_frame.animate_all()

        def on_closing() -> None:
            SETTINGS["DYNAMIC"][
                "init_text_input"
            ] = main_frame.params.text_input.get()
            SETTINGS["DYNAMIC"]["ui_theme"] = tb.Style().theme.name
            save_settings(SETTINGS)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)


class TkbUI(UI):
    def run(self) -> None:

        AppWindow().mainloop()
