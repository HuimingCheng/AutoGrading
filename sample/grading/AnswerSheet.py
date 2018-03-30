from sample.grading.Box import Box
import cv2
import sys
import numpy as np

class AnswerSheet(object):
    def __init__(self,myCentre=(0.0,0.0),myAnswerArea = 0.0):
        self.centre = myCentre
        self.answerArea = myAnswerArea
        self.answerBox = []
        self.answer = []
        self.height = 0.0
        self.length = 0.0
        self.difference = 0
        self.numberOfChoice = 0
        self.centreList = []
        self.xlittleDIfference = 0
        self.xlargeDIfference = 0
        self.ydifference = 0
        self.thresholdImage = np.array(0)
        self.totalLine = 0



    def setCentre(self,myCentre):
        self.centre = myCentre

    def setCnswerBox(self,myArea):
        self.answerArea = myArea

    def setThreshold(self, thres):
        self.thresholdImage = thres

    def getArea(self):
        return self.answerArea

    def getCentre(self):
        return self.centre

    def getAnswerBox(self):
        return self.answerBox

    def getAnswer(self):
        return self.answer


    def findAnswerBox(self,allBox):
        delta = self.answerArea * 0.125
        for box in allBox:
            if (self.answerArea-delta < box.getArea() < self.answerArea+delta ):
                self.answerBox.append(box)

    def drawAnswerBox(self,res):
        for box in self.answerBox:
            cv2.drawContours(res, box.getContour(), -1, (0, 255, 0), 2)
            # print(box.getContour())
            cv2.circle(res,box.getCentre(),20,(0,0,0))
        # cv2.circle(image,(x_max,y_max),20,(0,0,0))
        # cv2.imshow("test", image)
        # cv2.waitKey(20000)

        # cv2.imwrite("this is res1.png", res)

    # find the length and height of one answer box.
    def findLengthAndHeight(self):
        contour = self.answerBox[0].getContour()
        x_axis = []
        y_axis = []
        for point in contour:
            x_axis.append(point[0][0])
            y_axis.append(point[0][1])
        x_axis.sort()
        y_axis.sort()
        self.length = x_axis[-1] - x_axis[0]
        self.height = y_axis[-1] - y_axis[0]


    def findBoxArea(self,distanceFromCentre):
        areaList = []
        for i in range(20):
            flag = False
            for j in range(len(areaList)):
                if (0.9 * areaList[j][1] < distanceFromCentre[i][2] < 1.1 * areaList[j][1]):
                    sum = areaList[j][1] * areaList[j][0]
                    areaList[j][1] = (sum + distanceFromCentre[i][2]) / (areaList[j][0] + 1)
                    areaList[j][0] += 1
                    flag = True
            if (flag == False):
                areaList.append([1, distanceFromCentre[i][2]])

            if len(areaList) == 0:
                areaList.append([1, distanceFromCentre[i][2]])

        areaList.sort(reverse=True)
        self.answerArea = areaList[0][1]



    def findDistanceBetweenAnswerBoxAndNumberOfChoice(self):
        centre_list = []
        for box in self.answerBox:
            centre = box.getCentre()
            centre_list.append(centre)
        centre_list.sort(key=lambda x: x[1])
        self.centreList = centre_list


        # this is a double list, inner list contains the centre of box in one line
        # our list contains different line.
        list_of_one_line = []
        y_base = centre_list[0][1]
        one_line = []

        for i in range(len(centre_list)):
            y_upper = y_base + 0.6 * self.height
            if (centre_list[i][1] < y_upper):
                one_line.append(centre_list[i])

            else:
                y_base = centre_list[i][1]
                list_of_one_line.append(one_line)
                one_line = [centre_list[i]]
                continue
        list_of_one_line.append(one_line)

        differences = []
        numbers = []
        for oneLine in list_of_one_line:
            numbers.append(len(oneLine))

        number = max(numbers)
        if number%4 == 0:
            self.numberOfChoice = 4
        elif number%5 == 0:
           self.numberOfChoice = 5
        else:
            print("Can not determine the number of choice, please give the number and try again!")
            sys.exit(1)

        for oneLine in list_of_one_line:
            oneLine.sort()
            if len(oneLine) == number:
                self.xlittleDIfference = oneLine[1][0] - oneLine[0][0]
                choice = self.numberOfChoice
                self.xlargeDIfference = oneLine[choice][0] - oneLine[choice-1][0]
                break

        self.ydifference = list_of_one_line[1][0][1] - list_of_one_line[0][0][1]
        centre_list.sort(key=lambda x:x[0])

        self.totalLine = len(list_of_one_line)
        print()
        '''
            difference = []
            oneLine.sort()
            for i in range(len(oneLine)-1):
                difference.append(oneLine[i+1][0] - oneLine[i][0])
            differences.append(difference)
        

        numberOfQuestions = []
        for difference in differences:
            sort_difference = sorted(difference)
            self.difference = sort_difference[0]

            # numberOfQuestion = []
            count = 0
            for number in difference:
                numberOfQuestion = []
                if number < self.difference + 0.5*self.length :
                    count += 1
                else:
                    # numberOfQuestion.append(count)
                    numberOfQuestions.append(count)
                    count = 0

        self.numberOfQuestion = max(numberOfQuestions) + 1
        self.littleDIfference = sort_difference[0]

        i = 0
        for line in differences:
            for value in line:
                if value < self.littleDIfference+0.5*self.length:
                    i+=1
                # elif (i==)





        # one_line_centre_list


        print()
        '''

    def relocate(self, x_base, y_base):
        centre_list = self.centreList
        i = 0
        while(x_base+0.5*self.length > centre_list[i][0] ):
            if (centre_list[i][0]-0.5*self.length < x_base < centre_list[i][0]+0.5*self.length and
                centre_list[i][1]-0.5 * self.height < y_base < centre_list[i][1] + 0.5 * self.height):
                return centre_list[i]
            i+=1
        # if we can not relocate the position, we will locate the second choice and go back
        # to locate the first choice
        x_base += self.xlittleDIfference
        while(x_base+0.5*self.length > centre_list[i][0] ):
            if (centre_list[i][0]-0.5*self.length < x_base < centre_list[i][0]+0.5*self.length and
                centre_list[i][1]-0.5 * self.height < y_base < centre_list[i][1] + 0.5 * self.height):
                return centre_list[i][0]-self.xlittleDIfference,centre_list[i][1]
            i+=1

        #===============================================================================
        # if we run to this line, we need to improve this function to fit more situation
        #===============================================================================
        return x_base-self.xlittleDIfference,y_base



    def grade(self,question):
        list_of_px = []
        for box in question:
            px = 0
            x_start, x_end = int(box[0]-0.2*self.length) ,  int(box[0]+0.2*self.length)
            y_start, y_end = int(box[1]-0.2*self.height) ,  int(box[1]+0.2*self.height)

            for x in range(int(x_start), int(x_end)):
                for y in range(int(y_start), int(y_end)):
                    # x, y for high qualit
                    # y,x for low quality
                    px += self.thresholdImage[y, x]
            list_of_px.append(px)

        if list_of_px.index(min(list_of_px)) == 0:
            return 'A'
        if list_of_px.index(min(list_of_px)) == 1:
            return 'B'
        if list_of_px.index(min(list_of_px)) == 2:
            return 'C'
        if list_of_px.index(min(list_of_px)) == 3:
            return 'D'



    def locateQuestion(self):
        question = []
        centre_list = self.centreList
        centre_list.sort(key=lambda x:x[0])
        i = 0
        y_base = centre_list[i][1]
        x_base = centre_list[0][0]
        while(centre_list[i][0] < centre_list[0][0]+0.5*self.length):
            if y_base > centre_list[i][1]:
                y_base = centre_list[i][1]
            i+=1

        x_base_original, y_base_original = self.relocate(x_base,y_base)
        i = 0
        answer = []


        while(i<40):
            # if i != 0:
            x_base, y_base = self.relocate(x_base,y_base)

            question = [
                        (x_base, y_base),
                        (x_base + 1*self.xlittleDIfference, y_base),
                        (x_base + 2*self.xlittleDIfference, y_base),
                        (x_base + 3*self.xlittleDIfference, y_base),
                       ]
            answer.append(self.grade(question))
            y_base+=self.ydifference
            i+=1
            if (i%self.totalLine == 0):
                x_base = x_base_original + (self.numberOfChoice-1)*self.xlittleDIfference + self.xlargeDIfference
                y_base = y_base_original
                x_base,y_base = self.relocate(x_base,y_base)
                # cv2.circle(self.thresholdImage, (x_base, y_base), 20, (0, 0, 0))
                # cv2.imwrite("this is thre.png", self.thresholdImage)
                x_base_original, y_base_original = x_base, y_base

        self.answer = answer
        print()






    def someUsefulFunction(self):

        cv2.circle(self.thresholdImage,(  100, 100),20,(0,0,0))
        cv2.imwrite("this is thre.png", self.thresholdImage)
        pass















