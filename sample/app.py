# -*- coding: utf-8 -*-
import os
import sys

# two file is created by developers
from main import grading
from flaskHelper import readAndSaveAnswerFile
from flaskHelper import saveImage, writeAnswer



from flask import Flask, render_template, request
from flask import url_for, redirect
from flask_dropzone import Dropzone

reload(sys)
sys.setdefaultencoding("UTF8")

app = Flask(__name__)
dropzone = Dropzone(app)

app.config.update(
    UPLOADED_PATH=os.getcwd() + '/static/upload',
    DROPZONE_ALLOWED_FILE_TYPE='default',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_INPUT_NAME='photo',
    DROPZONE_MAX_FILES=30
)

# sys.setdefaultencoding('Cp1252')
@app.route('/', methods=['POST', 'GET'])
def upload_answer():
    if request.method == "POST":
        f = request.files.get('photo')
        data = readAndSaveAnswerFile(f)

    return render_template("index.html")

@app.route('/upload_sheet', methods=['POST', 'GET'])
def upload_sheet():

    if request.method == 'POST':
        f = request.files.get('photo')
        saveImage(f)
        answer = grading(f.filename,"answer.txt")
        writeAnswer(answer)
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    f = open("static/result/result.txt")
    f = f.read()
    f = f.strip()

    new_answer = []
    answers = f.split('\n')
    for answer in answers:
        new_answer.append(answer.split('\t'))
    return render_template('show_result.html',items=new_answer)

if __name__ == '__main__':
    app.run(debug=True)


















