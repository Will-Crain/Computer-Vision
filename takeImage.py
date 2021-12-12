import os
import cv2

os.chdir('E')

cap = cv2.VideoCapture(0)
count = 0
num = 0

while True:    
    ret, frame = cap.read()
    cv2.imshow('Test', frame)

    if count >= 20:
        count = 0
        cv2.imwrite('Test'+str(num)+'.png', frame)
        num += 1
        
    count += 1
    
    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        break

