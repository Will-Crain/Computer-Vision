import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

#cap0 = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(1)

#calRet0, calFrame0 = cap0.read()
#calRet1, calFrame1 = cap1.read()

img0 = cv2.imread('stereoL.png')
img1 = cv2.imread('stereoR.png')

img0G = cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
img1G = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

while True:
#    ret0, frame0 = cap0.read()
#    ret1, frame1 = cap1.read()

#    ret1, frame1 = cv2.flip(ret1, 1), cv2.flip(frame1, 1)

    stereo = cv2.StereoBM_create(numDisparities=32, blockSize=5)
    disparity = stereo.compute(img0G, img1G)
    cv2.imshow('Frame0', disparity)


    orb = cv2.ORB_create()


    
    kp0, des0 = orb.detectAndCompute(img0, None)
    kp1, des1 = orb.detectAndCompute(img1, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    matches = bf.match(des0, des1)
    #matches = sorted(matches, key = lambda x:x.distance)

    show = matches[:5]

    testImg = cv2.drawMatches(img0, kp0, img1, kp1, show, None, matchColor=(0, 0, 255), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv2.imshow('testFrame', testImg)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break


cap0.release()
cap1.release()
cv2.destroyAllWindows()
