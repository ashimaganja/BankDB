from mysql.connector.types import MySQLConvertibleType
import mysql.connector

conn = mysql.connector.connect(host="localhost", password="password", user="root",
                               database="Fraudserver")

if conn.is_connected():
    print("Connection established ..")

mycursor = conn.cursor()

