
import sqlite3

# TASK 2: Create a new database
database = "purchases.db"
connection = sqlite3.connect(database)
cursor = connection.cursor()

filenames = ["users.csv", "purchases.csv", "purchaseParts.csv"]


# TASK 1: Read the contents of the csv files.
for loop in filenames:
    with open(loop, 'r') as f:
        for row in f.readlines():
            print(row)
        print("-----------------------")


# TASK 3: Create the tables
def dropAndCreateTable(name, information):
    cursor.execute(f"DROP TABLE IF EXISTS {name}")
    cursor.execute(f"CREATE TABLE {name}({information})")

for i in range(3):
    with open(filenames[i], 'r') as f:
        line = f.readline()
    dropAndCreateTable(filenames[i][:-4], line)


# TASK 4: Insert data into the tables:
def insertData(tablename, tablecolumns, tablerecords):
    cursor.execute(f"INSERT INTO {tablename}({tablecolumns}) VALUES ({tablerecords})")

for i in range(3):
    with open(filenames[i], 'r') as f:
        list = f.readline().replace(","," ")
        list = list.split()
        for i2 in range(len(list)):
            for x in list:
                if x.isupper() == True:
                    list.remove(x)
        list.remove(list[0])

    with open(filenames[i], 'r') as f:
        for x in f.readlines()[1:]:
            records = x[2:len(x)]
            insertData(filenames[i][:-4], ", ".join(list), records)
    
    print("Table:", filenames[i][:-4])
    for row in cursor.execute(f"SELECT * FROM {filenames[i][:-4]}"):
        print(row)

# TASK 5: Join all the tables

print("Join all tables:")
cursor.execute("SELECT * FROM users JOIN purchases ON purchases.userId=users.userId JOIN purchaseParts ON purchaseParts.purchaseId=purchases.purchaseId ORDER BY users.email ASC")
joinlist = cursor.fetchall()
for i in range(len(joinlist)):
    print(joinlist[i])


connection.commit()
connection.close()
    