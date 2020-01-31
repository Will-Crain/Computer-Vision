import numpy as np
import cv2

cap = cv2.VideoCapture(0)
k = 0
i = 300

while k<i:
    ret, frame = cap.read()
    cv2.imshow('Frame', frame)

    k++
