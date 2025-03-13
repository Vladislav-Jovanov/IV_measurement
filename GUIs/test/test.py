#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 06:48:12 2024

@author: tze
"""

from tkWindget.tkWindget import AppFrame, FigureFrame
from Figures.Figures import FigureXY2
from numpy import append, newaxis
from tkinter.filedialog import asksaveasfilename
from RW_data.RW_files import Files_RW
import os
from tkinter import DISABLED, Frame, Button, StringVar, IntVar, DoubleVar

class Test(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(900,600,10,10))
        self.init_variables()
        self.init_frames()
        self.init_command_frame()
        self.figure.plot.update_x_label("new X")
        self.figure.plot.update_y_label("new Y1")
    
    def init_variables(self):
        pass
    
    def init_frames(self):
        #for the buttons and file list
        self.command_frame = Frame(self.frameroot)
        self.command_frame.grid(column=0,row=0)
        self.command_frame.columnconfigure(0, weight = 1)
        self.command_frame.rowconfigure(0, weight = 1)

        #for the figure
        self.figure=FigureFrame(parent=self.frameroot,figclass=FigureXY2,figkwargs={"y2":True})
        #self.figure=FigureFrame(parent=self.frameroot,figclass=FigureXY2
        self.figure.grid(row=0,column=1)
        self.figure.columnconfigure(0, weight = 1)
        self.figure.rowconfigure(0, weight = 1)    
        
    def init_command_frame(self):
        rowcount=1
        Button(self.command_frame, text="Connect\ninstruments", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.command_frame, text="Disconnect\ninstruments", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=2)
        rowcount+=1
        Button(self.command_frame, text="Measure point", command=self.fake,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.command_frame, text="Clear point", command=self.fake2,width=12,bg='lightgray').grid(row=rowcount,column=2)
        rowcount+=1
        Button(self.command_frame, text="Save data", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.command_frame, text="Clear data", command=self.placeholder,width=12,bg='lightgray').grid(row=rowcount,column=2)    
    
    def fake(self):
        self.figure.plot.update_y2_label("new Y2")
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
        