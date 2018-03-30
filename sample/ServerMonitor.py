import os
import time
import platform
import shutil


def main(AskForPath=False, Intervtime=15, moveFile=True):
    if AskForPath:
        print("Enter the path: ")
        print("If the program is already in the requested directory, press 'Enter' directly. (Use / to replace \\):",
              end=' ')
        currPath = input("").strip()
        if currPath != "":
            if "/" in currPath:
                Path = currPath.split("/")
            elif "\\" in currPath:
                Path = currPath.split("\\")
            currPath = Path[0]
            for i in (1, Path):
                currPath = os.path.join(currPath, Path[i])
            os.chdir(currPath)  # change the path
    else:
        if 'windows' in platform.platform().lower():
            currPath = os.getcwd()
        else:
            currPath = os.getcwdu()
    allfile = os.listdir(currPath)
    print('Current Files:', allfile)
    while 1:
        newfile = os.listdir(currPath)
        if allfile != newfile:
            print("Changes Found")
            print('Current Files:', newfile)
            diff = set()
            diff = set(newfile) - set(allfile)
            if moveFile:
                for i in diff:
                    # print(os.path.join(currPath, i))
                    # print(os.path.join(currPath,"update"))
                    time.sleep(0.5)
                    shutil.move(os.path.join(currPath, i),
                                os.path.join(currPath, "update", i))
                    print("File " + str(i) + " has moved to " + str(currPath) + "/update/ ")
            allfile = newfile
            time.sleep(Intervtime)


if __name__ == '__main__':
    main()
