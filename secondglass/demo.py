from time import sleep

from secondglass.timer.timer import Status, Timer


def console_demo() -> None:
    t = Timer()
    t.start(input("\nTimer: "))
    print()
    print()
    while t.status != Status.RANG:
        try:
            t.tick()
            sleep(0.01)
        except KeyboardInterrupt:
            break
    t.tick()
