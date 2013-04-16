 #!/usr/bin/env python

import os
import sys
import time
import random
import socket
import json

#from leds_control import LedsControl

import termios, sys, os

HOST = 'localhost'	# Symbolic name meaning all available interfaces
PORT = 30000           	# Arbitrary non-privileged port

LED_MAX_VAL = 4095	# Value for max power of the leds
NB_LEDS = 11		# Number max of leds that can be connected to the board

def set_leds_value( value ): # float value expected fom 0 to 1
	values = [value*LED_MAX_VAL] * NB_LEDS;
	print 'Leds val: ', value
	#ledsCtrl.usb_send_values( values );


def getkey():
	term = open("/dev/tty", "r")
	fd = term.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] &= ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, new)
	c = None
	try:
		c = os.read(fd, 1)
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		term.close()
	return c


if __name__ == '__main__':

	print 'Try to connect to board';
	try:
		#ledsCtrl = LedsControl();
		shutdown = 0;

	except SystemExit, e:
		shutdown = 1;
		print 'Exception in LedsControl';

	print 'Try to connect to ' + HOST + ':' + str(PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)

	while not shutdown:
	
		conn, addr = s.accept();
		print 'Connected by', addr;
	
		while 1:
			data = conn.recv(1024)
			cmd = '';
			if not data:
				break
			
			d = json.loads( data );	# create a dict from json string
			
			if 'val' in d:
				set_leds_value( float(d['val']) );
				cmd = '{\"leds_val\":'+ d['val'] +'}'
				conn.sendall(cmd)
			elif 'cmd' in d:
				if d['cmd'] == 'get_leds_intensity':
					cmd = '{\"leds_val\":'+ str(-1) +'}'
					conn.sendall(cmd)
				elif d['cmd'] == 'disconnect':
					cmd = '{\"disconnect\":true}'
					conn.sendall(cmd)
					break
				elif d['cmd'] == 'shutdown':
					cmd = '{\"shutdown\":true}'
					conn.sendall(cmd)
					shutdown = 1
					break
			else:
				cmd = '{\"error\":\"cmd_not_found\"}';
				conn.sendall(cmd);
				
		conn.close();
		print ' CONNECTION CLOSED ';

