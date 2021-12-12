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


#       #               #       #

pos =   (478, 443)
size =  (650, 464)
bbox =  (pos[0], pos[1], pos[0]+size[0], pos[1]+size[1])

blur = (10, 10)

background = cv2.imread('potatoBackground.png')
    
scale = 1.0
width = int(background.shape[1]*scale)
height = int(background.shape[0]*scale)

backgroundRGB = cv2.resize(background, (width, height))

backgroundGRY = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
backgroundGRY_BLUR = cv2.blur(backgroundGRY, blur)

#       #     Setup     #       #

#       #               #       #

start = True

while True:
    screenCap = imageGrab.grab(bbox).convert('RGB')
    screenCap = np.array(screenCap)
    

    screenCapRGB = cv2.cvtColor(screenCap, cv2.COLOR_BGR2RGB)
    screenCapGRY = cv2.cvtColor(screenCap, cv2.COLOR_BGR2GRAY)
    screenCapGRY_BLUR = cv2.blur(screenCapGRY, blur)
    
    frame = np.copy(screenCapRGB)
    frame = cv2.resize(frame, (width, height))
    
    diff = cv2.absdiff(screenCapGRY_BLUR, backgroundGRY_BLUR)
    outImg = np.zeros_like(diff)
    blackImg = np.zeros_like(diff)
    whiteImg = np.ones_like(diff)*255

    # mask = cv2.inRange(diff, 1, 255)
    mask = cv2.blur(diff, blur)
    mask = cv2.inRange(mask, 1, 255)

    if start == True:
        params = cv2.SimpleBlobDetector_Params()

        params.blobColor = 255

        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 10000

        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False
        
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(mask)

        # print(keypoints)
        
        frame = cv2.drawKeypoints(mask, keypoints, np.array([]), (255, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    
    cv2.imshow('Game', frame)
    
    k = cv2.waitKey(10) & 0XFF
    if k == ord('q'):
        break
    
    if k == ord('m'):
        start = not start
    
