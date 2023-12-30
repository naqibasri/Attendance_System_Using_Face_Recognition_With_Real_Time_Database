import cv2 as cv
import os 

cap = cv.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath,path)))

while True:
    success, img = cap.read()

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[0]

    #cv.imshow('Webcam', img)
    cv.imshow('Face Attendence', imgBackground)
    cv.waitKey(1) 