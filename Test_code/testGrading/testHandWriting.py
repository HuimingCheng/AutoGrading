import cv2
import numpy as np
# import matplotlib.pyplot as plt
import math
# from sample.grading.Box import Box
# from sample.grading.AnswerSheet import AnswerSheet
import os
import sys
# import Tkinter
import tkinter
from importlib import reload

import mysql.connector
import sshtunnel
from mysql.connector.cursor import MySQLCursor

from pytesseract import image_to_string, image_to_boxes
from PIL import Image
from difflib import SequenceMatcher
from PIL import *
from PIL import ImageEnhance


def recogRuijie(image):
    box = image_to_string(image,
                           config="--psm 6 -c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz").strip()
    # image.show()
    # box = image_to_boxes(image).split('\n')
    print(box)



def findcoordinateOfName(path):
    image = cv2.imread(path)
    height, width  = image.shape[:2]
    crop_img = image[  0:int(height/3), 0:width]
    cv2.imwrite("temp.png", crop_img)
    image = Image.open("temp.png")
    # image.show()
    # file = open("image_to_string.txt", "w")
    box = image_to_boxes(image).split('\n')

    print(image.size)
    width , height = image.size

    coordinate = []
    for i in range(len(box)):
        flag = False
        if (box[i][0] == 'n' and box[i + 1][0] == 'a' and box[i + 2][0] == 'm' and box[i + 3][0] == 'e'):
            print("true")
            for j in range(0, 4):
                flag = True
                coordinate.append(box[i+j])
                print(box[i + j])

            if(flag):
                break
    coorE = coordinate[3].split(" ")
    print()
    return (( int(coorE[1]) , height - int(coorE[4])), ( int(coorE[3]), height - int(coorE[2])))



def similar(a, b):
    return SequenceMatcher(None, a.replace(" ", "").lower(), b.replace(" ", "").lower()).ratio()


# swap the position of first name and last name
def swap(name):
    beforespace = ""
    afterspace = ""
    space = False
    for letter in name:
        if letter == ' ' or letter == ',':
            space = True
        elif space:
            afterspace += letter
        else:
            beforespace += letter
    return afterspace + " " + beforespace


def recog_name(image):
    return image_to_string(image,
                           config="--psm 6 -c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz").strip()

    # return image_to_string(image).strip()


def image_proc(filename, n_pos):
    image = cv2.imread(filename)
    # calculate bounds of interest
    dh = n_pos[1][1] - n_pos[0][1]
    upper = n_pos[0][1] - 2 * dh
    lower = n_pos[1][1] + int(3.5 * dh)
    left = n_pos[1][0]
    right = left + 40 * (n_pos[1][0] - n_pos[0][0])
    # print(upper,lower, left, right)
    # image = image.crop((left, upper, right, lower))
    crop_img = image[  upper:lower, left:right]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    #
    # r = 100.0 / crop_img.shape[1]
    # dim = (100, int(crop_img.shape[0] * r))
    #
    # # perform the actual resizing of the image and show it
    # resized = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("temp.png", crop_img)
    image = Image.open("temp.png")
    return image


# list of names to compare
names = ["Haolun Zhang", "Haotian Wu", "Huirong Zhang", "Huiming Cheng", "Pengqin Wu", "Ruijie Geng", "Yirong Cai",
         "Zhepeng Luo", "Van Darkholme", "William \"Billy\" Herrington", "Zixiang Zhang"]

if __name__ == "__main__":
    # name position
    filename = "/Users/gengruijie/Desktop/未命名文件夹/OneDrive/学习/cs/课外/Github/AutoGrading/sample/local/temp20180309_6.png"
    n_pos = findcoordinateOfName(filename)
    # n_pos = ((712, 571), (725, 587))
    # string to decide
    # filename = sys.argv[1]
    # string = recog_name(image_proc("handwritten names\\" + filename))
    image = image_proc(filename, n_pos)
    # image.show()
    # string = recogRuijie(image)
    string = recog_name(image)
    print(string)
    m_sim = 0
    m_name = ""
    # get the name with maximum similarity
    for name in names:
        # we don't make any assumption of the order of first name and last name
        # check both possibilityies
        # we compare the higher of both with results from other strings
        sim = max(similar(string, name), similar(string, swap(name)))
        if sim > m_sim:
            m_name = name
            m_sim = sim
    if (m_name != ""):
        print(m_name, m_sim)
    else:
        print("Recognition Failed")


