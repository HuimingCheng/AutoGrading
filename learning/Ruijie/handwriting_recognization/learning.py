import cv2
import numpy as np


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
    #######   training part    ###############
    samples = np.loadtxt('generalsamples.txt',np.float32)
    responses = np.loadtxt('generalresponses.txt',np.float32)
    responses = responses.reshape((responses.size,1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    ############################# testing part  #########################

    im = cv2.imread("temp1.png")
    out = np.zeros(im.shape,np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # is an alternative way to blur the image
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)
    canny = cv2.Canny(gray, 30, 200)
    image,contours,hierarchy = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # contours = checkEnclosed(contours)
    # contours = sorted(contours, reverse=True)

    # cv2.drawContours(im, contours, -1, (0, 255, 0),2)
    # cv2.imshow("norm",  im)
    # key = cv2.waitKey(0)

    mediumHeight = findMediumHeight(contours)
    smallestWide = findSmallestWide(contours)

    smallestWide = [10000]
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if h > 0.3 * mediumHeight:
            x, y, w, h = checkSpecial(cnt, contours, smallestWide, im)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("norm" , im)
            key = cv2.waitKey(0)

            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, 1)
            string = str(chr((results[0][0])))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
            cv2.imshow('out', out)

    cv2.imshow('im',im)
    cv2.imshow('out',out)
    cv2.waitKey(0)

    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
