#       #    Impoort    #       #

import sys
import os
import numpy as np
from numpy import mean

from PIL import ImageGrab as imageGrab

import cv2
import time
import keyboard

from directKeys import moveMouseTo, click, queryMousePosition, mouseDown, mouseUp

#        moveMouseTo(toPos[0], toPos[1])
#        if dotSize >= 17.0:
#            mouseDown(toPos[0], toPos[1])
#            if down == False:
#                down = True
#            
#       if dotSize < 17.0:
#            if down == True:
#                down = False
#                mouseUp(toPos[0], toPos[1])
#            moveMouseTo(toPos[0], toPos[1])


#       #               #       #

pos =   (640, 0)
size =  (640, 360)
bbox =  (pos[0], pos[1], pos[0]+size[0], pos[1]+size[1])

blur = (2, 2)
    
scale = 0.5
width = int(size[0]*scale)
height = int(size[1]*scale)

#       #     Setup     #       #

#       #               #       #

while True:
    screenCap = imageGrab.grab(bbox).convert('HSV')
    screenCap = np.array(screenCap)

    screepCapRGB = cv2.cvtColor(screenCap, cv2.COLOR_BGR2RGB)
    screenCapHSV = cv2.cvtColor(screenCap, cv2.COLOR_BGR2HSV)
    screenCapGRY = cv2.cvtColor(screenCap, cv2.COLOR_BGR2GRAY)

    screenCapR = screepCapRGB[:, :, 0]
    screenCapV = screenCapHSV[:, :, 2]

    screenCapHSV_BLUR = cv2.blur(screenCapHSV, blur)
    screenCapGRY_BLUR = cv2.blur(screenCapGRY, blur)

    processFrame = screenCapHSV[:, :, 1]
    threshold = cv2.inRange(processFrame, 50, 100)

    

    frame = threshold
    
    cv2.imshow('Game', frame)
    
    k = cv2.waitKey(10) & 0XFF
    if k == ord('q'):
        break
    
    if k == ord('m'):
        start = not start
    
