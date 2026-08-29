from gpiozero import Motor
from time import sleep

left = Motor(forward=17, backward=27, pwm=True)
right = Motor(forward=23, backward=24, pwm=True)

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
