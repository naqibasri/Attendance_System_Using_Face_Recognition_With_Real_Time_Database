import cv2 as cv

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while True:
    success, img = cap.read()
    cv.imshow('Face Atendence', img)
    cv.waitKey(1)