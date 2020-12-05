import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="nic",
  password="nic",
#   database="nome-in-codice"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE mydatabase") # fails because of some kind of permission

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

# output:
# ('information_schema',)
# ('nome-in-codice',)