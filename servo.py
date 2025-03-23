from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, Servo
from time import sleep

Device.pin_factory = PiGPIOFactory()
servo = Servo(18, min_pulse_width=.0007, max_pulse_width=.0026)

servo.mid()
sleep(3)
servo.min()
