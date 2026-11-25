"""Week 3: keyboard remote control over SSH.

Run on the Pi:  python3 ~/robot_build/drive.py
W/A/S/D to drive, SPACE to stop, Q to quit.
"""
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
Device.pin_factory = LGPIOFactory(chip=15)  # re-check with `gpiodetect` if this breaks

import curses
import signal
from gpiozero import Motor

left = Motor(forward=17, backward=27, enable=22, pwm=True)
right = Motor(forward=23, backward=24, enable=25, pwm=True)

SPEED = 0.6


def stop():
    left.stop()
    right.stop()


def drive(stdscr):
    curses.curs_set(0)
    stdscr.timeout(50)  # wait up to 50ms for a key, so the loop doesn't max out the CPU
    stdscr.addstr(0, 0, "W/A/S/D to drive, SPACE to stop, Q to quit")

    while True:
        key = stdscr.getch()
        if key == -1:
            continue  # no key pressed; keep doing whatever we were doing
        key = chr(key).lower() if 0 <= key < 256 else ""

        if key == "w":
            left.forward(SPEED); right.forward(SPEED); status = "Forward"
        elif key == "s":
            left.backward(SPEED); right.backward(SPEED); status = "Backward"
        elif key == "a":
            left.backward(SPEED); right.forward(SPEED); status = "Spin left"
        elif key == "d":
            left.forward(SPEED); right.backward(SPEED); status = "Spin right"
        elif key == " ":
            stop(); status = "Stopped"
        elif key == "q":
            break
        else:
            continue

        stdscr.addstr(2, 0, f"{status:<20}")
        stdscr.refresh()


def _shutdown(signum, frame):
    raise SystemExit  # lets the `finally` below stop the motors


# If the SSH connection drops (e.g. phone screen locks) or the script is killed,
# still stop the motors instead of leaving the robot driving.
signal.signal(signal.SIGHUP, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

try:
    curses.wrapper(drive)
finally:
    stop()  # always stop the motors, even after Ctrl+C or a crash
