import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="nic",
  password="nic",
  database="nome-in-codice"
)

mycursor = mydb.cursor()

sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
mycursor.execute(sql)
# this will update the address inside the customers table

sql = "SELECT name, address FROM customers WHERE address = 'Canyon 123'"
mycursor.execute(sql)
myresult = mycursor.fetchone()
print(myresult)

# this will print the new entry on the db