import mysql.connector

from mysql.connector import errorcode


class Database_mysql:
    def __init__(self, user, password, host, database_name):

        self.user = user

        self.password = password

        self.host = host

        self.database = database_name

        # self.conn

        # self.cur



        try:

            self.conn = mysql.connector.connect(

                user=user,

                password=password,

                host=host,

                database=database_name)

            self.cur = self.conn.cursor()



        except mysql.connector.Error as e:

            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:

                print("Invalid username or Password")

            elif e.errno == errorcode.ER_BAD_DB_ERROR:

                print("DataBase N/A")

            else:

                print(e)

