from Box import Box
import cv2

class AnswerSheet(object):
    def __init__(self,myCentre=(0.0,0.0),myAnswerArea = 0.0):
        self.centre = myCentre
        self.answerArea = myAnswerArea
        self.answerBox = []
        self.height = 0.0
        self.length = 0.0


    def setCentre(self,myCentre):
        self.centre = myCentre

    def setCnswerBox(self,myArea):
        self.answerArea = myArea

    def getArea(self):
        return self.answerArea

    def getCentre(self):
        return self.centre

    def findAnswerBox(self,allBox):
        delta = self.answerArea * 0.125
        for box in allBox:
            if (self.answerArea-delta < box.getArea() < self.answerArea+delta ):
                self.answerBox.append(box)

    def drawAnswerBox(self,res):
        for box in self.answerBox:
            cv2.drawContours(res, box.getContour(), -1, (0, 255, 0), 2)
        cv2.imwrite("this is res1.png", res)

    def findLengthAndHeight(self):
        print(self.answerBox[0].getContour()[0])
        self.height = self.answerBox[0].getContour()[2][0][1] - self.answerBox[0].getContour()[0][0][1]
        self.length = self.answerBox[0].getContour()[2][0][0] - self.answerBox[0].getContour()[0][0][0]
        print(self.height,self.length)

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