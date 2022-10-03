import serial
import pynmea2
import os

def GPS(n=0,gps=''):
	while True:
		port="/dev/ttyAMA0"
		os.system("sudo chmod 777 /dev/ttyAMA0")
		ser=serial.Serial(port, baudrate=9600, timeout=0.5)
		dataout = pynmea2.NMEAStreamReader()
		gps_2 =gps
		try:
			newdata=ser.readline()
		except Exception as e:
			print(e)
		newdata = '$GPRMC,125728.000,A,19979.296568354,N,11051.1114843533,E,0.25,100.97,270422,,,A,V*08'
		if newdata[0:6] == '$GPRMC':
			data = newdata.split(',',7)
			lat=float(data[5])/100
			lng=float(data[3])/1000
			gps = "Latitude=" + str(lat) + "and Longitude=" +str(lng)
		else: n = n-1
		if n < 0:
			return 0
		if gps_2 == gps:
			n = n+1 
		if n == 4:
			gps_1 = [lat, lng]
			return (gps_1)