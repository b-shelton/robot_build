"""Week 6: Obstacle Avoidance v1.

Drives forward on its own. When something is closer than SAFE_DISTANCE,
it stops, backs up, turns a random direction, and carries on.

Run on the Pi:  python3 ~/robot_build/avoid.py   (Ctrl+C to stop)
"""
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
Device.pin_factory = LGPIOFactory(chip=15)  # re-check with `gpiodetect` if this breaks

import random
import signal
from time import sleep
from gpiozero import Motor, DistanceSensor

left = Motor(forward=17, backward=27, enable=22, pwm=True)
right = Motor(forward=23, backward=24, enable=25, pwm=True)
sensor = DistanceSensor(echo=6, trigger=5, max_distance=2)

# --- Tune these together (Wednesday's job) ---
SAFE_DISTANCE = 0.20  # meters: react when something is closer than this
DRIVE_SPEED = 0.5     # forward/backward speed (0 to 1)
TURN_SPEED = 0.45     # spin speed; spins at 0.6 felt too quick. Raise it if the motors just hum.
BACKUP_TIME = 0.5     # seconds of reversing
TURN_TIME = 0.4       # seconds of spinning (longer = bigger turn)


def stop():
    left.stop()
    right.stop()


def _shutdown(signum, frame):
    raise SystemExit  # lets the `finally` below stop the motors


# If the SSH connection drops (SIGHUP) or the script is killed (SIGTERM),
# still stop the motors instead of leaving the robot driving.
signal.signal(signal.SIGHUP, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

try:
    print("Driving on my own. Ctrl+C to stop.")
    while True:
        distance = sensor.distance
        if distance < SAFE_DISTANCE:
            print(f"Obstacle at {distance * 100:.0f} cm: backing up")
            stop()
            sleep(0.1)
            left.backward(DRIVE_SPEED)
            right.backward(DRIVE_SPEED)
            sleep(BACKUP_TIME)

            if random.choice([True, False]):
                print("  turning right")
                left.forward(TURN_SPEED)
                right.backward(TURN_SPEED)
            else:
                print("  turning left")
                left.backward(TURN_SPEED)
                right.forward(TURN_SPEED)
            sleep(TURN_TIME)
            stop()
        else:
            left.forward(DRIVE_SPEED)
            right.forward(DRIVE_SPEED)
        sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    stop()
    sensor.close()
    print("Stopped.")
