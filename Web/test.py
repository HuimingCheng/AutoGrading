import cv2
import sys

name = "upload/IB_answer_sheet7.png"
image = cv2.imread(name)

f = open("answer.txt")
answer = f.read()

temp = "%s" %"1" 
print(temp)

sys.exit()
print answer