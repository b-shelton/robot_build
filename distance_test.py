"""Week 5: live readings from the HC-SR04 ultrasonic distance sensor.

Wiring:
  HC-SR04 VCC  -> Pi 5V (physical pin 2 or 4)
  HC-SR04 GND  -> Pi GND (any GND pin)
  HC-SR04 Trig -> GPIO 5 (physical pin 29), direct
  HC-SR04 Echo -> 220 ohm -> junction -> 330 ohm -> GND
                  junction -> GPIO 6 (physical pin 31)   (~3.0V, safe for the Pi)

Run on the Pi:  python3 ~/robot_build/distance_test.py   (Ctrl+C to stop)
"""
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
Device.pin_factory = LGPIOFactory(chip=15)  # re-check with `gpiodetect` if this breaks

from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=6, trigger=5, max_distance=2)

try:
    while True:
        print(f"Distance: {sensor.distance * 100:.1f} cm")
        sleep(0.3)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    sensor.close()
