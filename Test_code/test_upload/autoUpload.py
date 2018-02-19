# coding=utf-8
import requests


import os
import time
import platform
import atexit

# global variable for exit function

global FILENUMBER

# print the number of files uplaod in this time, and give a reminder for user that the
# the file will be deleted after Monday before exit the script.

'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    print(timeStruct.tm_year)
    return time.strftime('%Y-%m-%d',timeStruct)


def get_FileCreateTime(filePath):
    # filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def upload(fileName):
    url = "http://129.161.41.95:5000/auto_upload"
    file = open(fileName, 'rb')
    files = {'file': file}
    response = requests.post(url, files=files)
    file.close()
    global FILENUMBER
    FILENUMBER += 1
    # print(response.status_code)
    # print(response.request.body)

def move(fileName,path):
    file = open(fileName, 'rb')
    print("in auto upload, the type is ",type(file))
    os.rename(path+'/'+fileName, path+"/UpLoaded/" + fileName)
    file.close()
    # os.remove(fileName)





def upLoadAndMoveFile(allfile,newfill,path):
    for new in newfill:
        newFileFlag = True
        for all in allfile:
            if new == all:
                newFileFlag = False
                break
        if newFileFlag:
            upload(new)
            move(new,path)




def moniter():
    # print("请输入地址")
    # print("如果本程序已经在需要的地址下，请直接敲击回车(请使用/代替\\):",end = ' ')
    # path = input("")
    # if path != "":
    #     os.chdir(path)   # 调整目录
    # else:

    # to get path of the file.
    if 'windows' in platform.platform().lower():  # windows 系统使用gbk编码
        path = os.getcwd()  # 返回当前目录
    else:
        path = os.getcwd()  # 返回当前目录




    # to check whether the complete upload folder is created or not.
    if os.path.isdir('Uploaded'):
        createTime = get_FileCreateTime(path+"/Uploaded")
        # currentTime = time.str
        print("2018-03-09" > createTime)
    else:
        os.mkdir('Uploaded')



    allfile = os.listdir(path)
    print('Current Files:', allfile)
    while 1:
        newfile = os.listdir(path)
        if allfile != newfile:
            print("Changes Found")
            upLoadAndMoveFile(allfile,newfile,path)
            # print('Current Files:', newfile)
            time.sleep(15)
            # allfile = newfile


def exit():
    print("You have upload {:d}".format(FILENUMBER))
    print("Please reminder the file will be deleted when you open this file next time.")

def autoUpload():
    FILENUMBER = 0
    atexit.register(exit)
    moniter()


if __name__ == '__main__':
    FILENUMBER = 0
    atexit.register(exit)
    moniter()


