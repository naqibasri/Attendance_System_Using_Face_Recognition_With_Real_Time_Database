import cv2 as cv
import face_recognition
import pickle_1
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendencerealtime-9bd47-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storagebucket': 'faceattendencerealtime-9bd47.appspot.com'
})


# Importing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_recognition(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding started....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed")

file = open("Encodefile.p", "wb")
pickle_1.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")