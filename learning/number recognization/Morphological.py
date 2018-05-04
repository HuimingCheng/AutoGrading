import cv2
import numpy as np

if __name__ == "__main__":
    # testing erode
    img = cv2.imread("Illustration.png")
    img = cv2.resize(img, None, fx=0.60, fy=0.60, interpolation=cv2.INTER_LINEAR)
    cv2.imshow("", img)
    cv2.waitKey()
    kernel = np.ones((25, 25), dtype=int)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imshow("", erosion)
    cv2.waitKey()

    # testing dilation
    img = cv2.imread("Illustration.png")
    img = cv2.resize(img, None, fx=0.60, fy=0.60, interpolation=cv2.INTER_LINEAR)
    cv2.imshow("", img)
    cv2.waitKey()
    kernel = np.ones((2, 2))
    erosion = cv2.dilate(img, kernel, iterations=1)
    cv2.imshow("", erosion)
    cv2.waitKey()
    print("done")
