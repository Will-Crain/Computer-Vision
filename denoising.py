import sys
import os
import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frameG =    cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    corrected = cv2.fastNlMeansDenoising(frameG)

    outData = np.hstack([frameG, corrected])
    cv2.imshow('Frame', outData)

    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break
