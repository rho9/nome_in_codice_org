import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="nic",
  password="nic",
  database="nome-in-codice"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))") # once created cannot be overwritten with this
# shows: mysql.connector.errors.ProgrammingError: 1050 (42S01): Table 'customers' already exists

# mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))") 
# statement "INT AUTO_INCREMENT PRIMARY KEY" which will insert a unique number for each record. Starting at 1, and increased by one for each record.

# If the table already exists, use the ALTER TABLE keyword:
# mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)

# output:
# ('customers',)