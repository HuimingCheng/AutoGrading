# import processData
import mysql.connector
from mysql.connector import errorcode

import os
import sys
# two file is created by developers
# from main import grading
# from helperFunction import readAndSaveAnswerFile
# from sample.web.helperFunction import saveImage, writeAnswer
import flask
from flask import Flask, render_template, request
from flask import url_for, redirect
# from flask_dropzone import Dropzone
import threading
import time
from multiprocessing import Process, Pool
# for user login
# from flask_wtf import FlaskForm
# from wtforms import StringField, BooleanField, PasswordField
# from wtforms.validators import DataRequired
import mysql.connector
# connect database
cnx = mysql.connector.connect(
    user="Ruijie",
    password="gengruijie123",
    host="142.93.59.116",
    database="mysql"
)

# create flask application
app = Flask(__name__)

@app.route('/main', methods=['POST', 'GET'])
def getData():
    cursor = cnx.cursor()
    query = "show databases;"
    cursor.execute(query)

    data = cursor.fetchall()
    string = str(data)
    # print(cursor.fetchall())
    return string

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True )
