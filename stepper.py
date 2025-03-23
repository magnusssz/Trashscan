from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

direction = 21
step = 20
stepper = RpiMotorLib.A4988Nema(direction, step, (-1,-1,-1), "A4988")
stepper.motor_go(True, "Full", 100, .0005, False, .05)
GPIO.cleanup()
