#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:57:35 2023

@author: tze
"""

import time
import socket
import numpy as np
import matplotlib.pyplot as plt

voltages=np.linspace(0,6,51)
mvolt=np.zeros(np.shape(voltages))
mcurr=np.zeros(np.shape(voltages))
mpow=np.zeros(np.shape(voltages))



sock=socket.socket()
sock.connect(('192.168.1.250', 5025))
sock.send("*IDN?\n".encode('utf-8'))
print(sock.recv(2048).decode('utf-8'))
sock.send("OUT OFF\n".encode('utf-8'))
sock.send("OUT2 OFF\n".encode('utf-8'))


sockidc=socket.socket()
sockidc.connect(("192.168.1.210",5025))
sockidc.send('CURR:APER 0.2\n'.encode('utf-8'))
sockidc.send("*IDN?\n".encode('utf-8'))
#print(sockidc.recv(2048).decode('utf-8'))
if sockidc.recv(2048).decode('utf-8')=="KEITHLEY INSTRUMENTS,MODEL DAQ6510,04480963,1.0.04b\n":
    sockidc.send('CURR:DC:RANGE 1\n'.encode('utf-8'))    
else:
    sockidc.send('CONF:CURR:DC 3\n'.encode('utf-8'))


sock.send("OUT:MIN:VOLT 0\n".encode('utf-8'))
sock.send("OUT:MAX:VOLT 21\n".encode('utf-8'))

sock.send("SOUR:VOLT 0\n".encode('utf-8'))
time.sleep(0.005)
sock.send("OUT ON\n".encode('utf-8'))

for i in range (0,np.shape(voltages)[0]):
        sock.send(f"SOUR:VOLT {voltages[i]}\n".encode('utf-8'))
        time.sleep(0.2)
        sock.send("MEAS:VOLT?\n".encode('utf-8'))
        mvolt[i]=float(sock.recv(2048).decode('utf-8'))
        sockidc.send('MEAS:CURR?\n'.encode('utf-8'))
        mcurr[i]=float(sockidc.recv(2048).decode('utf-8'))
        
sock.send("OUT OFF\n".encode('utf-8'))


plt.plot(mvolt,mcurr)
plt.show()

