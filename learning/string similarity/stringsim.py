from difflib import SequenceMatcher
from pytesseract import image_to_string
from PIL import *
from PIL import ImageEnhance
import cv2
import numpy as np
import sys

def similar(a, b):
	return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# swap the position of first name and last name
def swap(name):
	beforespace = ""
	afterspace = ""
	space = False
	for letter in name:
		if letter == ' ' or letter == ',':
			space = True
		elif space:
			afterspace += letter
		else:
			beforespace += letter
	return afterspace + " " + beforespace

def recog_name(image):
    return image_to_string(image)

def image_proc(filename):
	image = Image.open(filename)
	# image = image.filter(ImageFilter.BLUR)
	image.show()
	return image

# list of names to compare
names = ["Haolun Zhang", "Haotian Wu", "Hongrui Zhang", "Huiming Cheng", "Pengqin Wu", "Ruijie Geng", "Yirong Cai", "Zhepeng Luo"]

if __name__ == "__main__":
	# string to decide
	filename = sys.argv[1]
	string = recog_name(image_proc("handwritten names\\" + filename))
	m_sim = 0
	m_name = ""
	# get the name with maximum similarity
	for name in names:
		# we don't make any assumption of the order of first name and last name
		# check both possibilityies
		# we compare the higher of both with results from other strings
		sim = max(similar(string, name), similar(string, swap(name)))
		if sim > m_sim:
			m_name = name
			m_sim = sim
	print(m_name)
		