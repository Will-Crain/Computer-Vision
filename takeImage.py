import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

cap0 = cv2.VideoCapture(1)

calRet0, calFrame0 = cap0.read()

cv2.imwrite('testL.png', calFrame0)
