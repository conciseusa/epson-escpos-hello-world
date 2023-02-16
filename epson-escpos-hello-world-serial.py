#!/usr/bin/python

# run with `python3 epson-escpos-hello-world-serial.py`

import serial
from datetime import datetime
import time

# Windows built in serial port
#serialp  = 'COM1'
# USB serial port
#serialp  = '/dev/ttyUSB0'
# Ubuntu on box with built-in serial port `python3 epson-escpos-hello-world-serial.py`
# Tested with Epson TM-T20II connected with a Monoprice #479 6ft Null Modem DB9F/DB25M Molded Cable
serialp  = '/dev/ttyS0'
# Pine A64
#serialp  = '/dev/ttyS2'
# Raspberry Pi, may need to setup serial port first
#serialp  = '/dev/serial0'

# some common commands
init=b'\x1b\x40' # ESC @ Initialize printer
lf=b'\x0a' # LF Prints the data in the print buffer and feeds one line
gs=b'\x1d' # GS Group Separator
cut=gs+b'\x56\x00'; # GS V x00 worked on TM-T20II

# https://stackoverflow.com/questions/59887559/python-send-escpos-command-to-thermal-printer-character-size-issue
def magnify(wm, hm): # Code for magnification of characters.
    # wm: Width magnification from 1 to 8. Normal width is 1, double is 2, etc.
    # hm: Height magnification from 1 to 8. Normal height is 1, double is 2, etc.
    return bytes([0x1d, 16*(wm-1) + (hm-1)])

def text(t, encoding="ascii"): # Code for sending text.
    return bytes(t, encoding)

ser = serial.Serial(serialp, 38400) # , timeout=0.050
ser.write(init)

ser.write(text("Hello World! The time is:"))
ser.write(lf)

now = datetime.now()
ser.write(text("{}".format(now.strftime("%Y/%m/%d %H:%M:%S"))))
ser.write(lf)

# ser.write(magnify(2, 2)) # did not seem to do anything on TM-T20II
count = 0
while count <= 3:
    ser.write(text("Sent {} line(s)".format(count)))
    ser.write(lf)
    time.sleep(1)
    count += 1

ser.write(lf+lf+lf+lf) # move printed area above blade
ser.write(cut)
