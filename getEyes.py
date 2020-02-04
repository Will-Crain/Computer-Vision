#       #       #       #       #
#       # Eye Detection #       #
#       #       #       #       #


#       #    Impoort    #       #

import sys
import os
import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time
import keyboard
from directKeys import moveMouseTo, click, queryMousePosition, mouseDown, mouseUp


#       #     Setup     #       #

cap = cv2.VideoCapture(0)

os.chdir(r'C:\Users\willc\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\cv2\data')

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')


#       #   Functions   #       #

def getEyes(inFrame):
    eyes = eyeCascade.detectMultiScale(inFrame, 1.3, 5)
    
    return eyes

def drawEyes(inFrame, eyes):
    for (x, y, w, h) in eyes:
        cv2.rectangle(inFrame, (x, y), (x+w, y+h), (0, 0, 0), 1)

    return inFrame

    
#       #    Execute    #       #

while True:
    ret, frameC = cap.read()
    frameG = cv2.cvtColor(frameC, cv2.COLOR_RGB2GRAY)
    frameG = np.uint8(frameG)
    
    eyes = getEyes(frameG)
    outFrame = drawEyes(frameC, eyes)
    
    cv2.imshow('Frame', outFrame)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break
    if k == ord('a'):
        pass
