import cv2 as cv
import os 
import pickle_1
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendencerealtime-9bd47-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storagebucket': 'faceattendencerealtime-9bd47.appspot.com'
})

bucket = storage.bucket()

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
encodeListKnownWithIds = pickle_1.load(file)
file.close()
encodeListKnown, StudentIds = encodeListKnownWithIds
print('encode file loaded')


modeType = 0
counter = 0
id = 0
imgStudent = []
while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            y1, x1, y2, x2 = faceLoc
            y1, x1, y2, x2 = y1*4, x1*4, y2*4, x2*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
        id = StudentIds[matchIndex]
        if counter == 0:
            counter += 1
            modeType = 1

    if counter != 0:
        if counter == 1:
            #Get the data
            studentInfo = db.reference(f'Students/{id}').get()
            # Get the image from the storage
            blob = bucket.get_blob(f'images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv.imdecode(array, cv.COLOR_BGR2RGB)

            cv.putText(imgBackground, str(studentInfo['total_attendence']), (861,125),
                       cv.FONT_HERSHEY_COMPLEX, 1, (225,225,225), 1)
            cv.putText(imgBackground, str(studentInfo['position']), (1006,550),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (225,225,225), 1)
            cv.putText(imgBackground, str(id), (1006,493),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (225,225,225), 1)
            cv.putText(imgBackground, str(studentInfo['standing']), (910,625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
            cv.putText(imgBackground, str(studentInfo['year']), (1025,625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
            cv.putText(imgBackground, str(studentInfo['starting_year']), (1125,625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
            
            (w,h), _ = cv.getTextSize(studentInfo['name'], cv.FONT_HERSHEY_COMPLEX,1,1)
            offset = (414-w)//2
            cv.putText(imgBackground, str(studentInfo['name']), (808+offset,445),
                       cv.FONT_HERSHEY_COMPLEX,1, (50,50,50), 1)
            
            imgBackground[175:175+216, 909,909+216] = imgStudent
    #cv.imshow('Webcam', img)
    cv.imshow('Face Attendence', imgBackground)
    cv.waitKey(1) 