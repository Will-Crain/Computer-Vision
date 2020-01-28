import numpy as np
from PIL import ImageGrab as imageGrab
from PIL import Image
import cv2
import os

#path = os.getcwd() + '\\video'
#os.chdir(path)

width = 640
height = 480

images = []

for i in range(0, 28):
    images.append(cv2.imread('Frame' + str(i) + '.png'))

def genVideo():
    imageFolder = '.'
    
    video = cv2.VideoWriter('handSkeletonization.avi', 0, 5, (width, height))
    
    for image in images:
        video.write(image)

    cv2.destroyAllWindows()
    video.release()

genVideo()


