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




sock=socket.socket()
sock.connect(('192.168.1.210', 5025))
sock.send("*IDN?\n".encode('utf-8'))
tmp=sock.recv(2048).decode('utf-8')
print(tmp)


#aper is in seconds
sock.send('VOLT:APER 0.02\n'.encode('utf-8'))
sock.send("VOLT:AZERO 0\n".encode())

if tmp=="KEITHLEY INSTRUMENTS,MODEL DAQ6510,04480963,1.0.04b\n":
    sock.send('VOLT:DC:RANGE 10\n'.encode('utf-8'))    


#create buffer init part
#sock.send(f"TRAC:MAKE 'meas_buff', 10000\n".encode())


#measurement part
#trigger model
sock.send(f"TRIG:LOAD 'EMPTY'\n".encode())
sock.send(f"TRIG:BLOC:BUFF:CLEAR 1, 'defbuffer1'\n".encode())
sock.send(f"TRIG:BLOC:DEL:CONS 2, 0.02\n".encode())
#makes measurement
sock.send(f"TRIG:BLOC:MDIG 3, 'defbuffer1'\n".encode())
sock.send(f"TRIG:BLOC:BRAN:COUN 4, 1000, 2\n".encode())

#start measurement
sock.send("INIT\n".encode())

#stoping measurement
time.sleep(1000*(0.02+0.02)*0.8)
sock.send("ABORT\n".encode())


#getting data

#number of points
sock.send("TRAC:ACT? 'defbuffer1'\n".encode())
data_points=int(sock.recv(2048).decode())


#points
sock.send(f"TRAC:DATA? 1, {data_points}, 'defbuffer1', REL, READ\nINIT\n".encode())


data=''        
while len(data.strip().split(','))!=2*data_points or data=='':
    data=data+sock.recv(2048).decode()
new_data=data.strip().split(',')
data=[]
times=[]
#relative times
for idx,item in enumerate(new_data):
    if idx % 2:
        data.append(item)
    else:
        times.append(item)

data=np.array(data).astype('float')
times=np.array(times).astype('float')
        



sock.close()