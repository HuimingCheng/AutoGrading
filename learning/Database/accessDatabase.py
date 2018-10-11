from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)




con = mysql.connector.connect(
    user="Ruijie",
        password="gengruijie123",
        host="142.93.59.116",
        database="mysql"
                              )

if __name__ == '__main__':

    # qian mian dou shi chao wang shang de
    cur=con.cursor()
    try:
        cur.execute('CREATE TABLE Density(province TEXT, population INTEGER, land_area REAL)')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("DATABASE already exists.")
        else:
                print(err.msg)
    else:
                print("OK")


    data=[
    ('Newfoundland and Labrador', 512930, 370501.69),
    ('Prince Edward Island', 135294, 5684.39),
    ('Nova Scotia' ,908007 ,52917.43),
    ('New Brunswick' ,729498 ,71355.67),
    ('Quebec' ,7237479 ,1357743.08),
    ('Ontario', 11410046, 907655.59),
    ('Manitoba' ,1119583 ,551937.87),
    ('Saskatchewan' ,978933, 586561.35),
    ('Alberta',2974807 ,639987.12),
    ('British Columbia' ,3907738 ,926492.48),
    ('Yukon Territory', 28674 ,474706.97),
    ('Northwest Territories' ,37360 ,1141108.37),
    ('Nunavut' ,26745 ,1925460.18),
    ]
    # hkjhjkhjh=====
    #jlkjkljkljlkkl
    # for element in data:
    #     a = "INSERT INTO Density(province,population,land_area) VALUES('{:s}',{:d},{:0.2f});".format(element[0],element[1],element[2])
    #     print(a)
    #     cur.execute(a)

    # need to commit after insert data
    # con.commit()

    query = "select * from Density"
    cur.execute(query)
    data = cur.fetchall()
    print(data)



























#cursor=cnx.cursor()
#DB_NAME="Student_grade"

##try:
    ##cursor.execute("USE {}".format(DB_NAME))
##except mysql.connector.Error as err:
    ##print("Database {} does not exists.".format(DB_NAME))
    ##if err.errno == errorcode.ER_BAD_DB_ERROR:
        ##create_database(cursor)
        ##print("Database {} created successfully.".format(DB_NAME))
        ##cnx.database = DB_NAME
    ##else:
        ##print(err)
        ##exit(1)

##cursor.execute("DROP TABLE GRADE")   

#cursor.execute("INSERT INTO GRADE VALUES('Wang Jiahang',100)")
#cursor.execute("INSERT INTO GRADE VALUES('Bill Li',100)")
#cursor.execute("INSERT INTO GRADE VALUES('Wu Tong',68)")
#cursor.execute("INSERT INTO GRADE VALUES('ssb',77)")
#cursor.execute("INSERT INTO GRADE VALUES('Su Laoshi',99)")
#cursor.execute("INSERT INTO GRADE VALUES('xhl',88)")
#cnx.commit()
#cursor.execute("SELECT name, grade FROM GRADE WHERE grade>65")
#for (name,grade) in cursor:
    #print("{} gets {} in the test".format(name,grade))
#cursor.close()