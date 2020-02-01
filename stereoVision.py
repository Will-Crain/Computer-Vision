import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

calRet0, calFrame0 = cap0.read()
calRet1, calFrame1 = cap1.read()

img0 = cv2.imread('stereoL.png')
img1 = cv2.imread('stereoR.png')

img0G = cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
img1G = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

while True:
    
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

#    frame0 = cv2.imread('stereoL.png')
#    frame1 = cv2.imread('stereoR.png')

    ret1, frame1 = cv2.flip(ret1, 1), cv2.flip(frame1, 1)

    frame0G = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
    frame1G = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

    stereo = cv2.StereoSGBM_create(
        numDisparities=16,
        blockSize=5,
        speckleRange=10,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY,
        P1 = 50,
        P2 = 64
    )

    disparity = stereo.compute(frame0, frame1).astype(np.float32) / 16 + 1
    print(disparity.min())
#    disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)

    data0 = np.hstack([frame0G, frame1G])
    data1 = disparity
    cv2.imshow('Frame1', data1)

    #       #       #       #       #

#    orb = cv2.ORB_create()
    
#    kp0, des0 = orb.detectAndCompute(frame0, None)
#    kp1, des1 = orb.detectAndCompute(frame1, None)

#    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
#    matches = bf.match(des0, des1)
#    matches = sorted(matches, key = lambda x:x.distance)

#    show = matches[:30]

#    testImg = cv2.drawMatches(frame0, kp0, frame1, kp1, show, None, matchColor=(0, 0, 255), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#    cv2.imshow('testFrame', testImg)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break


cap0.release()
cap1.release()
cv2.destroyAllWindows()
