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
import sys


def checkSpecial(cnt, contours,smallestWide, crop_image):
    [x, y, w, h] = cv2.boundingRect(cnt)
    if w < smallestWide[0]:
        smallestWide[0] = w

    for contour in contours:
        [x1, y1, w1, h1] = cv2.boundingRect(contour)
        if x - 0.1* w <x1 < x +0.5 * w and \
            0.1*w < w1 < 1.3 * w and \
            cv2.contourArea(contour) < 0.3 * cv2.contourArea(cnt) and \
            h1 > 0.05*h and \
            w < 2*smallestWide[0] and \
            abs(y1-y) < h:
            cv2.drawContours(crop_image, [contour], -1, (0, 255, 0), 2)

            return x, y1,abs(x1-x+w1), y-y1+h
    return x, y, w, h


def findMediumHeight(cnts):
    heights = []
    for cnt in cnts:
        y_axis = []
        for point in cnt:
            y_axis.append(point[0][1])
        y_axis.sort()
        heights.append(y_axis[-1] - y_axis[0])

    return heights[len(heights)//2]


def findSmallestWide(cnts):
    wides = []
    for cnt in cnts:
        x_axis = []
        for point in cnt:
            x_axis.append(point[0][0])
        x_axis.sort()
        wides.append(x_axis[-1] - x_axis[0])
    wides.sort()
    return wides[0]


def checkEnclosed(cnts):
    i = 0
    j = 0
    while (i != len(cnts)):
        j = 0
        x1,y1,w1,h1 =  cv2.boundingRect(cnts[i])
        while (j != len(cnts)):
            temp = []
            x2, y2, w2, h2 = cv2.boundingRect(cnts[j])
            if x1 < x2 and x1+w1 > x2+w2 and y1 < y2 and y1+h1 > y2+h2:
                k = 0
                while (k!=len(cnts)):
                    if k == j:
                        k += 1
                        continue
                    temp.append(cnts[k])
                    k += 1
                cnts = temp
                i -= 1
                j -= 1
            j += 1
        i += 1
    return cnts




if __name__ == '__main__':
    crop_img = cv2.imread("learnLetter.png")
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # is an alternative way to blur the image
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)
    edged = cv2.Canny(gray, 30, 200)
    try:
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # to remove some small contours which is enclosed in other big contours
    cnts = checkEnclosed(cnts)

    print("After function", len(cnts))
    mediumHeight = findMediumHeight(cnts)
    smallestWide = findSmallestWide(cnts)

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
    # cv2.drawContours(crop_img, cnts, -1, (0, 255, 0), 2)
    # cv2.imwrite("temp.png", crop_img)

    # for cnt in cnts :
    #     cv2.drawContours(crop_img, [cnt], -1, (0, 255, 0), 2)
    #     cv2.imshow("norm", crop_img)
    #     key = cv2.waitKey(0)

    samples =  np.empty((0,100))
    responses = []

    smallestWide = [10000]

    for cnt in cnts:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if h > 0.3*mediumHeight :
            # special is i and j
            x,y,w,h = checkSpecial(cnt, cnts,smallestWide, crop_img)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = thresh[y:y + h, x:x + w]
            roismall = cv2.resize(roi, (10, 10))
            cv2.imshow("norm" , crop_img)
            key = cv2.waitKey(0)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(key)

            if key == 27:  # (escape to quit)
                sys.exit()
            elif key == 32: # this is invalid training sample determined by user.
                continue
            responses.append(chr(key))
            sample = roismall.reshape((1, 100))
            samples = np.append(samples, sample, 0)

    # responses = np.array(responses, np.float32)
    # responses = responses.reshape((responses.size, 1))
    print("training complete")

    np.savetxt("generalsamples.data", samples)
    np.savetxt("generalresponses.data", responses)

            # cv2.drawContours(temp, [cnts[14]], -1, (0, 255, 0), 2)
    # cv2.imwrite("1111"+ ".png", crop_img)











