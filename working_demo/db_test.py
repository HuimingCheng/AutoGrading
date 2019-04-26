import mysql.connector
from mysql.connector import errorcode
from sample.database import  database
import json


if  __name__ == '__main__':

    db = database.Database("Ruijie", "12345678", "142.93.59.116", "Student_grade")
    print(db.show_database())
    print(db.describe_table("Users.User_info"))
    db.insert_data("Users.User_info",[["username","hubert51"],["password","hubert"],["email","ruijiegengatrpi.edu"],["is_professor",False]])
    # db.get_cursor().execute("INSERT INTO Users.User_info (username ,password ,email ,is_professor ) VALUES('Jiahang','JiahangWang','wangj39@rpi.edu',False);")
    # db.get_cnx().commit()
    print(db.queryData("Users.User_info"))

    # DB_name = "Student_grade"
    # print(db.show_database())
    #
    # # db.create_tables("machine_learning", [ ["id", "int"], ["result", "int"], ["img", "JSON"] ], "id")
    # # print(db.show_tables(DB_name))
    #
    # list1 = {255, 3, 0, 0, 0, 255} # Note that the 3rd element is a tuple (3, 4)
    # json_data = json.dumps(list1)
    #
    # print(type(list1))
    # print(json_data)
    #
    # print(db.describe_table("machine_learning"))
    # # db.insert_data("machine_learning", [ ["id", 1],["result", 1], ["img", list1]] )
    # db.queryData("machine_learning")

