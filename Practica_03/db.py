import mysql.connector


password = "m0th3l3td3lg4"
user_db = "root"

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