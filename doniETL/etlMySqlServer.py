from os import getenv
import pymssql

server = "donigroup.cczhghwibti9.us-west-2.rds.amazonaws.com:1433"
user = "immadimtiaz"
password = "Giki1990????"

conn = pymssql.connect(server, user, password, "DoniEnterprises")

cursor = conn.cursor()