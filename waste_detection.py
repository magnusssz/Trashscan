#################################################################################
#                                                                               #
#                           UFPA - Projetos I                                   #
#                           Projeto Trashscan                                   #
#               Lixeira Inteligente de Separação Automática                     #
#                                                                               #
#   Cibele Sodré, Gustavo Silva, Letícia Amorim, Mariana Ribeiro, Tainá Baia    #
#                                                                               #
#################################################################################

from ultralytics import YOLO as yolo
import cv2
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, Servo, DistanceSensor
from RpiMotorLib import RpiMotorLib
from time import sleep
import os

#Inicializando funções
Device.pin_factory = PiGPIOFactory()
sensor = DistanceSensor(echo=15, trigger=14, threshold_distance = 0.12)
servo = Servo(18, min_pulse_width=.0007, max_pulse_width=.0026)
model = yolo('trashscan.pt')
servo.min() #Calibração do Servo

#Inicializando variáveis
i = 1
pos = 1
direction = 21
step = 20
path = 'home/lprad/Desktop'

metal = [0]
paper = [1, 2, 3]
plastic = [4, 5, 6, 7, 8, 9, 10, 11]
glass = [12]

#Função para abrir o Servo Motor
def open_trapdoor():
    servo.value = 0.2
    sleep(1.5)
    servo.min()

#Função para calcular e mover o Stepper Motor para o recipiente de saída relativo à última posição 
def position(goto):
    global pos
    takesteps = goto - pos
    stepper = RpiMotorLib.A4988Nema(direction, step, (-1,-1,-1), "A4988")
    stepper.motor_go(takesteps < 0, "Full", abs(takesteps * 304), .0005, False, .05)
    pos = goto

#Função para capturar uma foto da webcam USB e salvá-la em disco
def capture(): 
    cam = cv2.VideoCapture(0)
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

#Loop principal de inferência
while True:
    sensor.wait_for_in_range()
    sleep(1.5)
    source = capture()

    results = model(source, max_det = 1, conf = 0.5)
    detection = results[0].boxes
    results[0].show()

    if len(detection) == 0:
        print('Nada Detectado')
        position(4)
        open_trapdoor()
    else:
        classid = int(detection[0].cls.item())
        if classid in metal:
            print("Metal")
            position(1)
            open_trapdoor()
        elif classid in paper:
            print("Papel")
            position(2)
            open_trapdoor()
        elif classid in plastic:
            print("Plastico")
            position(3)
            open_trapdoor()
        elif classid in glass:
            print("Vidro")
            position(4)
            open_trapdoor()