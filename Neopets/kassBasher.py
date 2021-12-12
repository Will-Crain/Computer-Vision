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


#       #     Setup     #       #

pos =   (478, 443)
size =  (650, 464)
bbox =  (pos[0], pos[1], pos[0]+size[0], pos[1]+size[1])


#       #               #       #

click = False

while True:
    if click == True:
        mouse.position = clickPos
        mouse.
    
    k = cv2.waitKey(10) & 0XFF
    if k == ord('q'):
        break
    
    if k == ord('m'):
        start = not start
    
