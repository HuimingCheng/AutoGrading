# -*- coding: utf-8 -*-
import cv2
import numpy as np
# import matplotlib.pyplot as plt
import math
# from sample.grading.Box import Box
# from sample.grading.AnswerSheet import AnswerSheet
# import os
# import sys
# # import Tkinter
# import tkinter
# from importlib import reload
#
# import mysql.connector
# import sshtunnel
# from mysql.connector.cursor import MySQLCursor
#
# from pytesseract import image_to_string, image_to_boxes
# from PIL import Image


image = cv2.imread("/Users/gengruijie/Desktop/未命名文件夹/OneDrive/学习/cs/课外/Github/AutoGrading/sample/web/static/upload/unclassify/answerSheet2.png")
print(image.shape[:2])

imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
print(thresh.shape[:2])

(_, cnts, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
