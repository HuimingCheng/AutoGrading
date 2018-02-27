from pytesseract import image_to_string, image_to_boxes
from PIL import Image
import sys


if __name__ == '__main__':

	image = Image.open('answerSheet_with_name.png')
	file = open("image_to_string.txt", "w")
	box = image_to_boxes(image).split('\n')

	for i in range(len(box)):
		if (box[i][0] == 'n' and box[i+1][0] == 'a' and box[i+2][0] == 'm' and box[i+3][0] == 'e'):
			print("true")
			for j in range(0,4):
				print(box[i+j])



	file.write(image_to_boxes(image))
	file.close()
