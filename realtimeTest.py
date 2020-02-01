import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time

import os

cap = cv2.VideoCapture(1)

calRet, calFrame = cap.read()

#size = (calFrame.shape[1], calFrame.shape[0])
size = (640, 480)

lenSec = 5
fps = 60

lenFrm = fps*lenSec

rFrames = []
pFrames = []

for i in range(0, lenFrm):
    ret, frame = cap.read()

    name = 'frame{}.png'.format(i)
    rFrames.append(frame)
    cv2.imshow('Frame', frame)
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break

print('Finished capturing')

cv2.destroyAllWindows()
cap.release()

protoFile = 'hand/pose_deploy.prototxt'
weightsFile = 'hand/pose_iter_102000.caffemodel'

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
nPoints = 22
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

threshold = 0.2

vid = cv2.VideoWriter('fullProcessed.avi', 0, 60, size)

for j in range(0, lenFrm):
    tFrame = rFrames[j].copy()
    inpBlob = cv2.dnn.blobFromImage(tFrame, 1.0/256, size, (0, 0, 0), swapRB=False, crop=False, ddepth=cv2.CV_32F)
    net.setInput(inpBlob)
    output = net.forward()
    
    points = []
    for i in range(0, nPoints):
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, size)

        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > threshold:
            points.append((int(point[0]), int(point[1])))

        else:
            points.append(None)
            
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(tFrame, points[partA], points[partB], (127, 127, 127), 2)
            cv2.circle(tFrame, points[partA], 3, (255, 0, 0), thickness=1)
            cv2.circle(tFrame, points[partB], 3, (255, 0, 0), thickness=1)

    cv2.circle(tFrame, points[8], 3, (0, 0, 255), thickness=-1)
            
    vid.write(tFrame)
    cv2.imshow('Frame', tFrame)
    pFrames.append(tFrame)
    print('{}/{}'.format(j, lenFrm))

    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break

print('Finished processing')


vid.release()
cv2.destroyAllWindows()
