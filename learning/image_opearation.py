# import the necessary packages
import cv2

# load the image and show it
# the picture is in the same folder with python file.
image = cv2.imread("image/basic-original.png")

# show the image in original window
# cv2.imshow("original", image)
# Display the window infinitely until any keypress
# cv2.waitKey(0)
# cv2.waitKey(10000)      # wait 10 second 


# print the image that x rows(tall), y columns(wide), and z channels (the RGB components)
# print(image.shape)


# we want to resize the picture. resize the wide from y to 100 pix 
ratio = 100.0 / image.shape[1]
# new dimension for image
dim = (100, int(image.shape[0] * ratio))
# perform the actual resizing of the image and show it
# interpolation = cv2.INTER_AREA this is the algorithm we used. Do worry now
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("resized", resized)
cv2.waitKey(5000)


# flip this upside down:
(h, w) = image.shape[:2]
center = (w / 2, h / 2)
 
# rotate the image by 180 degrees
# center: tuple of two int/float  180: rotation angle   1.0: ratio of original size.
# matrix that can be used for rotating (and scaling) the image
matrix = cv2.getRotationMatrix2D(center, 180, 1.0)
# to rotate the image.
rotated = cv2.warpAffine(image, matrix, (w, h))
cv2.imshow("rotated", rotated)
cv2.waitKey(5000)



# crop the image using array slices -- it's a NumPy array
# from starty to endy(height) and from startx to endx(wide)
cropped = image[0:170, 0:540]
cv2.imshow("cropped", cropped)
cv2.waitKey(5000)























