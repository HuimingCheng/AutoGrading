import os
import time
import platform
import shutil
import sample.grading.main


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
            try:
                currPath = os.getcwdu()
            except:
                currPath = os.path.dirname(os.path.realpath(__file__))

    allfile = os.listdir(currPath)
    print('Current Files:', allfile)
    while 1:
        newfile = os.listdir(currPath)
        if allfile != newfile and "answer.txt" in newfile and newfile-{"answer.txt"} != allfile:
            print("Changes Found")
            print('Current Files:', newfile)
            diff = set(newfile) - set(allfile)
            if moveFile and "answer.txt" in newfile:
                diff = diff - {"answer.txt"}
                for i in diff:
                    # print(os.path.join(currPath, i))
                    # print(os.path.join(currPath,"update"))
                    time.sleep(5)
                    # try:
                    sample.grading.main.grading(os.path.join(currPath, i), os.path.join(currPath, "answer.txt"))
                    shutil.move(os.path.join(currPath, i),
                                os.path.join(currPath, "update", i))
                    print("File " + str(i) + " has moved to " + str(currPath) + "/update/ ")
                    # except:
                    #     print("Fail to grade " + str(i) + ". We will try again")
            else:
                print("Please upload answer.txt file")


            # allfile = newfile
            time.sleep(Intervtime)


if __name__ == '__main__':
    main()
