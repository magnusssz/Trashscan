import os
import cv2
from ultralytics import YOLO as yolo
from pynput import keyboard
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, Servo
from RpiMotorLib import RpiMotorLib
from time import sleep


print('start')
i = 1
pos = 0
direction = 21
step = 20
Device.pin_factory = PiGPIOFactory()
servo = Servo(18, min_pulse_width=.0007, max_pulse_width=.0026)
path = 'C:/Users/Gustavo/Downloads/projects/trashscan/git'
model = yolo('trashscan.pt')
print('model loaded')
cam = cv2.VideoCapture(0)
print('cam loaded')

metal = [0]
paper = [1, 2, 3]
plastic = [4, 5, 6, 7, 8, 9, 10, 11]
glass = [12]

def open_trapdoor():
    servo.value = 0.2
    sleep(1.5)
    servo.min()

def position(goto):
    takesteps = goto - pos
    stepper = RpiMotorLib.A4988Nema(direction, step, (-1,-1,-1), "A4988")
    stepper.motor_go(takesteps < 0, "Full", takesteps, .0009, False, .05)

def capture(): 
    ret, frame, = cam.read()
    global i
    while True:
        if os.path.exists(f'image{i}.jpg'):
            i += 1
        else:
            cv2.imwrite(f'image{i}.jpg', frame)
            print('Capture Successful')
            break
    cam.release()
    return frame

def on_press(key):
    if key == keyboard.Key.space:
        print('taking frame')
        source = capture()
        print('frame taken')

        results = model(source, max_det = 1, conf = 0.5)
        detection = results[0].boxes
        results[0].show()

        if len(detection) == 0:
            print('No Object Detected')
        else:
            classid = int(detection[0].cls.item())
            if classid in metal:
                position(300)
            elif classid in plastic:
                position(600)
            elif classid in paper:
                position(900)
            elif classid in glass:
                position(1200)
            open_trapdoor()

    if key == keyboard.Key.esc:
        print('stopping')
        return False

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()