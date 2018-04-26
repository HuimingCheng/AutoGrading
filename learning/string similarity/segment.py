from __future__ import division
import sys
from copy import *
import numpy as np
import cv2
from PIL import Image
from pytesseract import image_to_string
from math import *


im = cv2.imread("HZ2.jpg")
im = cv2.resize(im, None,fx = 0.4, fy = 0.4, interpolation = cv2.INTER_LINEAR)
height, width = im.shape[:2]
# print(im)

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)

#################      Now finding Contours         ###################

image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(im, contours, -1, (0, 0, 255),1)
print(hierarchy)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

# cont = np.ones((height, width))
# cv2.fillPoly(cont, contours, 0)
# cv2.imshow('norm',cont)
# key = cv2.waitKey(0)
lines = []
for cnt in contours:
    if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<10000:
        [x,y,w,h] = cv2.boundingRect(cnt)
        r = ceil(w / h / 0.9)
        assert(w!=0)
        wc = w / r
        # print(w,h,r,wc)
        while r > 0:
            lines.append(int(x))
            print(x)
            x += wc
            r = r - 1
        # cont = np.ones((height, width))
        # cv2.fillPoly(cont, cnt, 0)
        # cv2.imshow('norm',cont)
        # key = cv2.waitKey(0)
        
lines.sort()
prev = lines[0]
name = ""
for cut in lines[1:]:
    print(prev,cut)
    seg = im[:, prev:cut]
    seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
    seg_pil = Image.fromarray(seg)
    seg_pil.show()
    prev = cut
    # name = name + image_to_string(seg_pil, config="-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -psm 6").strip()

cut = width
seg = im[:, prev:cut]
seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
seg_pil = Image.fromarray(seg)
seg_pil.show()
# name = name + image_to_string(seg_pil, config="-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -psm 6").strip()
print(name)
# seg_pil.show()

