#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 06:48:12 2024

@author: tze
"""

from submodules.tkWindget import AppFrame, FigureFrame, IPEntry, OnOffButton, LabelButton
from submodules.Figures import FigureXY2
from numpy import append, newaxis
from tkinter.filedialog import asksaveasfilename
from submodules.RW_files import Files_RW
from submodules.RW_files import Read_from, Write_to
import os
from tkinter import DISABLED, Frame, Button, StringVar, IntVar, DoubleVar, Toplevel
from socket import socket
import time




class IP_instrument(Toplevel):
    def __init__(self,file,extension,label,geometry=(400,400,10,10),connect=None,disconnect=None):
        #connect disconnect are actions from the that this element should do upon connecting and disconnecting
        super().__init__()
        if connect==None:
            self.main_connect=self.placeholder
        else:
            self.main_connect=connect
        if disconnect==None:
            self.main_disconnect=self.placeholder
        else:
            self.main_disconnect=disconnect
        self.label=label
        self.labeltext=self.label.get_var()
        self.protocol("WM_DELETE_WINDOW",self.mywithdraw)
        self.protocol("WM_ICON_WINDOW",self.mywithdraw)#disable this button
        self.geometry('%dx%d+%d+%d' % geometry)
        self.ini=Read_from.inst(file=file,extension=extension)
        if self.ini['error']:
            self.ini={}
            self.ini["ip_address"]=None
            self.ini["port"]=None
            self.ini["inst_name"]=""
        self.init_frame()
        self.init_elements()
        self.init_variables()

    def mywithdraw(self):
        self.withdraw()
        self.mydisplay=False

    def mydeiconify(self):
        self.deiconify()
        self.mydisplay=True

    def init_frame(self):
        self.frameroot=Frame(self)
        self.frameroot.pack(pady = (25,25), padx = (25,25))

    def init_elements(self):
        self.IPEntry=IPEntry(parent=self.frameroot,address=f"{self.ini['ip_address']}:{self.ini['port']}")
        self.IPEntry.grid(row=1,column=1)
        self.status=OnOffButton(parent=self.frameroot,commandon=self.connect,commandoff=self.disconnect)
        self.status.grid(row=2,column=1)
        self.status.enable_press()

    def init_variables(self):
        self.sock=socket()

    def placeholder(self):
        pass
    def connect(self):
        try:
            #self.sock.connect((self.IPEntry.get_address(), self.IPEntry.get_port()))
            #self.sock.send("*IDN?\n".encode('utf-8'))
            #self.ini["inst_name"]=self.sock.recv(1024).decode('utf-8')
            #self.label.set_var(self.ini["inst_name"].split(',')[1]+'\n'+self.ini["inst_name"].split(',')[2])
            self.IPEntry.disable()
            self.status.change_state('on')
            self.label.set_var('Test')
            self.update()
            self.main_connect()
            time.sleep(0.5)
            self.mywithdraw()
        except:
            self.status.change_state('off')

    def disconnect(self):
        self.sock.close()
        self.IPEntry.enable()
        self.label.set_var(self.labeltext)
        self.update()
        self.main_disconnect()
        time.sleep(0.5)
        self.mywithdraw()

class PowerSupply_AmMeter(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(900,600,10,10))
        self.init_frames()
        self.init_command_frame()
        self.init_variables()
        #self.figure.plot.update_labels("new X","old Y1",'old Y2')

    def init_variables(self):
        self.ps_ip_init=False

    def init_frames(self):
        #for the buttons and file list
        self.command_frame = Frame(self.frameroot)
        self.command_frame.grid(column=0,row=0)
        self.command_frame.columnconfigure(0, weight = 1)
        self.command_frame.rowconfigure(0, weight = 1)

        #for the figure
        #self.figure=FigureFrame(parent=self.frameroot,figclass=FigureXY2,figkwargs={"y2":True})
        #self.figure=FigureFrame(parent=self.frameroot,figclass=FigureXY2
        #self.figure.grid(row=0,column=1)
        #self.figure.columnconfigure(0, weight = 1)
        #self.figure.rowconfigure(0, weight = 1)    

    def init_command_frame(self):
        rowcount=1
        self.instrument=LabelButton(self.command_frame, text='Connect Power Supply', command=self.setup_ps,width=18,bg='lightgray')
        self.instrument.grid(row=rowcount,column=1)
        rowcount+=1
        getip=Button(self.command_frame, text="Get IP", command=self.get_ip,width=18,bg='lightgray')
        getip.grid(row=rowcount,column=1)

        #Button(self.command_frame, text="Disconnect\ninstruments", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=2)
        #rowcount+=1
        #Button(self.command_frame, text="Measure point", command=self.fake,width=12,bg='lightgray').grid(row=rowcount,column=1)
        #Button(self.command_frame, text="Clear point", command=self.fake2,width=12,bg='lightgray').grid(row=rowcount,column=2)
        #rowcount+=1
        #Button(self.command_frame, text="Save data", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=1)
        #Button(self.command_frame, text="Clear data", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=2)    

    def get_ip(self):
        print(self.ps_level.IPEntry.get_address_port())

    def setup_ps(self):
        if not self.ps_ip_init:
            self.ps_level=IP_instrument(file=__file__,extension='psinst',label=self.instrument)
            self.ps_level.mywithdraw()
            self.ps_ip_init=True
        if self.ps_level.mydisplay:
            self.ps_level.mywithdraw()
        else:
            self.ps_level.mydeiconify()

    def connect_ps(self):
        pass

    def disconnect_ps(self):
        pass

    def fake(self):
        self.figure.plot.update_labels(y2="new Y2")
        self.figure.canvas.draw()

    def fake2(self):
        self.figure.plot.update_labels(x="x", y1="bla")
        self.figure.canvas.draw()

    def placeholder(self):
        pass

    def save_data(self):
        header=[]
        text='#comment'
        header.append(text)
        text="#setup"
        header.append(text)
        text='#data_header'
        header.append(text)
        text=f'{self.xname}\t{self.variables["quantity"].get()}'
        header.append(text)
        text=f'{self.units[self.xname]}\t{self.units[self.variables["quantity"].get()]}'
        header.append(text)
        text='#data_table'
        header.append(text)
        data=append(self.datatime[:,newaxis],self.data[:,newaxis],axis=1)
        fmtlist=['%.6e','%.6e']
        filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("Tab sep file","*.log")],initialfile='Measured_IV')
        if filename:
            Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
            self.savedir=os.path.dirname(filename)
            #self.write_to_ini()
            self.command_elements['save'].config(state=DISABLED)