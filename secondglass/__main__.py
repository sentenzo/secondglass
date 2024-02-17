from secondglass.timer import Timer  # noqa: F401
from secondglass.ui import ConsoleUI  # noqa: F401
from secondglass.ui.tkbootstrap import TkbAppWindow

if __name__ == "__main__":
    # TkbUI(Timer()).run()
    # ConsoleUI(Timer()).run()
    TkbAppWindow().mainloop()
