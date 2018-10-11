import os
import sys


# two file is created by developers
# from main import grading
# from helperFunction import readAndSaveAnswerFile
from sample.web.helperFunction import saveImage, writeAnswer

import flask
from flask import Flask, render_template, request
from flask import url_for, redirect
from flask_dropzone import Dropzone
import threading
import time
from multiprocessing import Process, Pool

# for user login
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
import mysql.connector

# ==================================================
# test for connect pythonanywhere
import mysql.connector
import sshtunnel
from mysql.connector.cursor import MySQLCursor


from flask_mail import Mail, Message

def connectDatabase(username, password):
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0

    with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='Gengruijie', ssh_password='Grj12345',
        remote_bind_address=('Gengruijie.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        connection = mysql.connector.connect(
            user='Gengruijie', password='GRJ12345',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='Gengruijie$AutoGrading',
        )
        # Do stuff
        query = "SELECT password, level, score from main where name = \"" + username + "\""
        # print(query)
        # cur = connection.cursor(buffered=True)
        cursor = MySQLCursor(connection)
        cursor.execute(query)
        data = cursor.fetchall()
        # print(data, password)
        if data[0][0] != password:
            return (False,1,1)
        return (True, data)

# end test.
# ==================================================

# global variable:
loginUsers = []

# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class MyThread(threading.Thread):
    def __init__(self):
        self.run()


    def run(self) -> object:
        print("{} started!".format(self.getName()))              # "Thread-x started!"
        time.sleep(1)                                      # Pretend to work for a second
        print("{} finished!".format(self.getName()))             # "Thread-x finished!"


app = Flask(__name__)


mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'haotian666666@gmail.com'
app.config['MAIL_PASSWORD'] = 'Uwha090909'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





conn = mysql.connector.connect(
    user="root",
    password="gengruijie",
    host="127.0.0.1",
    database="Lemma"
)

# to config upload file
app.wsgi_app = app.wsgi_app
app.config['SECRET_KEY'] = "Hubert"
UPLOAD_FOLDER = "static/upload/unclassify"

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

@app.route("register", method=['POST','GET'])
def register():
   msg = Message('Hello', sender = 'haotian666666@gmail.com', recipients = ['651938023@qq.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

@app.route('/login', methods=['POST', 'GET'])
def login():

    form = LoginForm()
    if request.method == "POST":
        # print(11231231)
        user = request.form.get("username")
        password = request.form.get("password")
        data = connectDatabase(user, password)
        if (  data[0] == False ):
            return render_template('index.html')
        global loginUsers
        loginUsers.append((user, data))
        # print(loginUsers)
        return render_template('indexUser.html')
    return render_template('login.html', title="Sign In", form=form)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    global loginUsers
    # print("I am run here")
    loginUsers= []
    return render_template('index.html')


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
        # print("this is upload_sheet")
    return render_template('index.html')

@app.route('/grading', methods=['POST', 'GET'])
def grading():
    return render_template('grading.html')

def upload_answer():
    if request.method == "POST":
        f = request.files.get('photo')
        # data = readAndSaveAnswerFile(f)

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
    # check = he.checkAnswerFile()
    # if check == False:
    #     pass

    f = open("static/result/result.txt")
    f = f.read()
    f = f.strip()

    new_answer = []
    answers = f.split('\n')
    for answer in answers:
        new_answer.append(answer.split('\t'))
    return render_template('show_result.html',items=new_answer)

@app.route('/auto_upload', methods=['post'])
def myupload():
    myFile = request.files['file']
    myFile.save(os.path.join(UPLOAD_FOLDER, myFile.filename))
    return "ok"


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')



@app.route('/Scores', methods=['GET'])
def Scores():
    global loginUsers
    username = loginUsers[0][0]

    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0

    with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='Gengruijie', ssh_password='Grj12345',
        remote_bind_address=('Gengruijie.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        connection = mysql.connector.connect(
            user='Gengruijie', password='GRJ12345',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='Gengruijie$AutoGrading',
        )
        # Do stuff
        query = "SELECT level, score from main where name = \"" + username + "\""
        # print(query)
        # cur = connection.cursor(buffered=True)
        cursor = MySQLCursor(connection)
        cursor.execute(query)
        data1 = cursor.fetchall()

    # print(username)

    if data1[0][0] == "student":
        return render_template('Scores.html', name=username,score =data1[0][1] )
    else :
        sshtunnel.SSH_TIMEOUT = 5.0
        sshtunnel.TUNNEL_TIMEOUT = 5.0

        with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username='Gengruijie', ssh_password='Grj12345',
                remote_bind_address=('Gengruijie.mysql.pythonanywhere-services.com', 3306)
        ) as tunnel:
            connection = mysql.connector.connect(
                user='Gengruijie', password='GRJ12345',
                host='127.0.0.1', port=tunnel.local_bind_port,
                database='Gengruijie$AutoGrading',
            )
            # Do stuff
            query = "SELECT name, score from main"
            # print(query)
            # cur = connection.cursor(buffered=True)
            cursor = MySQLCursor(connection)
            cursor.execute(query)
            data = cursor.fetchall()
        # print(data)
        result = []
        for element in data :
            if element[1] != "":
                if element[0] == "Turner":
                    continue
                result.append((element[0],element[1]))
        return render_template('ScoresProfessor.html', name=username,items =result )






def flaskRun():
    # print(os.path.realpath(__file__))
    # print(os.path.dirname(os.path.realpath(__file__)))

    app.run(host='0.0.0.0', debug=True )








if __name__ == '__main__':
    # threading.Thread(target=moniter()).start()
    # threading.Thread(target=run()).start()
    p = Pool(2)
    p.apply_async(flaskRun())
    print("Waiting for all subprocess done...")
