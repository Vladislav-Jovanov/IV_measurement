#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:57:35 2023

@author: tze
"""

import time
import socket
import select
#import pyvisa
#rm = pyvisa.ResourceManager()

#item='TCPIP::192.168.1.210'


#keythley = rm.open_resource(item)
#print(keythley.query('*IDN?\n'))
#keythley.write("*RST")

#keythley.write('SOUR:VOLT2 4.5')
#keythley.write('OUT2 ON')
#time.sleep(0.3)
#keythley.write('MEAS:CURR2?')
#time.sleep(0.3)
#print(keythley.read_raw())
#keythley.write('MEAS:VOLT2?')
#time.sleep(0.3)
#print(keythley.read_raw())

#port 5025 is also for keysight
sock=socket.socket()
sock.connect(('192.168.1.210', 5025))
sock.send("*RST\n".encode('utf-8'))

sock.send("OUT2 ON\n".encode('utf-8'))
sock.send("MEAS:CURR2?\n".encode('utf-8'))

#youll need to add select if you have many data points to measure at once
sock.recv(2048).decode('utf-8')
sock.send("MEAS:VOLT2?\n".encode('utf-8'))
sock.recv(2048).decode('utf-8')


#set of commands for keysight current and voltage measurement
sock.connect(('192.168.1.220', 5025))
sock.send("*RST\n".encode('utf-8'))
sock.send("*IDN?\n".encode('utf-8'))
sock.recv(2048).decode('utf-8')
sock.send("CURR:APER 0.2\n".encode('utf-8'))
sock.send("VOLT:APER 0.2\n".encode('utf-8'))


sock.send(':CONF:VOLT:DC 10\n'.encode('utf-8'))
sock.send('TRIG:SOUR BUS\n'.encode('utf-8'))
sock.send('SAMP:COUN 10\n'.encode('utf-8'))
sock.send('INIT\n'.encode('utf-8'))
sock.send('*TRG\n'.encode('utf-8'))
sock.send('FETC?\n'.encode('utf-8'))
sock.recv(2048).decode('utf-8')
sock.send(':CONF:VOLT:DC 10\n'.encode('utf-8'))
sock.send(':MEAS:VOLT:DC? 10 \n'.encode('utf-8'))
sock.recv(2048).decode('utf-8')
sock.send(':CONF:CURR:DC 0.1\n'.encode('utf-8'))
sock.send(':MEAS:CURR?\n'.encode('utf-8'))
sock.recv(2048).decode('utf-8')