import cv2 as cv
import os 
import pickle
import numpy as np
import cvzone

cap = cv.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath,path)))

#Load the encoding file
print("Loading the encode file....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, StudentIds = encodeListKnownWithIds
print('encode file loaded')

while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[0]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            y1, x1, y2, x2 = faceLoc
            y1, x1, y2, x2 = y1*4, x1*4, y2*4, x2*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)


    #cv.imshow('Webcam', img)
    cv.imshow('Face Attendence', imgBackground)
    cv.waitKey(1) 