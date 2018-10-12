import mysql.connector
from mysql.connector import errorcode
from sample.database import  database
import json

db = database.Database("Ruijie", "gengruijie123", "142.93.59.116", "Student_grade")

DB_name = "Student_grade"
print(db.show_database())

# db.create_tables("machine_learning", [ ["id", "int"], ["result", "int"], ["img", "JSON"] ], "id")
# print(db.show_tables(DB_name))

list1 = {255, 3, 0, 0, 0, 255} # Note that the 3rd element is a tuple (3, 4)
json_data = json.dumps(list1)

print(type(list1))
print(json_data)

print(db.describe_table("machine_learning"))
# db.insert_data("machine_learning", [ ["id", 1],["result", 1], ["img", list1]] )
db.queryData("machine_learning")
