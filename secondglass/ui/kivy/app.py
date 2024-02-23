from kivy.app import App
from kivy.uix.widget import Widget

from ..ui import UI


class MainFrame(Widget):
    pass


class MyApp(App):
    def build(self) -> MainFrame:
        return MainFrame()


class KivyUI(UI):
    def run(self) -> None:
        MyApp().run()
