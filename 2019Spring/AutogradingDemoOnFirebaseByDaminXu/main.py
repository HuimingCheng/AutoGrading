# -*- coding: utf-8 -*-
import cv2
import numpy as np
# import matplotlib.pyplot as plt
import math

try:
    # for pycharm projet
    from sample.database_grading_demo.Box import Box
    from sample.database_grading_demo.AnswerSheet import AnswerSheet
    from sample.database_grading_demo.helperFunction import getNameFromDatabse, updateScore
except:

    # for non-pycharm user
    from Box import Box
    from AnswerSheet import AnswerSheet
    from helperFunction import getNameFromDatabse, updateScore

import os
import time
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
import handWriting as HW
import pytesseract

from dbmanager import firebaseManager
# begin of handwriting
#===========================================================================
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


def image_proc(image, n_pos):
    # calculate bounds of interest
    dh = n_pos[1][1] - n_pos[0][1]
    upper = n_pos[0][1] - 2 * dh
    lower = n_pos[1][1] + int(3.5 * dh)
    left = n_pos[1][0]
    right = left + 40 * (n_pos[1][0] - n_pos[0][0])
    crop_img = image[  upper:lower, left:right]
    cv2.imwrite("temp.png", crop_img)
    time.sleep(10)
    image = Image.open("temp.png")
    return image
# end of handwriting
#============================================================


def gradeAnswer(correct_answer,answer):
    temp = ""
    result = []
    for letter in correct_answer:
        if letter.isalpha()==True :
            temp += letter
    correct_answer = temp
    if len(correct_answer) != len(answer):
        return None
    for i in range(len(answer)):
        temp = []
        if answer[i] != correct_answer[i]:
            temp.append(i+1)
            temp.append(answer[i])
            temp.append(correct_answer[i])
            result.append(temp)
    return result

def printTime(timeBegin):
    timeEnd = time.time()
    # print("Time consuming is {:}".format(timeEnd-timeBegin))
    return  timeEnd


''' 
@parameter: image1: the path of the input image which need to be graded
'''


def grading(img_file, answer_file,recog = False):
    # sshtunnel.SSH_TIMEOUT = 300.0
    # sshtunnel.TUNNEL_TIMEOUT = 300.0
    # with sshtunnel.SSHTunnelForwarder(
    #         ('ssh.pythonanywhere.com'),
    #         ssh_username='Gengruijie', ssh_password='Grj12345',
    #         remote_bind_address=('Gengruijie.mysql.pythonanywhere-services.com', 3306)
    # ) as tunnel:
    #     connection = mysql.connector.connect(
    #         user='Gengruijie', password='GRJ12345',
    #         host='127.0.0.1', port=tunnel.local_bind_port,
    #         database='Gengruijie$AutoGrading',
    #     )
    #     query = "SELECT name from main"
    #     cursor = MySQLCursor(connection)
    #     cursor.execute(query)
    #     names = cursor.fetchall()
    #
    # print("Begin to grade answer sheet")
    # temp = []
    # for name in names:
    #     temp.append(name[0])
    # names = temp

    # myPath = os.path.dirname(os.path.realpath(__file__))
    # myPath = os.path.split(myPath)[0] +  "/web/static/upload/unclassify"
    # myPathImage = image1
    # myPathAnswer = myPath  + "/answer.txt"

    image = cv2.imread(img_file)
    answerFile = open(answer_file)

    timeBegin = time.time()

    # print("Begin to process the image")
    # the paper is almost 3000*2000
    centerOfPaper = (image.shape[0]/2, image.shape[1]/2)
    # now the centre is (x,y)
    centerOfPaper = (centerOfPaper[1],centerOfPaper[0])
    answerSheet = AnswerSheet(centerOfPaper)

    res = image
    # convert image to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # blur the image slightly to remove noise.
    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # is an alternative way to blur the image
    # canny edge detection
    edged = cv2.Canny(gray, 30, 200)

    # two threshold method.
    # The first one is normal threshold method
    # The second one is use Gaussian method which has better effect.
    ret,thresh1 = cv2.threshold(gray,150,150,cv2.THRESH_BINARY)
    thresh1=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # print("Finish to process the image")
    # timeBegin = printTime(timeBegin)

    answerSheet.setThreshold(thresh1)

    # print("Begin to find the counters of the answer sheet")
    try:
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:200]
    # print("Finish to find the counters of the answer sheet")
    timeBegin = printTime(timeBegin)

    # print("Begin to find counter around the centre of answer sheet")
    listOfContourObject = []
    for c in cnts:
        listOfContourObject.append(Box(c))

    distanceFromCentre = []
    for box in listOfContourObject:
        boxCentre = box.getCentre()

        distance = math.sqrt((boxCentre[0]-centerOfPaper[0])**2 + (boxCentre[1]-centerOfPaper[1])**2 )
        distanceFromCentre.append((distance,box,box.getArea()))

    distanceFromCentre.sort()
    # print("Finish to find counter around the centre of answer sheet")
    timeBegin = printTime(timeBegin)

    # print("To get the area of the answer box.")
    # to get the area of the answer box.
    answerSheet.findBoxArea(distanceFromCentre)
    # print("Finish to get the area of the answer box.")
    timeBegin = printTime(timeBegin)

    # print("Begin to determine the box which is answer box")
    # to determine the box which is answer box
    answerSheet.findAnswerBox(listOfContourObject)
    # print("Finish to determine the box which is answer box")
    timeBegin = printTime(timeBegin)

    # print("Begin to find length and height and difference between box")
    # find length and height of the box
    answerSheet.findLengthAndHeight()
    answerSheet.findDistanceBetweenAnswerBoxAndNumberOfChoice()
    # print("Finish to find length and height and difference between box")
    timeBegin = printTime(timeBegin)

    # print("Begin to locate the question")
    answerSheet.locateQuestion()
    # print("Finish to locate the question")
    timeBegin = printTime(timeBegin)

    # print("Begin to get the answer from sheet and file, and grade.")
    # to get the answer from sheet and file, and grade.
    answerFile = answerFile.read()
    correctAnswer = answerFile.split("\n")
    studentAnswer = answerSheet.getAnswer()
    result = gradeAnswer(correctAnswer,studentAnswer)
    score = str(len(studentAnswer)-len(result)) +"/" +  str(len(studentAnswer))
    # print("Finish to get the answer from sheet and file, and grade.")
    timeBegin = printTime(timeBegin)

    if recog == False:
        return len(studentAnswer)-len(result)


    # =======================================================================================
    # next part is handwriting recognition
    # this is still developing part
    # =======================================================================================
    """
    print("Begin to recongnize the handwriting")
    filename = myPathImage
    n_pos = findcoordinateOfName(filename)
    image = image_proc(image, n_pos)
    # string = recogRuijie(image)
    string = recog_name(image)
    print("End to recongnize the handwriting")
    timeBegin = printTime(timeBegin)

    print("Begin to compare the name with database")
    os.remove("temp.png")
    m_sim = 0
    m_name = ""
    searchName = ""
    names = getNameFromDatabse()
    for name in names:
        # get the name with maximum similarity
        # we don't make any assumption of the order of first name and last name
        # check both possibilityies
        # we compare the higher of both with results from other strings
        sim = max(similar(string, name), similar(string, swap(name)))
        if sim > m_sim:
            m_name = name
            searchName = name
            m_sim = sim
    if (m_name != ""):
        updateScore(score,searchName)
    else:
        print("Recognition Failed")
    print("Finish to compare the name with database")
    printTime(timeBegin)
    
    """
# list of names to compare
names = ["Haolun Zhang", "Haotian Wu", "Huirong Zhang", "Huiming Cheng", "Pengqin Wu", "Ruijie Geng", "Yirong Cai",
         "Zhepeng Luo", "Van Darkholme", "William \"Billy\" Herrington", "Zixiang Zhang", "Damin Xu"]

def getName(fileName):
    n_pos = HW.findcoordinateOfName(fileName)
    image = HW.image_proc(fileName, n_pos)
    string = HW.recog_name(image)
    m_sim = 0
    m_name = ""
    # get the name with maximum similarity
    for name in names:
        # we don't make any assumption of the order of first name and last name
        # check both possibilityies
        # we compare the higher of both with results from other strings
        sim = max(HW.similar(string, name), HW.similar(string, HW.swap(name)))
        if sim > m_sim:
            m_name = name
            m_sim = sim
    if (m_name != ""):
        return m_name
    else:
        return False

def generateResult(answerFile, imageList):
    result = dict()
    for imageFile in imageList:
        name = getName(imageFile)
        if(name == False):
            print("ERROR Cannot analyse the name of image {}\n".format(imageFile))
            continue
        result[name] = grading(imageFile, answerFile)
        print("Done with {}.\n".format(imageFile))
    return result

def getFileNames(file_dir): 
    L=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if  os.path.splitext(file)[1] == '.png':
                L.append(os.path.join(root,file))
    print(L)
    return L

def calcGrade(score, total):
    percent = float(score)/total*100
    grade = ""
    if(percent >= 93):
        grade = "A"
    elif(percent >= 80):
        grade = "B"
    elif(percent >= 70):
        grade = "C"
    elif(percent >= 60):
        grade = "D"
    else:
        grade = "F"
    return percent, grade
    


if __name__ == '__main__':
    """
    For DEMO
    """
    # answer sheet and answer
    answerFile = "test_file/answer.txt"
    dirc = "test_file/"
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    
    # get list of image names

    imageList = getFileNames(dirc)
    # the result is the integer
    print("Start Analysing...\n")
    result = generateResult(answerFile, imageList)
    for key, value in result.items():
        percent, grade = calcGrade(value, 40)
        print("{}: {} {:.2f} {}\n".format(key, value, percent, grade))



    config = {
              "apiKey": "AIzaSyCVL9P3X4pDhr0xXwgikOm7eabBr-u0U40",
              "authDomain": "autograding-47061.firebaseapp.com",
              "databaseURL": "https://autograding-47061.firebaseio.com",
              "storageBucket": "autograding-47061.appspot.com",
              "serviceAccount": "privateKey.json"
            }
    firebase = firebaseManager(config)
    firebase.newGrads("DemoTest", result)

    '''
    db = database.Database("Ruijie", "12345678", "142.93.59.116", "Student_grade")
    print(db.describe_table("GRADE"))
    db.insert_data(["hubert", result], table="GRADE")

    print(db.queryData("GRADE"))
    '''