import os
import sys
import math
import time
import struct
import md5
import re
import socket
import signal
import threading

#import socketFunctions
import TeensyRawhid

class LedsControl():
    def __init__(self, autostart = True):
        self.devices_init()
        
    def devices_init(self):
        # Init serial & usb
        self.usb_init()

    def usb_init(self):
        while True:
            try:
                self.device = TeensyRawhid.Rawhid()
                self.timeout = 50
                self.handler = self.usb_handler
                self.stophandler = self.usb_stophandler
                # NOTE: if you fail to open the device at this point even though you can
                # see the device listed (with 0x16c0/0x8000) in lsusb, check your udev
                # rules. You can also try re-running as root.
	    	vid = 0x03eb; #int(self.settings.xpath('/settings/usb/@vid')[0], 0)
	    	pid = 0x204f; #int(self.settings.xpath('/settings/usb/@pid')[0], 0)
	    	self.device.open(vid = vid, pid = pid, usage_page = -1, usage = -1)
                print ' =============== Connected';
                break
            except IOError, e:
                pass

    def usb_handler(self, pos):
        values = [128] * 11; #[int(led['interpoler'].value_at(pos) * 4095) for led in leds]

        # Read the current led values & sensors
        #self.usb_read_values()

        # Send the led values
        self.usb_send_values(values)

    def usb_stophandler(self):
        values = [0] * 11; #len(leds)
        self.usb_send_values(values)

    def usb_send_values(self, values):
        # Protocol is sending the number of leds followed by each led value split on two bytes
        # led values must be little endian
        buf = struct.pack('<B' + 'H' * len(values), len(values), *values)
        self.device.send(buf, self.timeout)

    def usb_read_values(self):
        answer = self.device.recv(64, self.timeout)

        # Parse leds
        leds_count = ord(answer[0])
        self.current_leds = struct.unpack('<' + ('H' * leds_count), answer[1:leds_count*2+1])
	return self.current_leds;

    def quit(self):
        if self.device is not None:
	    if self.enabled:
		device.stophandler()
	    self.device.close()
        
        self.close()


