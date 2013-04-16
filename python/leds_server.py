 #!/usr/bin/env python

import os
import sys
import time
import random
import socket
import json

from leds_control import LedsControl

import termios, sys, os

HOST = '' #'localhost'	# Symbolic name meaning all available interfaces
PORT = 30000           	# Arbitrary non-privileged port

LED_MAX_VAL = 4095	# Value for max power of the leds
NB_LEDS = 11		# Number max of leds that can be connected to the board
LEDS_LERP_DT = 0.05	# refreshing time of the leds lerp fct.

def get_leds_value():

	values = ledsCtrl.usb_read_values();
	values = ledsCtrl.usb_read_values();
	val = float( values[0] ) / LED_MAX_VAL;
	#print 'Get leds val: ', val;
	return val;

def set_leds_value( value ): # float value expected fom 0 to 1

	values = [value*LED_MAX_VAL] * NB_LEDS;
	#print 'Set leds val: ', value
	ledsCtrl.usb_send_values( values );

def lerp_to_leds_value( value, duration ):

	val_init = get_leds_value();
	d_val_per_sec = ( value - val_init ) / duration;
	
	t = 0;
	t_init = time.time();

	while t < duration:
		val = val_init + d_val_per_sec*t;
		if val < 0:
			val = 0;
		elif val > 1:
			val = 1;
		#print 'val: ', val, '; t: ', t;
		set_leds_value( val );
		time.sleep( LEDS_LERP_DT );
		t = time.time() - t_init;

	set_leds_value( value );	

if __name__ == '__main__':

	print 'Try to connect to board';
	try:
		ledsCtrl = LedsControl();
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

			try:
				d = json.loads( data );	# create a dict from json string
			except:
				continue;

			if 'val' in d:
				val = d['val'];
				if 'dur' in d:
					dur = d['dur'];
					lerp_to_leds_value( val, dur );
				else:
					set_leds_value( val );
				cmd = '{\"leds_val\":'+ str( d['val'] ) +'}'
				conn.sendall(cmd)

			elif 'cmd' in d:
				if d['cmd'] == 'get_leds_intensity':
					val = get_leds_value();
					cmd = '{\"leds_val\":'+ str(val) +'}'
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

