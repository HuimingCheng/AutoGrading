import cv2
import numpy as np

#######   training part    ############### 

samples = np.loadtxt('generalsample.txt',np.float32)
responses = np.loadtxt('generalresponse.txt',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)

############################# testing part  #########################


im_name = input("Enter the name of the image to learn: ")

im = cv2.imread("WechatIMG452.jpeg")
im = cv2.resize(im, None,fx = 0.4, fy = 0.4, interpolation = cv2.INTER_LINEAR)
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)

new_sample = np.empty((0,100))
new_response = []

image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt)>10:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>10:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),1)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, 1)
            string = str(int((results[0][0])))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

            cv2.imshow('im', im)
            cv2.imshow('out',out)

            sample = roismall.reshape((1, 100))
            new_sample = np.append(new_sample, sample, 0)
            key = cv2.waitKey(0)
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)

            if key == 36:
                new_response.append(int((results[0][0])))
            else:
                new_response.append(key)




cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)

np.savetxt("tmpsamples.txt", new_sample)
np.savetxt("tmpresponses.txt", new_response)

tmp = open("tmpsamples.txt", "r")
sample = open("generalsample.txt", "a")

for line in tmp:
    sample.write(line)

sample.close()
tmp.close()

tmp = open("tmpresponses.txt", "r")
response = open("generalresponse.txt", "a")

for line in tmp:
    response.write(line)

response.close()
tmp.close()
