#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 19:56:00 2024

@author: tze
"""
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import socket

voltages=np.linspace(0,2.5,51)
mvolt=np.zeros(np.shape(voltages))
mcurr=np.zeros(np.shape(voltages))
mpow=np.zeros(np.shape(voltages))


sockidc=socket.socket()
sockidc.connect(("192.168.1.210",5025))
sockidc.send('CURR:APER 0.2\n'.encode('utf-8'))
sockidc.send("*IDN?\n".encode('utf-8'))
if sockidc.recv(2048).decode('utf-8')=="KEITHLEY INSTRUMENTS,MODEL DAQ6510,04480963,1.0.04b\n":
    sockidc.send('CURR:DC:RANGE 1\n'.encode('utf-8'))    
else:
    sockidc.send('CONF:CURR:DC 1\n'.encode('utf-8'))

ser = serial.Serial()
#config
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE

ser.open()

ser.write("*IDN?\n".encode('utf-8'))
while not ser.inWaiting():
    time.sleep(0.1)
print(ser.readline().decode('utf-8'))
time.sleep(0.5)
ser.write("INST:SEL OUT2\n".encode('utf-8'))
ser.write("VOLT 0\n".encode('utf-8'))
ser.write("CURR 0\n".encode('utf-8'))
ser.write("INST:SEL OUT1\n".encode('utf-8'))
ser.write("CURR 1\n".encode('utf-8'))
ser.write("OUTP ON\n".encode('utf-8'))

for i in range (0,np.shape(voltages)[0]):
        print(i)
        ser.write(f"VOLT {voltages[i]}\n".encode('utf-8'))
        time.sleep(0.5)
        ser.write("MEAS:VOLT?\n".encode('utf-8'))
        time.sleep(0.5)
        while not ser.inWaiting():
            time.sleep(0.1)
        mvolt[i]=float(ser.readline().decode('utf-8'))
        sockidc.send('MEAS:CURR?\n'.encode('utf-8'))
        mcurr[i]=float(sockidc.recv(2048).decode('utf-8'))
        
        
ser.write("OUTP OFF\n".encode('utf-8'))

plt.plot(mvolt,mcurr)
plt.show()