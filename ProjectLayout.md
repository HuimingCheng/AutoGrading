#  Project layout(TBD)

This description file mainly focus on the grading part, the "Model", of the project.

## 1 Picture upload
- From cell phone   
- From pc(.pdf, .jpg, ...)


Related files : *.html; app.py; 

## 2 Find center of answer sheet


Related files : AnswerSheet.py;  

## 3 Find all boxes/contours in answer sheet


Related files : Box.py; AnswerSheet.py

## 4 Find center of each box


Related files : Box.py; AnswerSheet.py

##  5 Find area of boxes near center


Related files : Box.py; AnswerSheet.py

## 6 Find area of answer box zone


Related files : AnswerSheet.py

## 7 Find most of the answer boxes from contour list


Related files : AnswerSheet.py

## 8 Find length, height of each answer box


Related files : AnswerSheet.py

## 9 Find number of multiple choice options AND distance between answer boxes(same question && different questions)


Related files : AnswerSheet.py
   
## 10 Find remaining answer boxes that are not in the list(if any)


Related files : AnswerSheet.py

## 11 Find center of each list of indexed boxes (1 list of boxes corresponds to 1 question)

## 12 Convert image input into 2-D list
 data = list<Questions>;
 Questions = list<Boxes>;
 
## 13 Grading, find which boxes are marked


## 14 Output results
* in plain text
* (also return a modified input with √ and × ?)
