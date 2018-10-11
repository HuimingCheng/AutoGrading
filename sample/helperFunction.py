from pytesseract import image_to_string, image_to_boxes
from PIL import Image
import sys
import os
import time
import platform



# the type file is <FileStorage: u'answer.txt' ('text/plain')>
# the output is a tuple contains (year, semester, exam name and answer)
def readAndSaveAnswerFile(file):
    # here we have problem that the f.filename is unicode char. If there is Chinese inside filename
    # we need to encode this unicode into ascii and ignore or replace Chinese word
    #filename = filename.encode('ascii','ignore')
        
    content = file.readline().strip()
    date = content.split('/')
    
    content = file.readline().strip()
    folder = os.getcwd()
    f = open(folder + '/static/upload/answer.txt','w')

    f.write(content)
    f.close()
    return (date[0],date[1],date[2], content)


def saveImage(file):
    # f = request.files.get('photo')
    filename = file.filename
    # here we have problem that the f.filename is unicode char. If there is Chinese inside filename
    # we need to encode this unicode into ascii and ignore or replace Chinese word
    # filename = filename.encode('ascii','ignore')
    folder = os.getcwd()
    file.save(folder+"/static/upload/unclassify/"+filename)

def writeAnswer(answer):
    f = open("static/result/result.txt", 'w')
    for x in answer:
        for y in x:
            f.write(str(y))
            f.write('\t')
        f.write('\n')
    f.close()



def locateNameBox():
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

def checkAnswerFile():
    if 'windows' in platform.platform().lower():  # windows 系统使用gbk编码
        path = os.getcwd()  # 返回当前目录
    else:
        try:
            path = os.getcwdu()  # 返回当前目录
        except:
            path = os.path.dirname(os.path.realpath(__file__))  # 返回当前目录
    path += "/static/upload/unclassify"
    allfile = os.listdir(path)
    if "answer.txt" in allfile:
        return True
    else:
        return False
    # print('Current Files:', allfile)



def FileMoniter():
    print("请输入地址")
    print("如果本程序已经在需要的地址下，请直接敲击回车(请使用/代替\\):",end = ' ')
    path = input("")
    if path != "":
        os.chdir(path)   # 调整目录
    else:
        if 'windows' in platform.platform().lower():  # windows 系统使用gbk编码
            path = os.getcwd()  # 返回当前目录
        else:
            try:
                path = os.getcwdu()  # 返回当前目录
            except:
                path = os.path.dirname(os.path.realpath(__file__))  # 返回当前目录
    path += "/static/upload/unclassify"
    allfile = os.listdir(path)
    print('Current Files:', allfile)
    while 1:
        newfile = os.listdir(path)
        if allfile != newfile:
            print("Changes Found")
            print('Current Files:', newfile)
            time.sleep(5)
            allfile = newfile


