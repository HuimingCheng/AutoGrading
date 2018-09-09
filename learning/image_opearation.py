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

x_axis = sorted(x_axis)
y_axis = sorted(y_axis)
x_centre = int((x_axis[0] + x_axis[-1]) / 2)
y_centre = int((y_axis[0] + y_axis[-1]) / 2)
# print "The smallest x coordinate is",x_axis[0]
# print "The smallest y coordinate is",y_axis[0]
# print "The biggest x coordinate is",x_axis[-1]
# print "The biggest y coordinate is",y_axis[-1]
# print "The centre of this rectangle is (%d,%d)" %(x_centre, y_centre)
if (check_include(centre_list, x_centre, y_centre)):
    centre_list.append((x_centre, y_centre))
# print "The centre of this rectangle is (%d,%d)" %(x_centre, y_centre)
return centre_list

# crop the image using array slices -- it's a NumPy array
# from starty to endy(height) and from startx to endx(wide)
cropped = image[0:170, 0:540]
cv2.imshow("cropped", cropped)
cv2.waitKey(5000)























