import sys
import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click


gameBounds =    [312, 305, 312+1280, 305+678]
screen = np.array(ImageGrab.grab(bbox=gameBounds))
print("Hello, world")

cv2.imshow('Test', screen)
# cv2.imwrite('Test.png', screen)

# screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
