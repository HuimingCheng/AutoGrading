# -*- coding: utf-8 -*-
import cv2
import numpy as np
# import matplotlib.pyplot as plt

from PIL import Image
from difflib import SequenceMatcher
from PIL import *
from PIL import ImageEnhance
import time
from pytesseract import image_to_string, image_to_boxes
import os


def findcoordinateOfName(path):
    image = cv2.imread(path)
    height, width  = image.shape[:2]
    crop_img = image[  0:int(height/3), 0:width]
    cv2.imwrite("temp.png", crop_img)
    image = Image.open("temp.png")
    box = image_to_boxes(image).split('\n')
    width , height = image.size

    coordinate = []
    for i in range(len(box)):
        flag = False
        if (box[i][0] == 'n' and box[i + 1][0] == 'a' and box[i + 2][0] == 'm' and box[i + 3][0] == 'e'):
            for j in range(0, 4):
                flag = True
                coordinate.append(box[i+j])

            if(flag):
                break
    coorE = coordinate[3].split(" ")
    return (( int(coorE[1]) , height - int(coorE[4])), ( int(coorE[3]), height - int(coorE[2])))

def image_proc(image, n_pos,name):
    # calculate bounds of interest
    dh = n_pos[1][1] - n_pos[0][1]
    upper = n_pos[0][1] - 2 * dh
    lower = n_pos[1][1] + int(3.5 * dh)
    left = n_pos[1][0]
    right = left + 40 * (n_pos[1][0] - n_pos[0][0])
    crop_img = image[  upper:lower, left:right]

    name = "sample/" + name 
    cv2.imwrite(name, crop_img)
    # image = Image.open("temp.png")
    # return image

def findLengthAndHeight(contour):
    # contour = answerBox[0].getContour()
    x_axis = []
    y_axis = []
    for point in contour:
        x_axis.append(point[0][0])
        y_axis.append(point[0][1])
    x_axis.sort()
    y_axis.sort()
    length = x_axis[-1] - x_axis[0]
    height = y_axis[-1] - y_axis[0]

    return length


def checkSpecial(cnt, contours,smallestWide, crop_image):
    [x, y, w, h] = cv2.boundingRect(cnt)
    if w < smallestWide[0]:
        smallestWide[0] = w

    for contour in contours:
        [x1, y1, w1, h1] = cv2.boundingRect(contour)
        if x - 1.3 * w <x1 < x + 1.3 * w and \
            0.1*w < w1 < 1.3 * w and \
            cv2.contourArea(contour) < 0.3 * cv2.contourArea(cnt) and \
            h1 > 0.1*h and \
            w < 2*smallestWide[0]:
            cv2.drawContours(crop_image, [contour], -1, (0, 255, 0), 2)

            return x, y1,abs(x1-x+w1), y-y1+h
    return x, y, w, h



if __name__ == '__main__':
    # ==============================================================
    # get the sample from original image

    # # imagePath = "/Users/gengruijie/Desktop/未命名文件夹/OneDrive/学习/cs/课外/Github/AutoGrading/learning/Ruijie/handwriting_recognization/original_file/"
    # # allfile = os.listdir(imagePath)
    # # allfile.remove('.DS_Store')
    # # print(allfile)
    # # for element in allfile:
    # #   image = cv2.imread(imagePath+element)
    # #   n_pos = findcoordinateOfName(imagePath+element)
    # #   image = image_proc(image, n_pos,element)
    # #   name = "sample/" + element

    # # Finish to get the sample from original image
    # # ==============================================================

    # imagePath = "/Users/gengruijie/Desktop/未命名文件夹/OneDrive/学习/cs/课外/Github/AutoGrading/learning/Ruijie/handwriting_recognization/sample/"
    # image = cv2.imread(imagePath+"temp3.png")

    # res = image
    # # convert image to grayscale
    # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # # blur the image slightly to remove noise.
    # # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)  # is an alternative way to blur the image
    # # canny edge detection
    # edged = cv2.Canny(gray, 30, 200)


    # # two threshold method.
    # # The first one is normal threshold method
    # # The second one is use Gaussian method which has better effect.
    # # ret,thresh1 = cv2.threshold(gray,150,150,cv2.THRESH_BINARY)
    # thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # try:
    #     (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # except:
    #     (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # # 找到外面的那个框，长度大于2/3的框


    # i = 0

    # lengthList = []
    # temp = res.copy()

    # for cnt in cnts:
    #     lengthList.append(findLengthAndHeight(cnt))
    #     # if True:
    #         # temp = res.copy()
    #         # cv2.drawContours(temp, [cnt], -1, (0, 255, 0), 2)

    #         # cv2.imwrite(str(i) + ".png", temp)
    #         # i += 1
    # largestCnt = cnts[lengthList.index(max(lengthList))]

    # x_axis = []
    # y_axis = []
    # for point in largestCnt:
    #     x_axis.append(point[0][0])
    #     y_axis.append(point[0][1])
    # x_axis.sort()
    # y_axis.sort()
    # maxX = x_axis[-1] - 0.03*(x_axis[-1] - x_axis[0])
    # minX = x_axis[0] + 0.03*(x_axis[-1] - x_axis[0])
    # maxY = y_axis[-1] - 0.05*(y_axis[-1] - y_axis[0])
    # minY = y_axis[0] + 0.03*(y_axis[-1] - y_axis[0])

    crop_img = cv2.imread("learnLetter.png")
    # crop_img = temp[ int(minY): int(maxY), int(minX): int(maxX)]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # blur the image slightly to remove noise.
    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # is an alternative way to blur the image
    # canny edge detection
    edged = cv2.Canny(gray, 30, 200)

    try:
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for cnt in contours:
    #     # print(cv2.contourArea(cnt))
    #     if cv2.contourArea(cnt) > 8 and cv2.contourArea(cnt) < 3000:
    #         [x, y, w, h] = cv2.boundingRect(cnt)
    #         print(cv2.contourArea(cnt))
    #         print(h)
    #         if h > 25:
    #             cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #             roi = thresh[y:y + h, x:x + w]
    #             roismall = cv2.resize(roi, (10, 10))
    #             cv2.imshow('norm', im)
    #             key = cv2.waitKey(0)
    #
    #             if key == 27:  # (escape to quit)
    #                 sys.exit()
    #             elif key in keys:
    #                 responses.append(int(chr(key)))
    #                 sample = roismall.reshape((1, 100))
    #                 samples = np.append(samples, sample, 0)
    cv2.drawContours(crop_img, cnts, -1, (0, 255, 0), 2)
    cv2.imshow("this is all contours", crop_img)
    smallestWide = [10000]
    for cnt in cnts:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if h > (maxY - minY) * 0.2 and w < (maxX-minX)*0.5 :
            # special is i and j
            x,y,w,h = checkSpecial(cnt, cnts,smallestWide, crop_img)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            roi = thresh[y:y + h, x:x + w]
            roismall = cv2.resize(roi, (10, 10))
            cv2.imshow("norm" , crop_img)
            key = cv2.waitKey(0)
            




    # cv2.drawContours(temp, [cnts[14]], -1, (0, 255, 0), 2)
    # cv2.imwrite("1111"+ ".png", crop_img)











