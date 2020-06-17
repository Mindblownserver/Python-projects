import cv2
import numpy as np
from action import terminal_open
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video = cv2.VideoCapture(1)
num = 5
while num > 0:
    success, img = video.read()
    flipped = cv2.flip(img, 1)
    img_gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.1, minNeighbors=10)

    for (x, y, w, h) in faces:
        cv2.rectangle(flipped, (x, y), (x+w, y+h), (250, 60, 100), 3)
        cv2.imwrite("Captured {} action.png".format(num), img)
        num -= 1
terminal_open()
