import tkinter as tk
from typing import Callable

import ttkbootstrap as tb

from secondglass.config import SETTINGS
from secondglass.player import play_beep
from secondglass.screensaver import SCREENSAVER_PREVENTER

LIGHT_THEME_LIST = ["cerculean", "cosmo", "litera"]
DARK_THEME_LIST = ["darkly", "superhero"]

SOUND_LIST = list(SETTINGS["AUDIOFILES"])
# ["wood", "hit", "spin", "rattle", "ding", "metalic"]


class ContextMenu(tb.Menu):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, tearoff=0)
        self.create_theme_menu()
        self.create_sound_menu()
        self.create_screensaver_menu()

    def create_theme_menu(self) -> None:
        theme_menu = tb.Menu(self, tearoff=0)

        def theme_switch_closure(theme_name: str) -> Callable[[], None]:
            def theme_switch() -> None:
                tb.Style().theme_use(theme_name)
                SETTINGS["DYNAMIC"]["ui_theme"] = theme_name
                self.master.input_frame.btn_container.rebind_font()  # 😑

            return theme_switch

        self.theme_var = tb.StringVar(value=SETTINGS["DYNAMIC"]["ui_theme"])
        for theme in LIGHT_THEME_LIST + ["|"] + DARK_THEME_LIST:
            if theme == "|":
                theme_menu.add_separator()
            else:
                theme_menu.add_radiobutton(
                    label=theme,
                    value=theme,
                    command=theme_switch_closure(theme),
                    variable=self.theme_var,
                )
        self.add_cascade(label="theme", menu=theme_menu)

    def create_sound_menu(self) -> None:
        sound_menu = tb.Menu(self, tearoff=0)

        def sound_switch_closure(sound_name: str) -> Callable[[], None]:
            def sound_switch() -> None:
                SETTINGS["DYNAMIC"]["sound"] = sound_name
                play_beep(update=True)
                # `play_beep(update=True)` must be called at least once
                #   to update the `_sound` variable

            return sound_switch

        self.sound_var = tb.StringVar()
        for name in SOUND_LIST:
            sound_menu.add_radiobutton(
                label=name,
                value=name,
                variable=self.sound_var,
                command=sound_switch_closure(name),
            )

        self.add_cascade(label="sound", menu=sound_menu)
        self.sound_var.set(SETTINGS["DYNAMIC"]["sound"])

    def create_screensaver_menu(self) -> None:

        self.screensaver_var = tb.BooleanVar()

        self.add_checkbutton(
            label="prevent screensaver",
            variable=self.screensaver_var,
        )

        def on_screensaver_toggle(
            name: str, ind: str | int, method: str
        ) -> None:
            new_value = self.screensaver_var.get()
            SCREENSAVER_PREVENTER.prevent(new_value)
            SETTINGS["DYNAMIC"]["prevent_screensaver"] = str(new_value)

        self.screensaver_var.trace_add("write", on_screensaver_toggle)
        self.screensaver_var.set(SETTINGS["DYNAMIC"]["prevent_screensaver"])

    def _right_click_handler(self, event: tk.Event) -> None:
        self.post(event.x_root, event.y_root)
        # self.tk_popup(event.x_root, event.y_root)

    def activate(self) -> None:
        self.master.bind_all("<Button-3>", self._right_click_handler)
