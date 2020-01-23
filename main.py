import numpy as np
import PIL
import pyscreenshot as ImageGrab
import cv2
# from directKeys import click, queryMousePosition

gameBounds =    [312, 305, 312+1280, 305+678]
screen0 = ImageGrab.grab(bbox = (312, 305, 312+1280, 305+678))
screen1 = np.asanyarray(screen0)

# cv2.imshow('Test', screen)
# cv2.imwrite('Test.png', screen)

# screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
