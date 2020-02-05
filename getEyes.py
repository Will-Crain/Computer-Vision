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

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


#       #   Functions   #       #

def getEyes(inFrame):
    eyes = eyeCascade.detectMultiScale(inFrame, 1.3, 5)
    
    return eyes

def getEyeFrames(inFrame, eyes):
    eyeFrames = []
    for (x, y, w, h) in eyes:
        eyeFrames.append(inFrame[x:x+w, y:y+h])

    return eyeFrames

def drawEyes(inFrame, eyes):
    for (x, y, w, h) in eyes:
        pass
        #cv2.rectangle(inFrame, (x, y), (x+w, y+h), (0, 0, 0), 1)

    return inFrame

def drawPupils(inFrame, pupils):
    for (x, y, w, h) in pupils:
        cv2.circle(inFrame, (x, y), 3, (0, 0, 255, 127), -1)

    return inFrame

    
#       #    Execute    #       #

while True:
#    ret, frameC = cap.read()
    frameC = cv2.imread(r'C:\Users\willc\OneDrive\Documents\GitHub\Computer-Vision\testGetEyes.png')
    frameG = cv2.cvtColor(frameC, cv2.COLOR_RGB2GRAY)
    frameG = np.uint8(frameG)

    outFrame = np.copy(frameC)
    
    eyes = getEyes(frameG)
    eyeFrames = getEyeFrames(frameG, eyes)
    
    outFrame = drawEyes(frameC, eyes)

    side = 0
    for (x, y, w, h) in eyes:
        eyeFrame = frameG[y:y+h, x:x+w]
        eyeFrame = cv2.equalizeHist(eyeFrame)
        eyeFrame = cv2.morphologyEx(eyeFrame, cv2.MORPH_OPEN, kernel)

        threshold = cv2.inRange(eyeFrame, 5, 10)
        contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            print([c])
            #cv2.drawContours(outFrame, [c], 0, (0, 0, 0), 1)
    
        lCon = None
        if len(contours) > 1:
            maxArea = 0
            for c in contours:
                area = cv2.contourArea(c)
                if area > maxArea:
                    maxArea = area
                    lCon = c

        if lCon is not None:
            center = cv2.moments(c)
            if not center['m00'] == 0.0:
                cx, cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                cv2.circle(outFrame, (cx+x, cy+y), 5, (0, 0, 255), 1)
                
    side = side + 1
    cv2.imshow('outFrame', outFrame)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break
    if k == ord('a'):
        pass
