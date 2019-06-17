import mysql.connector as mc

connection = mc.connect (host = "127.0.0.1",
                         user = "mct",
                         passwd = "mct",
                         db = "solarweatherstation")

cursor = connection.cursor()
cursor.execute("SELECT * FROM meting")
result = cursor.fetchall()
for r in result:
    print (r)

cursor.close()
connection.close()