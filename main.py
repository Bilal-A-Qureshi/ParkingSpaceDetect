import cv2
import pickle
import cvzone
import numpy as np


width, height = 107,48

with open('CarParkingPos', 'rb') as f:
    posList=pickle.load(f)


cap = cv2.VideoCapture("carPark.mp4")


def checkParkingSpace(imgPro):
    spaces = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-10),scale=0.2)

        if count < 900:
            color = (0, 200, 0)
            thic = 5
            spaces += 1

        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + width, y + height), color, thic)

        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + height - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                       colorR=(0, 200, 0))

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)


    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 25, 16)
    imgmedian = cv2.medianBlur(imgThres, 5)

    kernel=np.ones((3,3),np.uint8)
    imDilate = cv2.dilate(imgThres, kernel, iterations=1)


    checkParkingSpace(imDilate)
    for pos in posList:
        cv2.rectangle(img, pos,(pos[0]+width,pos[1]+height),(255,0,255),2)


    cv2.imshow("img",img)
    #cv2.imshow("imgBlur",imDilate)
    cv2.waitKey(10)