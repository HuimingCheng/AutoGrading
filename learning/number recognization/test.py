from pytesseract import image_to_string
from PIL import Image
import cv2
import numpy


if __name__ == '__main__':
    position = ((712, 571), (725, 587))
    dh = position[1][1] - position[0][1]
    upper = position[0][1] - 2 * dh
    lower = position[1][1] + int(3.5 * dh)
    left = position[1][0]

    print(upper,lower, left)

    img = cv2.imread('answerSheet_with_name.png')
    #image = Image.open('answerSheet_with_name.png')

    img = img[upper:lower, left:img[1].size]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)
    cv2.imshow("hello", img)


    #################      Now finding Contours         ###################

    img,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255),1)

    im = Image.fromarray(img, 'RGB')

    file = open("image_to_string.txt", "w")
    # box = image_to_string(image).split('\n')
    file.write(image_to_string(im))
    #file.write(image_to_string(image))
    file.close()

