from threading import Event, Thread
from time import sleep

from secondglass.timer import Status, Timer

from .ui import UI

INPUT_PROMPT = "\nTimer: "
TICK_DURATION_SEC = 0.005
RENDER_DELAY_SEC = 0.01


class ConsoleUI(UI):
    def __init__(self) -> None:
        self.timer = Timer()
        self.app_close_event = Event()
        self.ticking_thread = self._create_ticking_thread()

    def _create_ticking_thread(self) -> Thread:
        def ticking_cycle() -> None:
            while not self.app_close_event.is_set():
                try:
                    self.timer.tick()

                    sleep(TICK_DURATION_SEC)
                except KeyboardInterrupt:
                    break
            self.app_close_event.clear()
            self.timer.tick()

        return Thread(target=ticking_cycle)

    def _pretty_print_progress(self) -> None:
        print("\033[A\033[0K" * 2, end="")  # clear two last lines
        print("Progress:", self.timer.progress)
        print("Time left:", self.timer.duration_left_text)

    def run(self) -> None:
        self.timer.start(input(INPUT_PROMPT))
        self.ticking_thread.start()

        print()
        print()
        while self.timer.status != Status.RANG:
            try:
                self._pretty_print_progress()
                sleep(RENDER_DELAY_SEC)
            except KeyboardInterrupt:
                break
        self._pretty_print_progress()
        self.app_close_event.set()
        self.ticking_thread.join()
