import mysql.connector
from mysql.connector import errorcode
print("  ")
conn = mysql.connector.connect(
    user="Ruijie",
    password="gengruijie123",
    host="142.93.59.116",
    database="mysql"
)