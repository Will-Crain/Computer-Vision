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

device = 'Desktop'

if device == 'Desktop':
    os.chdir(r'C:\Users\willc\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\site-packages\cv2\data')

elif device == 'Laptop':
    os.chdir(r'C:\Users\willc\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\cv2\data')

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

SHOW_PUPILS = 0
SHOW_THRESH = 1

MODE = SHOW_PUPILS

#       #   Functions   #       #

def getEyes(inFrame):
    eyes = eyeCascade.detectMultiScale(inFrame, 1.075, 100)#, 1, (2, 2), (5, 5))
    
    return eyes

def getEyeFrames(inFrame, eyes):
    eyeFrames = []
    for (x, y, w, h) in eyes:
        eyeFrames.append(inFrame[x:x+w, y:y+h])

    return eyeFrames

def drawEyes(inFrame, eyes):
    for (x, y, w, h) in eyes:
        cv2.rectangle(inFrame, (x, y), (x+w, y+h), (0, 0, 0), 1)
        pass

    return inFrame

def drawPupils(inFrame, pupils):
    for (x, y, w, h) in pupils:
        cv2.circle(inFrame, (x, y), 3, (0, 0, 255, 127), -1)

    return inFrame

    
#       #    Execute    #       #

def showThresh():
    while True:
        ret0, frameC = cap.read()
        frameG = np.uint8(cv2.cvtColor(frameC, cv2.COLOR_RGB2GRAY))

        gBlur = cv2.GaussianBlur(frameG, (3, 3), 0)
        ret1, frameG = cv2.threshold(gBlur, 220, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#        ret1, frameG = cv2.threshold(gBlur, 220, 255, cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)

        cv2.imshow('Frame', frameG)
        
        k = cv2.waitKey(1)
        if k == 27 or k == ord('q'):
            break
        if k == ord('a'):
            pass      

def showPupils():
    while True:
        ret0, frameC = cap.read()
        frameG = np.uint8(cv2.cvtColor(frameC, cv2.COLOR_RGB2GRAY))

        outFrame = np.copy(frameC)
        
        eyes = getEyes(frameG)
        eyeFrames = getEyeFrames(frameG, eyes)
        
        outFrame = drawEyes(frameC, eyes)

        side = 0
        for (x, y, w, h) in eyes:
            eyeFrame = frameG[y:y+h, x:x+w]
            eyeFrame = cv2.equalizeHist(eyeFrame)
            eyeFrame = cv2.morphologyEx(eyeFrame, cv2.MORPH_OPEN, kernel)

            threshold = cv2.inRange(eyeFrame, 0, 5)
            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #cv2.imshow('tFrame', threshold)
            
            def sortContours(c):
                return cv2.contourArea(c)

            contours.sort(reverse=True, key=sortContours)
            ind = min(0, len(contours)-1)

            if len(contours) == 0:
                continue
            
            larCon = contours[ind]
            center = cv2.moments(larCon)
            
            if not center['m00'] == 0.0:
                cx, cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                cv2.circle(outFrame, (cx+x, cy+y), 4, (0, 148, 255), -1)
                    
        side = side + 1
        cv2.imshow('outFrame', outFrame)
        
        k = cv2.waitKey(1)
        if k == 27 or k == ord('q'):
            break
        if k == ord('a'):
            pass


if MODE == SHOW_THRESH:
    showThresh()
    
elif MODE == SHOW_PUPILS:
    showPupils()
