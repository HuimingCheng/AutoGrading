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

    def up_load(self, file, table_name):

        pass




    def add_student(self, info):

        table_name = "Student"
        query = "INSERT INTO " + table_name + """ (FirstName,LastName,RIN,Email,ProofNum,ProofInfo) 

												VALUE (%s,%s,%s,%s,%s,%s)"""

        self.cur.execute(query, info)

        self.conn.commit()

    # name is student name

    # info is all of the hw content of this student


    def delete(self, table_name):

        query = "DELETE from " + table_name

        self.cur.execute(query)

        self.conn.commit()


    def search_student(self, student_name):

        query = "SELECT PersonID from Student WHERE FirstName = %s"

        self.cur.execute(query, [student_name])

        id_ = self.cur.fetchall()

        if (len(id_) != 1):

            rin = input("Please entre the RIN of the student")

            query = "SELECT PersonID from Student WHERE RIN = %s"

            self.cur.execute(query, [rin])

            id_ = self.fetchone()

            useless = self.cur.fetchall()

            return id_[0][0]



        else:

            return id_[0][0]

    def read_code(self, name, code_name):

        id_ = self.search_student("Ruijie")

        table_name = "student" + str(id_) + "_" + code_name

        query = "SELECT * from " + table_name

        self.cur.execute(query)

        code = self.cur.fetchall()

        print(code)





    def show_student(self):

        query = "SELECT * from Student"

        self.cur.execute(query)

        students = self.cur.fetchall()

        for i in students:
            print(i[1])
