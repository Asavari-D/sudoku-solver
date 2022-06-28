import cv2
import numpy as np
from tensorflow.keras.models import load_model

def getModel():
    model = load_model('model-OCR.h5')

    return model

def biggestContours(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    return biggest, max_area


def reorder(mypoints):
    mypoints = mypoints.reshape((4, 2))
    mypointsNew = np.zeros((4, 1, 2), dtype=np.int32)  # new array of shape mentioned with zeros
    add = mypoints.sum(1)
    mypointsNew[0] = mypoints[np.argmin(add)]
    mypointsNew[1] = mypoints[np.argmax(add)]
    diff = np.diff(mypoints, axis=1)
    mypointsNew[2] = mypoints[np.argmin(diff)]
    mypointsNew[3] = mypoints[np.argmax(diff)]

    return mypointsNew


def split(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)

    return boxes

def getPrediction(boxes, model):
    result = []
    for image in boxes:
        #prepare image
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        img = cv2.resize(img, (48, 48))
        img = img/255
        img = img.reshape(1,48,48,1)

        predictions = model.predict(img)
        classIndex = np.argmax(predictions, axis = -1) #to see which class [1 to 9] it belongs to
        probVal = np.amax(predictions)
        # print(classIndex, probVal)

        if probVal > 0.8:
            result.append(classIndex[0])
        else:
            result.append(0)

    return result

def displayNum(img, nums, color = (0,255,0)):
    w = int(img.shape[1]/9)
    h = int(img.shape[0]/9)

    for x in range(0,9):
        for y in range(0,9):
            if nums[(y*9)+x] != 0:
                cv2.putText(img=img, text=str(nums[(y*9)+x]), org=(x*w+int(w/2)-10, int((y+0.8)*h)), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    return img


