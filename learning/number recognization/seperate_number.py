import sys
from copy import *
import numpy as np
import cv2






if __name__ == '__main__':
    im = cv2.imread("dPaE8.png")
    # im = cv2.resize(im, None,fx = 0.4, fy = 0.4, interpolation = cv2.INTER_LINEAR)


    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)

    #################      Now finding Contours         ###################

    image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(im, contours, -1, (0, 0, 255),1)

    samples =  np.empty((0,100))
    responses = []
    keys = [i for i in range(48,58)]

    # print(contours)
    for cnt in contours:
        # print(cv2.contourArea(cnt))
        if cv2.contourArea(cnt)>8 and cv2.contourArea(cnt)<3000:
            [x,y,w,h] = cv2.boundingRect(cnt)
            print(cv2.contourArea(cnt))
            print(h)
            if  h>25:
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.imshow('norm',im)
                key = cv2.waitKey(0)

                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print("training complete")

    np.savetxt("generalsamples_RJ.data",samples)
    np.savetxt("generalresponses_RJ.data",responses)
