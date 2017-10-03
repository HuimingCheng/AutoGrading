import cv2
import numpy as np 

image = cv2.imread("image/gameboy.jpg")

# convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur the image slightly to remove noise.
gray = cv2.bilateralFilter(gray, 11, 17, 17) 
#gray = cv2.GaussianBlur(gray, (5, 5), 0) is an alternative way to blur the image
# canny edge detection
edged = cv2.Canny(gray, 30, 200)

# find contours in the edged image, keep only the largest ones, and initialize 
# our screen contour
# findContours takes three parameter:
# First parameter: the image we want to find counter. Need to copy since this method will
# destroy the image.
# Second parameter: cv2.RETR_TREE tells OpenCV to compute the hierarchy (relationship) 
# between contours
# Third parameter: compress the contours to save space using cv2.CV_CHAIN_APPROX_SIMPLE
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# sort the counter. The reference is the countourArea. And we only get largest 10 
# countour.
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
# initialize the screenCnt.
screenCnt = None

# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	#This function gives the number of vertices of the figure
	#For example, approx returns 4 if the shape is rectangle and 5 if the shape is pentagon
	approx = cv2.approxPolyDP(c, 0.02 * peri, True) 
	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

# the print is for test		
print screenCnt[0][0]

# to draw the contours in the original image.
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Game Boy Screen", image)
# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
cv2.waitKey(100000)















