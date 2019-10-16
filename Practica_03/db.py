import mysql.connector
from getpass import getpass

print("Introduzca usuario:")
user_db = str(input())
password = getpass("Introduzca su contraseña:")

mydb = mysql.connector.connect(
    host="localhost",
    user=user_db,
    passwd=password
)

mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS Central")
mydb.cmd_reset_connection

mydb2 = mysql.connector.connect(
    host="localhost",
    user=user_db,
    passwd=password,
    database="Central"
)

mycursor = mydb2.cursor()


mycursor.execute("CREATE TABLE IF NOT EXISTS Sumas (resultado INTEGER, ip VARCHAR(25), hora TIME)")