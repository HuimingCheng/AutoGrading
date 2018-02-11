# -*- coding: utf-8 -*-
import os
import sys

# two file is created by developers
# from main import grading
from helperFunction import readAndSaveAnswerFile
from helperFunction import saveImage, writeAnswer
import helperFunction

from flask import Flask, render_template, request
from flask import url_for, redirect
from flask_dropzone import Dropzone


# sys.setdefaultencoding("UTF8")


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
def index():
    return render_template("index.html")

'''
@app.route('/', methods=['POST', 'GET'])
def upload_answer():
    if request.method == "POST":
        f = request.files.get('photo')
        data = readAndSaveAnswerFile(f)

    return render_template("index.html")
'''

@app.route('/upload_sheet', methods=['POST', 'GET'])
def upload_sheet():

    if request.method == 'POST':
        f = request.files.get('photo')
        saveImage(f)
        # answer = grading(f.filename,"answer.txt")
        # writeAnswer(answer)
        print("this is upload_sheet")
    return render_template('index.html')

@app.route('/grading', methods=['POST', 'GET'])
def grading():
    return render_template('grading.html')

def upload_answer():
    if request.method == "POST":
        f = request.files.get('photo')
        data = readAndSaveAnswerFile(f)

    return render_template("index.html")

def upload_sheet():

    if request.method == 'POST':
        f = request.files.get('photo')
        saveImage(f)
        # answer = grading(f.filename,"answer.txt")
        # writeAnswer(answer)
    return render_template('index.html')



@app.route('/grade', methods=['POST', 'GET'])
def grade():
    check = helperFunction.checkAnswerFile()
    if check == False:
        pass

    f = open("static/result/result.txt")
    f = f.read()
    f = f.strip()

    new_answer = []
    answers = f.split('\n')
    for answer in answers:
        new_answer.append(answer.split('\t'))
    return render_template('show_result.html',items=new_answer)

if __name__ == '__main__':
    print(os.path.realpath(__file__))
    print(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=True)



















