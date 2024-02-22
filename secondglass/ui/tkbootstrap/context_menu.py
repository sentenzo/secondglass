import tkinter as tk
from typing import Callable

import ttkbootstrap as tb

LIGHT_THEME_LIST = ["cerculean", "cosmo", "litera"]
DARK_THEME_LIST = ["darkly", "superhero"]

SOUND_LIST = {
    "wood": "185846__lloydevans09__light-wood.wav",
    "hit": "186401__lloydevans09__balsa-hit-1.wav",
    "spin": "186993__lloydevans09__wood-spin.wav",
    "rattle": "332001__lloydevans09__spray_can_rattle.wav",
    "ding": "338148__artordie__ding.wav",
    "metalic": "464420__michael_grinnell__metalic_ching_keys_2.wav",
}


class ContextMenu(tb.Menu):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, tearoff=0)
        self.create_theme_menu()
        self.create_sound_menu()

    def create_theme_menu(self) -> None:
        theme_menu = tb.Menu(self, tearoff=0)

        def theme_switch_closure(theme_name: str) -> Callable[[], None]:
            def theme_switch() -> None:
                tb.Style().theme_use(theme_name)

            return theme_switch

        for theme in LIGHT_THEME_LIST:
            theme_menu.add_radiobutton(
                label=theme, command=theme_switch_closure(theme)
            )
        theme_menu.add_separator()
        for theme in DARK_THEME_LIST:
            theme_menu.add_radiobutton(
                label=theme, command=theme_switch_closure(theme)
            )
        self.add_cascade(label="Theme", menu=theme_menu)

    def create_sound_menu(self) -> None:
        sound_menu = tb.Menu(self, tearoff=0)
        sound_menu.add_radiobutton(label="wood")
        sound_menu.add_radiobutton(label="hit")
        sound_menu.add_radiobutton(label="spin")
        sound_menu.add_radiobutton(label="rattle")
        sound_menu.add_radiobutton(label="ding")
        sound_menu.add_radiobutton(label="metalic")
        self.add_cascade(label="Sound", menu=sound_menu)

    def _right_click_handler(self, event: tk.Event) -> None:
        self.post(event.x_root, event.y_root)
        # self.tk_popup(event.x_root, event.y_root)

    def activate(self) -> None:
        self.master.bind_all("<Button-3>", self._right_click_handler)
