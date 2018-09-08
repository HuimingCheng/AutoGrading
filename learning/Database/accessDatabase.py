import mysql.connector
from mysql.connector import errorcode
print("This is the first update")
print("Hello World")
conn = mysql.connector.connect(
    user="Ruijie",
    password="gengruijie123",
    host="142.93.59.116",
    database="mysql"
)