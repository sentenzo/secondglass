from secondglass.timer import Timer
from secondglass.ui import ConsoleUI, TkbUI  # noqa: F401

if __name__ == "__main__":
    TkbUI(Timer()).run()
