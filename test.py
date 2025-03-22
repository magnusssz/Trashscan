import os
import cv2
from ultralytics import YOLO as yolo

path = 'C:/Users/Gustavo/Downloads/projects/trashscan/code'
i = 1

def capture(): 
    cam = cv2.VideoCapture(0)
    ret, frame, = cam.read()
    global i
    while True:
        if os.path.exists('image'+ str(i) + '.jpg'):
            i += 1
        else:
            check = cv2.imwrite('image'+ str(i) + '.jpg', frame)
            if check:
                print('Capture Successful')
            break
    cam.release()

capture()

metal = [0]
paper = [1, 2, 3]
plastic = [4, 5, 6, 7, 8, 9, 10, 11]
glass = [12]

model = yolo('trashscan.pt')
source = str(path) + '/image' + str(i) + '.jpg'

results = model(source, max_det = 1, conf = 0.5)
detection = results[0].boxes
results[0].show()

if len(detection) == 0:
    print('No Object Detected')
else:
    classid = int(detection[0].cls.item())
    if classid in metal:
        print('Metal Detected')
    if classid in paper:
        print('Paper Detected')
    if classid in plastic:
        print('Plastic Detected')
    if classid in glass:
        print('Glass Detected')