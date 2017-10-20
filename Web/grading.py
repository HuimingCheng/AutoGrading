class Grading(object):
	"""docstring for Grading"""
	def __init__(self, answer,empty_answersheet=None,student_answersheet=None):
		# answer is a file, contains the choice of question
		# answer_ is a string, contains the choice of question.
		# empty_AS is a image, contains the empty_answer sheet.
		# student_AS_list is list of a image, the list contains the answer sheet of student.
		self.answer_ = self.process_answer(answer)
		self.student_AS_list = student_answersheet
		self.thresh_image = None

	def process_answer(self,answer):
		f = open(answer)
		content = f.read()
		return content

	def threshold_image(self,image):
		# convert image to grayscale
	    gray = cv2.cvtColor(self.student_AS_list, cv2.COLOR_BGR2GRAY)
	    # blur the image slightly to remove noise.
	    gray = cv2.bilateralFilter(gray, 11, 17, 17)
	    # gray = cv2.GaussianBlur(gray, (5, 5), 0) is an alternative way to blur the image
	    # canny edge detection
	    edged = cv2.Canny(gray, 30, 200)
	    # two threshold method.
	    # The first one is normal threshold method
	    # The second one is use Gaussian method which has better effect.
	    # ret,thresh1 = cv2.threshold(gray,150,150,cv2.THRESH_BINARY)
	    self.thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)



	def compare(self):


	    # find contours in the edged image, keep only the largest ones, and initialize
	    # our screen contour
	    # findContours takes three parameter:
	    # First parameter: the image we want to find counter. Need to copy since this method will
	    # destroy the image.
	    # Second parameter: cv2.RETR_TREE tells OpenCV to compute the hierarchy (relationship)
	    # between contours
	    # Third parameter: compress the contours to save space using cv2.CV_CHAIN_APPROX_SIMPLE
	    try:
	        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    except:
	        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	    # (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    # the number of returned parameter is different depending on the version of openCV
	    # for 2.x it is (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    # for 3.x it is (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    # sort the counter. The reference is the countourArea. And we only get largest 10
	    # countour.
	    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1000]

	    # a new list to store all the rectangle counter
	    cnts_rect = []
	    # initialize the screenCnt.
	    screenCnt = None

	    # loop over our contours
	    for c in cnts:
	        # approximate the contour
	        peri = cv2.arcLength(c, True)
	        # This function gives the number of vertices of the figure
	        # For example, approx returns 4 if the shape is rectangle and 5 if the shape is pentagon
	        # k is constant, it can be changing from 0.005 to 0.1
	        # k = 0.005
	        k = 0.1
	        approx = cv2.approxPolyDP(c, k * peri, True)
	        # if our approximated contour has four points, then
	        # we can assume that we have found our screen
	        if len(approx) == 4 and cv2.contourArea(c) > 15000:
	            screenCnt = approx
	            cnts_rect.append(approx)
	        # print "this is coutour area ", cv2.contourArea(c)

	    # the print is for test
	    # print screenCnt[0][0]

	    # to draw the contours in the original image.
	    # print len(cnts_rect)
	    cv2.drawContours(image, cnts_rect, -1, (0, 255, 0), 3)

	    # to find height and length of the rectangle
	    height = cnts_rect[0][2][0][1] - cnts_rect[0][0][0][1]
	    length = cnts_rect[0][2][0][0] - cnts_rect[0][0][0][0]

	    # x_axis is a list, store all the x_axis data of one contour
	    # y_axis is a list, store all the y_axis data of same contour
	    # cnts[0] is a list of point, which is one rectangle

	    centre_list = find_centre(cnts_rect)
	    # print len(centre_list)

	    # print "this length of centre_list is ", len(centre_list)

	    centre_list_col = sorted(centre_list, key=lambda point: point[1])
	    # answer_list is a list. It contains x elements, x is rows of the answer sheet. It is also list
	    # every row_list contains also list which are centre points of rectangle.
	    answer_list = find_missing_rectangle(centre_list, centre_list_col, length // 2, height // 2)

	    # ============================================================
	    # for test print point in centre list
	    # ============================================================
	    # print len(answer_list)
	    # for list1 in answer_list:
	    #     print("the length of list1 is ", len(list1))
	    #     for element in list1:
	    #         print element

	    # print len(answer_list)
	    # ============================================================
	    # end test
	    # ============================================================

	    number_of_choice = 4
	    answer = find_answer2(answer_list,number_of_choice,thresh1,pixel=40,number_of_question=40)

	    print answer

