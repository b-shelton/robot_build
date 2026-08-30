from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
Device.pin_factory = LGPIOFactory(chip=15)

from gpiozero import Motor
from time import sleep

left = Motor(forward=17, backward=27, enable=22, pwm=True)
right = Motor(forward=23, backward=24, enable=25, pwm=True)

print("Left forward")
left.forward(0.6)
sleep(1)
left.stop()

print("Right forward")
right.forward(0.6)
sleep(1)
right.stop()

print("Both forward")
left.forward(0.6)
right.forward(0.6)
sleep(2)
left.stop()
right.stop()
