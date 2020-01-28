import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

cap0 = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(2)

calRet0, calFrame0 = cap0.read()
calRet1, calFrame1 = cap1.read()

img0 = cv2.imread('testL.png')
img1 = cv2.imread('testR.png')

img0G = cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
img1G = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

while True:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

#    ret1, frame1 = cv2.flip(ret1, 1), cv2.flip(frame1, 1)

    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=9)

    frame0G = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
    frame1G = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    
    disparity = stereo.compute(img0G, img1G)

    mn = disparity.min()
    mx = disparity.max()

    disparity = np.uint8(6400 * (disparity - mn) / (mx - mn))
    cv2.imshow('Frame0', disparity)


    orb = cv2.ORB_create()


    
    kp0, des0 = orb.detectAndCompute(frame0, None)
    kp1, des1 = orb.detectAndCompute(frame1, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    matches = bf.match(des0, des1)
    #matches = sorted(matches, key = lambda x:x.distance)

    show = matches[:5]

    testImg = cv2.drawMatches(frame0, kp0, frame1, kp1, show, None, matchColor=(0, 0, 255), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    #cv2.imshow('testFrame', testImg)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break


cap0.release()
cap1.release()
cv2.destroyAllWindows()
