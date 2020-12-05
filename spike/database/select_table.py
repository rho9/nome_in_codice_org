import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="nic",
  password="nic",
  database="nome-in-codice"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

# output:
# ('John', 'Highway 21', 1)
# ('John', 'Highway 21', 2)
# ('Peter', 'Lowstreet 4', 3)
# ('Amy', 'Apple st 652', 4)
# ('Hannah', 'Mountain 21', 5)
# ('Michael', 'Valley 345', 6)
# ('Sandy', 'Ocean blvd 2', 7)
# ('Betty', 'Green Grass 1', 8)
# ('Richard', 'Sky st 331', 9)
# ('Susan', 'One way 98', 10)
# ('Vicky', 'Yellow Garden 2', 11)
# ('Ben', 'Park Lane 38', 12)
# ('William', 'Central st 954', 13)
# ('Chuck', 'Main Road 989', 14)
# ('Viola', 'Sideway 1633', 15)

mycursor.execute("SELECT name, address FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x) 

# output:
# ('John', 'Highway 21')
# ('John', 'Highway 21')
# ('Peter', 'Lowstreet 4')
# ('Amy', 'Apple st 652')
# ('Hannah', 'Mountain 21')
# ('Michael', 'Valley 345')
# ('Sandy', 'Ocean blvd 2')
# ('Betty', 'Green Grass 1')
# ('Richard', 'Sky st 331')
# ('Susan', 'One way 98')
# ('Vicky', 'Yellow Garden 2')
# ('Ben', 'Park Lane 38')
# ('William', 'Central st 954')
# ('Chuck', 'Main Road 989')
# ('Viola', 'Sideway 1633')

mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchone() #  return the first row of the result

print(myresult)

# output:
# ('John', 'Highway 21', 1)