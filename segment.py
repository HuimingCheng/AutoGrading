from __future__ import division
import sys
from copy import *
import numpy as np
import cv2
from PIL import Image
from pytesseract import image_to_string
from math import *

'''
This code uses a naive method to achieve segmentation. 
It simply sets a threshold for the ratio between width and height
When a detected contour has larger ratio, it determines that 
the contour contains several characters and the number of characters
is dependent on the the ratio between width and height.
This code works for some pariticular input image, but for a great part
of the input, it hardly works.
'''

# image processing
im = cv2.imread("HZ2.jpg")
im = cv2.resize(im, None,fx = 0.4, fy = 0.4, interpolation = cv2.INTER_LINEAR)
height, width = im.shape[:2]
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)

# looking for contours
image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
print(hierarchy)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

# find out possible segmentation 
lines = []
for cnt in contours:
	# valid contour size
    if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<10000:
        [x,y,w,h] = cv2.boundingRect(cnt)
        r = ceil(w / h / 0.9)
        assert(w!=0)
        wc = w / r
        # exceed threshold
        # several segmentation in a contour
        while r > 0:
            lines.append(int(x))
            print(x)
            x += wc
            r = r - 1

# cut coutours 
lines.sort()
prev = lines[0]
name = ""

for cut in lines[1:]:
    print(prev,cut)
    # extract the segmented picture
    seg = im[:, prev:cut]
    # convert to Image
    seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
    seg_pil = Image.fromarray(seg)
    seg_pil.show()
    prev = cut
    # accumulate recognized characters
    # cannot run on windows
    # name = name + image_to_string(seg_pil, config="-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -psm 6").strip()

# recognize the last one segment
cut = width
seg = im[:, prev:cut]
seg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
seg_pil = Image.fromarray(seg)
seg_pil.show()
# cannot run on windows
# name = name + image_to_string(seg_pil, config="-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -psm 6").strip()
print(name)
# seg_pil.show()

