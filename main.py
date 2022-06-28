#to remove errors of tensorflow:
print("Setting up")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import cv2
import numpy as np
from functions import *
import solver


img = cv2.imread("sudoku_3.png")
img = cv2.resize(img, (450, 450))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(gray,(5,5),0)
#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
#thresh2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
thresh = cv2.adaptiveThreshold(gray,255,0,1,19,2)
contours, hier = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(thresh, contours, -1, (0,255,0), 25)

biggest, max_area = biggestContours(contours)

if biggest.size != 0:
    biggest = reorder(biggest)

    imgBigContours = img.copy()

    cv2.drawContours(imgBigContours, biggest, -1, (0,255,0),3)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [450, 450], [450, 0], [0, 450]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarped = cv2.warpPerspective(img, matrix, (450,450))
    imgWarped = cv2.cvtColor(imgWarped, cv2.COLOR_BGR2GRAY)

    boxes = split(imgWarped)

    model = getModel()
    numbers = getPrediction(boxes, model)
    # print(numbers)

    # print(num_2d)
    imgDetected = np.zeros((450, 450, 3), np.uint8)
    imgDetected = displayNum(imgDetected, numbers, color=(0,255,0))
    numbers = np.asarray(numbers)
    posArr = np.where(numbers>0, 0, 1)

    num_2d = np.array_split(numbers, 9)
    print(num_2d)
    try:
        solver.sudoku(num_2d,0,0)
    except:
        pass
    print(num_2d)

    list = []
    for i in range(9):
        for j in range(9):
            list.append(num_2d[i][j])
    print(list)

    solvedNos = list*posArr
    imgSolved = np.zeros((450, 450, 3), np.uint8)
    imgSolved = displayNum(imgSolved, solvedNos)

    #overlay
    pts2 = np.float32(biggest)
    pts1 = np.float32([[0, 0], [450, 450], [450, 0], [0, 450]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgInvWarped = img.copy()
    imgInvWarped = cv2.warpPerspective(imgSolved, matrix, (450,450))

    final = cv2.addWeighted(imgInvWarped, 1, img, 0.5, 1)
    print("The solution coming up...")
    cv2.imshow('image', final)
    cv2.waitKey(0)

else:
    print("Sudoku not found, try another image")







