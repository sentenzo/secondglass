from time import sleep

from secondglass.timer.timer import Status, Timer


def _pretty_print(t: Timer) -> None:
    print("\033[A\033[0K", end="")  # clear the last line
    print("\033[A\033[0K", end="")  # clear the last line
    print("Progress:", t.progress)
    print("Time left:", t.duration_left_text)


def console_demo() -> None:
    t = Timer()
    t.start(input("\nTimer: "))
    print()
    print()
    while t.status != Status.RANG:
        try:
            t.tick()
            _pretty_print(t)
            sleep(0.01)
        except KeyboardInterrupt:
            break
    t.tick()


def thread_demo() -> None:
    import threading

    t = Timer()
    t.start(input("\nTimer: "))

    stop_ticking = threading.Event()

    def ticking_cycle() -> None:
        t.tick()
        while not stop_ticking.is_set():
            t.tick()
            sleep(0.005)

    ticking_thread = threading.Thread(target=ticking_cycle)

    ticking_thread.start()

    print()
    print()
    while t.status != Status.RANG:
        try:
            _pretty_print(t)
            sleep(0.01)
        except KeyboardInterrupt:
            break
    _pretty_print(t)
    stop_ticking.set()
    ticking_thread.join()
