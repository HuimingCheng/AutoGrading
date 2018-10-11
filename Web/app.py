# -*- coding: uk_UA.UTF-8 -*-
import os
#from main import grading


from flask import Flask, render_template, request
from flask import url_for, redirect
from flask_dropzone import Dropzone
from flask_mail import Mail, Message


app = Flask(__name__)
dropzone = Dropzone(app)


mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'haotian666666@gmail.com'
app.config['MAIL_PASSWORD'] = 'Uwha090909'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



app.config.update(
    UPLOADED_PATH=os.getcwd() + '/upload',
    DROPZONE_ALLOWED_FILE_TYPE='default',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_INPUT_NAME='photo',
    DROPZONE_MAX_FILES=30
)

# sys.setdefaultencoding('Cp1252')
@app.route('/', methods=['POST', 'GET'])
def function():
    if request.method == "POST":
        print(1)

        pass
    return render_template("index.html")

@app.route('/upload_answer', methods=['POST', 'GET'])
def upload_answer():
    # for x in range(2):
    if request.method == 'POST':
        return "asd"
        # print 1
        f = request.files.get('photo')
        # filename = f.filename
        #     # here we have problem that the f.filename is unicode char. If there is Chinese inside filename
        #     # we need to encode this unicode into ascii and ignore or replace Chinese word
        # filename = filename.encode('ascii','ignore')
        f.save(os.path.join(app.config['UPLOADED_PATH'], 'answer.txt'))
        # check = 1
        return redirect(url_for('upload_sheet'))
    # try:
    #     grading("image","answer")
    # if request.method == "GET" and check ==1:
        # return "hello world"
    # return render_template('index.html')


@app.route('/upload_sheet', methods=['POST', 'GET'])
def upload_sheet():

    # for x in range(2):
    if request.method == 'POST':
        f = request.files.get('photo')
        print(1)
        # return render_template('index2.html')
        filename = f.filename
            # here we have problem that the f.filename is unicode char. If there is Chinese inside filename
            # we need to encode this unicode into ascii and ignore or replace Chinese word
        filename = filename.encode('ascii','ignore')
        f.save(os.path.join(app.config['UPLOADED_PATH'], filename))
    # try:
        #answer = grading(filename,"answer.txt")
        f = open("result.txt", 'w')
        for x in answer:
            for y in x:
                f.write(str(y))
                f.write('\t')
            f.write('\n')
        # print f
        f.close()
    return render_template('index2.html')#,items = answer)


    # print answer

    # except :
        # print "ERROR"
@app.route('/result', methods=['POST', 'GET'])
def result():
    print("Open result")
    f = open("result.txt")
    f = f.read()
    f = f.strip()

    new_answer = []
    answers = f.split('\n')
    for answer in answers:
        new_answer.append(answer.split('\t'))

    # print answer
    return render_template('show_result.html',items=new_answer)#,items = answer)

if __name__ == '__main__':
    app.run(debug=True)
