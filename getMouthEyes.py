#       #       #       #       #
#       # Eye Detection #       #
#        Mouth Detection        #
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

cap = cv2.VideoCapture(1)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
mouthCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mouth.xml')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

HIGHLIGHT = 0

MODE = HIGHLIGHT
    
#       #    Execute    #       #

def highlight() :
    while True:
        ret0, frameC = cap.read()
        frameG = np.uint8(cv2.cvtColor(frameC, cv2.COLOR_RGB2GRAY))

        faces = faceCascade.detectMultiScale(frameG, 1.3, 5)
        outFrame = (0, 0, 0, 0)
        
        for (x, y, w, h) in faces:            
            faceG = frameG[y:y+h, x:x+w]
            faceC = frameC[y:y+h, x:x+w]

            amt = 0.2

            yi = int(y*(1-amt))
            yf = int((y+h)*(1+amt))
            xi = int(x*(1-amt))
            xf = int((x+w)*(1+amt))
            
            outFrame = frameC[yi:yf, xi:xf]

            eyes = eyeCascade.detectMultiScale(faceG)
            mouth = mouthCascade.detectMultiScale(faceG)

            eyeCount = 0
            for (x1, y1, w1, h1) in eyes:
                cv2.rectangle(faceC, (x1, y1), (x1+w1, y1+h1), (0, 0, 0), 1)
                eyeCount += 1
                if eyeCount == 2:
                    break
            
            for (x1, y1, w1, h1) in mouth:
                cv2.rectangle(faceC, (x1, y1), (x1+w1, y1+h1), (50, 50, 50), 3)
                break

        cv2.imshow('Frame', frameC)

        k = cv2.waitKey(1)
        if k == 27 or k == ord('q'):
            break
        if k == ord('a'):
            pass   



#       #    Execute    #       #


if MODE == HIGHLIGHT:
    highlight()
