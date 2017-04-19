#!/usr/bin/python3

import serial

con = serial.Serial('/dev/ttyAMA0', 9600)

while True:
	line = input()
	
	if line == 'f':
		con.write(b'50 50')
	elif line == 'ff':
		con.write(b'100 100')
	elif line == 'fs':
		con.write(b'10 10')
	elif line == 'fr':
		con.write(b'100 30')
	elif line == 'fl':
		con.write(b'30 100')
	elif line == 'b':
		con.write(b'-50 -50')
	elif line == 'bb':
		con.write(b'-100 -100')
	elif line == 'br':
		con.write(b'-100 -30')
	elif line == 'bl':
		con.write(b'-30 -100')
	elif line == 'bs':
		con.write(b'-10 -10')
	elif line == 'r':
		con.write(b'50 -50')
	elif line == 'rr':
		con.write(b'100 -100')
	elif line == 'rs':
		con.write(b'10 -10')
	elif line == 'l':
		con.write(b'-50 50')
	elif line == 'll':
		con.write(b'-100 100')
	elif line == 'ls':
		con.write(b'-10 10')
	elif line == 's':
		con.write(b'0 0')
	elif line == 'exit':
		con.write(b'0 0')
		exit(0)
	else:
		print('unknown cmd')
		con.write(b'0 0')
