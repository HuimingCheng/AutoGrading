from difflib import SequenceMatcher
from pytesseract import image_to_string
from PIL import *
from PIL import ImageEnhance
import cv2
import numpy as np
import sys

def similar(a, b):
    return SequenceMatcher(None, a.replace(" ","").lower(), b.replace(" ","").lower()).ratio()

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
    return image_to_string(image, config="-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz").strip()

    # return image_to_string(image).strip()

def image_proc(filename,n_pos):
    image = Image.open(filename)
    # calculate bounds of interest
    dh = n_pos[1][1] - n_pos[0][1]
    upper = n_pos[0][1] - 2 * dh
    lower = n_pos[1][1] + int(3.5 * dh)
    left = n_pos[1][0]
    right = left + 40 * (n_pos[1][0]-n_pos[0][0])
    # print(upper,lower, left, right)
    image = image.crop((left, upper, right, lower))
    
    return image

# list of names to compare
names = ["Haolun Zhang", "Haotian Wu", "Hongrui Zhang", "Huiming Cheng", "Pengqin Wu", "Ruijie Geng", "Yirong Cai", "Zhepeng Luo", "Van Darkholme", "William \"Billy\" Herrington", "Shirley Ann Jackson", "Malik Magdon-Ismail", "Herbert \"Buster\" Holzbauer"]

if __name__ == "__main__":
    #name position
    n_pos = ((712, 571), (725, 587))
    # string to decide
    filename = sys.argv[1]
    # string = recog_name(image_proc("handwritten names\\" + filename))
    string = recog_name(image_proc(filename, n_pos))
    print(string)
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
    if(m_name!=""):
        print(m_name, m_sim)
    else:
        print("Recognition Failed")


