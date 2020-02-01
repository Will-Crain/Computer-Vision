import sys
print(sys.executable)

import numpy as np
from PIL import ImageGrab as imageGrab
import matplotlib
from matplotlib import pyplot as plt
import cv2
import time
import keyboard
from directKeys import moveMouseTo, click, queryMousePosition, mouseDown, mouseUp

alpha = 0.5
cap = cv2.VideoCapture(0)

lastTime = time.time()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

scale = 1.0

dotSize = 0
dot = [0, 0]
down = False

while True:
    
    ret, frame = cap.read()
    
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    frame = cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)
    size = (frame.shape[1], frame.shape[0])

    outFrame = frame.copy()

    #   #   #   #   #
        
    screen0 = np.array(imageGrab.grab())
    screen1 = cv2.resize(screen0, size, interpolation = cv2.INTER_AREA)
    screen2 = cv2.cvtColor(screen1, cv2.COLOR_BGR2RGB)

    #   #   #   #   #

    # Mask 0 is a Light channel mask
    testScreen = cv2.cvtColor(outFrame, cv2.COLOR_RGB2HLS)
    channel0 = testScreen[:, :, 0]
    channel1 = testScreen[:, :, 1]
    channel2 = testScreen[:, :, 2]
    mask0 = cv2.inRange(channel1, 120, 255)
    outMask0 = cv2.bitwise_and(testScreen, testScreen, mask = mask0)

    outFrame[outMask0 == 0] = 0
    outFrame[outMask0 != 0] = 255

    # Mask 1 is skin mask
    lower = np.array([100, 77, 133], dtype = 'uint8')
    upper = np.array([255, 127, 173], dtype = 'uint8')

    frameYCrCb = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB)
    Y, Cb, Cr = cv2.split(frameYCrCb)
    
    skinMask = cv2.inRange(frameYCrCb, lower, upper)
    skinMask0 = skinMask
    
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
    skin[skin != 0] = 255

    Y = cv2.inRange(Y, 140, 255)
    Cb = cv2.inRange(Cb, 75, 127)
    Cr = cv2.inRange(Cr, 131, 173)
    Z = np.zeros_like(Y)

    #   #   #   #   #

    threshed = cv2.Canny(frame, 200, 400)
    
    edgeFrame = frame.copy()
    edgeFrame[threshed == 255] = 255
    edgeFrame[threshed != 255] = 0

    edgeFrameG = cv2.cvtColor(edgeFrame, cv2.COLOR_RGB2GRAY)

    #param1 500 param2 18
    circles = cv2.HoughCircles(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=500, param2=18, minRadius=10, maxRadius=20)
    if circles is not None:
        circles = circles[0]
        #circles = np.uint16(np.around(circles))

        center = (circles[0][0], circles[0][1])
        radius = circles[0][2]
        color = (0, 0, 255)
        thickness = -1
        cv2.circle(frame, center, radius, color, thickness)
        
        dotSize = radius
        dot = center
        
        for i in range(len(circles)):
            center = (circles[i][0], circles[i][1])
            radius = circles[i][2]
            color = (0, 0, 255)
            thickness = 1
            cv2.circle(frame, center, radius, color, thickness)


    #   #   #   #   #

    rX = screen0.shape[0]/frame.shape[0]
    rY = screen0.shape[1]/frame.shape[1]

    mouse = queryMousePosition()
    toPos = [int(dot[0] * rY), int(dot[1] * rX)]

    if circles is not None:
        pass
#        moveMouseTo(toPos[0], toPos[1])
#        if dotSize >= 17.0:
#            mouseDown(toPos[0], toPos[1])
#            if down == False:
#                down = True
#            
#       if dotSize < 17.0:
#            if down == True:
#                down = False
#                mouseUp(toPos[0], toPos[1])
#            moveMouseTo(toPos[0], toPos[1])
        
    #   #   #   #   #

    # hstack([])
    outData = frame
    #outData = cv2.addWeighted(screen2, 0, frame, 1, 0.0)
    
    cv2.imshow('Frame0', outData)
    #cv2.imshow('Frame1', frame)

    
    nowTime = time.time()
    k = cv2.waitKey(1)

    # 27 is Escape
    if k == 27 or k == ord('q'):
        break
    if k == ord('a'):
        print(nowTime - lastTime)

    lastTime = nowTime

    

cap.release()
cv2.destroyAllWindows()
