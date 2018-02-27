import os
import time
import platform

def main():
    print("请输入地址")
    print("如果本程序已经在需要的地址下，请直接敲击回车(请使用/代替\\):",end = ' ')
    path = input("")
    if path != "":
        os.chdir(path)   # 调整目录
    else:
        if 'windows' in platform.platform().lower():  # windows 系统使用gbk编码
            path = os.getcwd()  # 返回当前目录
        else:
            path = os.getcwdu()  # 返回当前目录
    allfile = os.listdir(path)
    print('Current Files:', allfile)
    while 1:
        newfile = os.listdir(path)
        if allfile != newfile:
            print("Changes Found")
            print('Current Files:', newfile)
            time.sleep(5)
            allfile = newfile

if __name__ == '__main__':
    main()