#!/usr/bin/env python

import os
import sys
import time
import random
import socket

from leds_control import LedsControl

import termios, sys, os

LED_MAX_VAL = 4095	# Value for max power of the leds
NB_LEDS = 11		# Number max of leds that can be connected to the board


def turn_leds_off():
	values = [0] * 11;
	ledsCtrl.usb_send_values( values );

def turn_leds_on():
	values = [4095] * 11;
	ledsCtrl.usb_send_values( values );

def set_leds_value( value ): # float value expected fom 0 to 1
	values = [value*4095] * 11;
	ledsCtrl.usb_send_values( values );

def set_leds_random():
	rndNumber = random.randint(0, 4095);
	values = [rndNumber] * 11;
	ledsCtrl.usb_send_values( values );

def get_leds_value():
	values = ledsCtrl.usb_read_values();
	values = ledsCtrl.usb_read_values();
	return float( values[0] ) / LED_MAX_VAL;


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

	try:
		ledsCtrl = LedsControl();
		shutdown = 0;

	except SystemExit, e:
		shutdown = 1;
		print("Exception in LedsControl");

        while not shutdown:
                c = getkey()
                if c == ' ':
		    	print ' =============== READ VALUES'
			val = get_leds_value();
			print 'val = ' + str(val);
		
		elif c == 'o':
		    	print ' =============== TURN ON'
			turn_leds_on();

		elif c == 'p':
		    	print ' =============== TURN OFF'
			turn_leds_off();

		elif c == 'm':
		    	print ' =============== MIDDLE RANGE'
			set_leds_value(0.5);

		elif c == 'r':
		    	print ' =============== RANDOM'
			set_leds_random();

		elif c == 'q':
			shutdown = 1;

	print(' =============== END')

