"""
Some useful note:
ASCII:
27: "ESC"
32: "blank"
13: enter
127: delete
up: 63232
down: 63233
left: 63234
right: 63235
"""

import sys
from copy import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sample import database


def create_key_image(key, row):
    # Create a black image
    size = row//2
    img = np.zeros((size, size, 3), np.uint8)
    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = ( int(0.22*row), int(0.22*row) )
    fontScale = 2
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(img, str(key),
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    return img

    # Display the image
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

def create_image_with_response(im):
    row, col = im.shape[0], im.shape[1]
    new_image = np.tile( (255,255,255), (row, row//2, 1,))
    new_image = np.concatenate((im,new_image), axis=1 )
    return new_image

def add_answer(image, key_image, sample_image):
    row1, col1 = image.shape[0], image.shape[1]
    row2, col2 = key_image.shape[0], key_image.shape[1]

    x_offset = col1-col2
    y_offset = row2
    image[0:0 + key_image.shape[0], x_offset:x_offset + key_image.shape[1]] = key_image
    image[y_offset:y_offset + key_image.shape[0], x_offset:x_offset + key_image.shape[1]] = sample_image


def store_data(samples, responses, myDB):
    db = database.database.Database("Ruijie", "gengruijie123", "142.93.59.116", myDB)
    # db.drop_table("machine_learning")
    # db.create_tables("machine_learning", [ ["id", "int NOT NULL AUTO_INCREMENT"], ["result", "int"], ["img", "JSON"] ], "id")
    for i in range(len(samples)):
        db.insert_data("machine_learning" ,[ [ "result", responses[i] ], ["img", list(samples[i]) ] ])


# def redo(contours, count, ):



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: seperate_number.py  input_iamge  output_sample  output_response\n")
        print("where input_iamge is an image file contains number you want to learn. \n"
              "output_data is the .data file to store the sample you collect. \n"
              "output_response is answer corresponding to the sample " )
        sys.exit()
    else:
        img_name = sys.argv[1]
        sample_output = sys.argv[2]
        response_output = sys.argv[3]

    db_name = "Student_grade"

    im = cv2.imread(img_name)
    scale1 = 700 / im.shape[0]
    # scale2 = 450 / img2.shape[0]
    # print(scale1)
    # print(img1.shape)

    im = cv2.resize(im, (int(im.shape[1]*scale1), int(im.shape[0]*scale1)) )
    im_alies = im
    row, col = im.shape[0], im.shape[1]
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)
    paper_area = im.shape[0] * im.shape[1]

    # create a image to show the answer
    answer_image = create_image_with_response(im)
    cv2.imwrite("test.png", answer_image)
    im = cv2.imread("test.png")

    # Now finding Contours
    image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))

    samples =  np.empty((0,100))
    responses = []

    area = []
    keys = [i for i in range(48,58)]
    for cnt in contours:
        temp = cv2.contourArea(cnt)
        if temp >= paper_area / 4:
            continue
        area.append(cv2.contourArea(cnt))

    area = np.array(area)
    n, binEdges, patches = plt.hist(area, 10, normed=1, color="red", alpha=1)
    # bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
    count = 0

    while count < len(contours):
        cnt = contours[count]

    # for cnt in contours:
        # print(cv2.contourArea(cnt))
        # if cv2.contourArea(cnt)>8 and cv2.contourArea(cnt)<3000:

        [x,y,w,h] = cv2.boundingRect(cnt)
        if h<=10:
            count+=1
        # print(h)
            # print(cv2.contourArea(cnt))
            # print(h)
        if  h>10:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
            roi = thresh[y:y+h,x:x+w]
            roi2 = im_alies[y:y+h,x:x+w]
            # the size of roismall image is 10*10
            roismall = cv2.resize(roi,(10,10))
            roibig = cv2.resize(roi, (row//2,row//2))
            roibig = cv2.cvtColor(roibig, cv2.COLOR_GRAY2RGB)
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)
            # print(key)

            # blank space input. jump to next input
            if key == 32:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1
                continue
            if key == 27:  # (escape to quit)
                break

            # redo
            if key == 114:
                print("redo.")
                #[x, y, w, h] = cv2.boundingRect(contours[count])
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 255), 2)  # color(white) = retrive
                responses.pop(-1)
                count -= 1
                [x, y, w, h] = cv2.boundingRect(contours[count])
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                key = cv2.waitKey(0)
                print(key)
                key_image = create_key_image(int(chr(key)), row)
                add_answer(im, key_image, roibig)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                responses.append(int(chr(key)))
                count += 1
                continue


            # up arrow
            elif key == 63232:
                print("this is up")
                continue

            key_image = create_key_image( int(chr(key)), row)
            add_answer(im, key_image,roibig )
            # print(key)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)


            if key in keys:
                count += 1
                responses.append(int(chr(key)))
                # print(roismall.shape)

                # sample from 10*10 to 1*100
                sample = roismall.reshape((1,100))
                # print(samples)
                # print(sample.shape)
                # print(responses)
                samples = np.append(samples,sample,0)
                # cv2.waitKey(0)

    store_data(samples, responses, db_name)


    # sys.exit(1)
    # responses = np.array(responses,np.float32)
    # responses = responses.reshape((responses.size,1))
    # print("training complete")
    #
    # np.savetxt(sample_output,samples)
    # np.savetxt(response_output,responses)


