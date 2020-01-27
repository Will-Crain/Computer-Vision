import sys
print(sys.executable)

import numpy as np
from PIL import ImageGrab as imageGrab
import cv2
import time
import keyboard
from directKeys import moveMouseTo, click, queryMousePosition, mouseDown, mouseUp
import argparse
import sys
from sys import platform

import pyopenpose as op



parser = argparse.ArgumentParser()

cap = cv2.VideoCapture(0)


lastTime = time.time()

scale = 0.6

protoFile = 'hand/pose_deploy.prototxt'
weightsFile = 'hand/pose_iter_102000.caffemodel'
nPoints = 22
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

threshold = 0.2
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def setup():
    params = dict()
    params['model_pose'] = 'BODY_25'
    params['num_gpu_start'] = 0

    return params

params = set_params()
openpose = openPose(params)

def getHandSkeleton(inFrame):    
    outFrame = np.copy(inFrame)
    outFrame = cv2.cvtColor(outFrame, cv2.COLOR_RGB2RGBA)
    
    width = int(outFrame.shape[1])
    height = int(outFrame.shape[0])
    
    inWidth = int(width*scale)
    inHeight = int(height*scale)
    
    inpBlob = cv2.dnn.blobFromImage(inFrame, 1.0/256, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False, ddepth=cv2.CV_32F)
    net.setInput(inpBlob)
    output = net.forward()

    points = []
    for i in range(nPoints):
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, (width, height))

        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > threshold:
            points.append((int(point[0]), int(point[1])))

        else:
            points.append(None)

    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(outFrame, points[partA], points[partB], (127, 127, 127, 255), 2)
            cv2.circle(outFrame, points[partA], 3, (255, 0, 0, 255), thickness=1)
            cv2.circle(outFrame, points[partB], 3, (255, 0, 0, 255), thickness=1)

    dot = points[8]
        
    cv2.circle(outFrame, points[8], 5, (0, 0, 255, 255), thickness=-1)

    return [outFrame, dot]
    

def getContours(outFrame):
    ret, threshedFrame = cv2.threshold(cv2.cvtColor(outFrame, cv2.COLOR_RGB2GRAY), 127, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(threshedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    wThresh = 30
    hThresh = 30

    xB, yB, wB, hB = 0, 0, 0, 0
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        if w*h > wB*hB:
            xB = x
            yB = y
            wB = w
            hB = h

    outFrame = outFrame[yB:yB+hB, xB:xB+wB]
    lBox = (xB, yB, outFrame.shape[1], outFrame.shape[0])
    return [outFrame, lBox]


while True:
    ret, frame = cap.read()
    
    screen0 = np.array(imageGrab.grab())

    contours, box = getContours(frame)
    x, y, w, h = box

    hand, dot = getHandSkeleton(frame)
    
    nowTime = time.time()
    
#    print('fps:\t{}'.format(1/(nowTime - lastTime)))

    outData = hand
    #outData = np.hstack([contours, iData0])
    #outData = cv2.addWeighted(frame, 1.0, blank, 1.0, 0.0)
    #outData = blank
    cv2.imshow('Frame0', outData)
    
    rX = screen0.shape[0]/frame.shape[0]
    rY = screen0.shape[1]/frame.shape[1]

    if dot is not None:
        toPos = [int(dot[0] * rY), int(dot[1] * rX)]
        print(toPos)

        moveMouseTo(toPos[0], toPos[1])

    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break
    if k == ord('a'):
        print(nowTime - lastTime)

    lastTime = nowTime


cap.release()
cv2.destroyAllWindows()
