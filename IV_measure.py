#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:02:13 2022

@author: tze
"""
import numpy as np
from RW_data.RW_files import Files_RW
from matplotlib.figure import Figure
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pyvisa
import os
from tkinter.filedialog import asksaveasfilename


class container():
    pass


class FigureIV():
    def __init__(self):
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        self.dim=container()
        self.dim.figwidth=11/2.54#fullfigure size
        self.dim.figheight=8/2.54#fullfigure size
        self.dim.x0=2/(2.54*self.dim.figwidth)#relative to large figure
        self.dim.y0=2/(2.54*self.dim.figwidth)#relative to large figure
        self.dim.w=7/(2.54*self.dim.figwidth)#small fig size in percentage of large figure
        self.dim.h=5/(2.54*self.dim.figheight)#small fig size in percentage of large figure

        self.fig=Figure()
        self.fig.set_size_inches((self.dim.figwidth,self.dim.figheight))
        self.axl=self.fig.add_axes([self.dim.x0,self.dim.y0,self.dim.w,self.dim.h])
        self.axl.tick_params(labelsize=8)
        self.axl.tick_params(axis='y',labelcolor='tab:blue')
        self.axl.set_xlabel('Voltage [V]',fontsize=10, position=(0.5,0),labelpad=5)
        self.axl.set_ylabel('Current [A]',fontsize=10,  position=(0,0.5),labelpad=5,color='tab:blue')
        self.axl.set_xlim(0,7.5)
        #self.axl.set_xticks(np.arange(0, 7.5, 0.5))
        self.axl.set_ylim(0,0.05)
        #linked right axes  https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html#sphx-glr-gallery-subplots-axes-and-figures-two-scales-py
        self.axr=self.axl.twinx()
        self.axr.tick_params(labelsize=8)
        self.axr.tick_params(axis='y',labelcolor='tab:red')
        self.axr.set_ylabel('Power [W]',fontsize=10,  position=(0,0.5),labelpad=5, color='tab:red')
        self.axr.set_ylim(0,1)



    def plot_data(self,axes,x,y):
        axes.axhline(color='k',linewidth=1,y=0)
        axes.axvline(color='k',linewidth=1,x=0)
        axes.plot(x,y)

    def update_label(self, axes, label, string):
        if label=='x_label':
            axes.set_xlabel(string,fontsize=10, position=(0.5,0),labelpad=5)
        elif label=='y_label':
            axes.set_ylabel(string,fontsize=10, position=(0.5,0),labelpad=5)


class GUI_measure_IV():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x480")
        self.root.title("IV curves")
        self.init_frames()
        self.init_figure_frame()
        self.init_command_frame()
        self.init_variables()
        try:
            tmp=Files_RW().check_IV_measure_ini(self.scriptdir,self.ini_name,self.split)
            self.savedir=tmp.savedir
        except:
            self.savedir='Documents'
            self.write_to_ini()
        self.init_instrument_ip()

    def write_to_ini(self):
        write=[]
        write.append(f'save_file_path{self.split}{self.savedir}')

        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)

    def init_variables(self):
        self.split=':='
        self.x=[]
        self.y=[]
        self.p=[]
        self.scriptdir=os.path.dirname(__file__)#path of this __file__ not the __main__
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')


    def init_instrument_ip(self):
        filename=self.ini_name.split('.')[0]+'.instr'
        self.ip_list=Files_RW().check_IV_measure_inst_file(self.scriptdir,filename,self.split)


    def init_frames(self):
        self.rootframe=tk.Frame(self.root)
        self.rootframe.pack(pady = (25,25), padx = (25,25))
        #for the buttons and file list
        self.command_frame = tk.Frame(self.rootframe)
        self.command_frame.grid(column=0,row=0,rowspan=3)
        self.command_frame.columnconfigure(0, weight = 1)
        self.command_frame.rowconfigure(0, weight = 1)

        #for the figure
        self.figure_frame=tk.Frame(self.rootframe)
        self.figure_frame.grid(column=1,row=2,columnspan=3)
        self.figure_frame.columnconfigure(0, weight = 1)
        self.figure_frame.rowconfigure(0, weight = 1)

    def init_start(self):
        self.root.mainloop()

    def init_command_frame(self):
        rowcount=1
        tk.Button(self.command_frame, text="Connect\ninstruments", command=self.connect,width=12,bg='lightgray').grid(row=rowcount,column=1)
        tk.Button(self.command_frame, text="Disconnect\ninstruments", command=self.disconnect,width=12,bg='lightgray').grid(row=rowcount,column=2)
        rowcount+=1
        tk.Button(self.command_frame, text="Measure point", command=self.measure,width=12,bg='lightgray').grid(row=rowcount,column=1)
        tk.Button(self.command_frame, text="Clear data", command=self.restart,width=12,bg='lightgray').grid(row=rowcount,column=2)
        rowcount+=1
        tk.Button(self.command_frame, text="Save data", command=self.save_data,width=12,bg='lightgray').grid(row=rowcount,column=1,columnspan=2)

    def setup_instruments(self):
        #this is now hardcoded but this should optional
        for item in self.instruments:
            item.write('CURR:APER 0.2')
            item.write('VOLT:APER 0.2')
            item.write(':SENS:CURR:RANG 0.1')
            item.write(':SENS:VOLT:RANG 10')


    def connect(self):
        self.instruments=[]
        rm = pyvisa.ResourceManager()
        for item in self.ip_list:
            try:
                tmp=rm.open_resource(item)
                tmp.write('*RST')
                self.instruments.append(tmp)
            except:
                pass
        self.setup_instruments()

    def disconnect(self):
        while len(self.instruments):
            item=self.instruments.pop()
            item.close()

    def measure(self):
        v=self.instruments[0].query(':MEAS:VOLT?')
        self.x.append(float(v.strip()))
        i=self.instruments[1].query(':MEAS:CURR?')
        self.y.append(float(i.strip()))
        self.p.append(self.x[-1]*self.y[-1])
        self.plot_data()

    def clear_graph(self):
        while (len(self.plot.axl.lines)):
            self.plot.axl.lines[0].remove()
        while (len(self.plot.axr.lines)):
            self.plot.axr.lines[0].remove()


    def plot_data(self):
        self.clear_graph()
        self.plot.axl.plot(self.x,self.y, color='tab:blue')
        self.plot.axl.set_ylim(0,2*max(self.y))
        self.plot.axr.plot(self.x,self.p, color='tab:red')
        self.plot.axr.set_ylim(0,2*max(self.p))
        self.canvas.draw()

    def save_data(self):
        if len(self.x)==len(self.y) and (len(self.y)>=1):
            header=[]
            text='#comment'
            header.append(text)
            text="#setup"
            header.append(text)
            text='#data_header'
            header.append(text)
            text='voltage\tcurrent'
            header.append(text)
            text='V\tA'
            header.append(text)
            text='#data_table'
            header.append(text)
            x=np.array(self.x)
            y=np.array(self.y)
            data=np.append(x[:,np.newaxis],y[:,np.newaxis],axis=1)
            fmtlist=['%.6e','%.6e']
            filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("E60 tab sep file","*.iv")],initialfile='Measured_IV')
            if filename:
                Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
                self.savedir=os.path.dirname(filename)
                self.write_to_ini()

    def restart(self):
        if len(self.x)==len(self.y) and (len(self.p)>=1):
            self.x=[]
            self.y=[]
            self.p=[]
            self.clear_graph()
        self.canvas.draw()

    def init_figure_frame(self):
        rowcount=1
        self.plot=FigureIV()
        self.canvas=FigureCanvasTkAgg(self.plot.fig,master=self.figure_frame)
        self.canvas.get_tk_widget().grid(row=rowcount,column=1)
        self.canvas.draw()
        rowcount+=1
        toolbar = NavigationToolbar2Tk(self.canvas, self.figure_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=rowcount,column=1)


if __name__=='__main__':
    GUI_measure_IV.init_start(GUI_measure_IV())
