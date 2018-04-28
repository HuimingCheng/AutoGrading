from sample.AutoGrading import AutoGrading


autoGrading = AutoGrading()
imageAddress = "temp1.png"
score = autoGrading.grading(imageAddress,recogFlag=False)
print("\nThe score of this answer sheet is {:}".format(score) )