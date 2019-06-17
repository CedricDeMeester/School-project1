import serial
import time
import MySQLdb as mdb

arduino = serial.Serial("/dev/ttyUSB0")
arduino.baudrate=9600

data = arduino.readline()
con = mdb.connect('localhost', 'mct', 'mct', 'solarweatherstation');

while True:
	data = arduino.readline()
	data = data.decode("utf-8")
	pieces = data.split(":")

	press = pieces[0]
	hum = pieces[1]
	temp = pieces[2]

	print(press)
	print(hum)
	print(temp)

cursor = con.cursor()
cursor.execute('''INSERT INTO meting("",waarde,tijd, sensor_id) VALUES(%s,%s,%s)''',(press, "06/10/2019", "1"))
con.commit()
cursor.close()


