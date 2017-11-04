import os

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
    filename = filename.encode('ascii','ignore')
    folder = os.getcwd()

    file.save(folder+"/static/upload/"+filename)

def writeAnswer(answer):
    f = open("static/result/result.txt", 'w')
    for x in answer:
        for y in x:
            f.write(str(y))
            f.write('\t')
        f.write('\n')
    f.close()