#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 06:49:34 2024

@author: tze
"""

from matplotlib.figure import Figure
from numpy import min as npmin
from numpy import max as npmax
from numpy import append as npappend

#figure with linked right axes
class FigureXY2(Figure):
    def __init__(self,y2=False,**kwargs):
        super().__init__(**kwargs)
        self.set_size_inches((11/2.54,8/2.54))
        self.axy=self.add_axes([2/11,2/11,7/11,5/8])
        self.axy.tick_params(labelsize=8)
        self.axy.tick_params(axis='y',labelcolor='tab:blue')
        
        self.y2=y2
        
        if self.y2:
            #linked right axes  https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html#sphx-glr-gallery-subplots-axes-and-figures-two-scales-py
            self.axy2=self.axy.twinx()
            self.axy2.tick_params(labelsize=8)
            self.axy2.tick_params(axis='y',labelcolor='tab:red')
        
        self.init_figure()

    def update_x_label(self,xname):
        self.axy.set_xlabel(xname,fontsize=10, position=(0.5,0),labelpad=5)
        
    def update_y_label(self,yname):
        self.axy.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5)
        
    def update_y2_label(self,y2name):
        if self.y2:
            self.axy2.set_ylabel(y2name,fontsize=10, position=(0.5,0),labelpad=5)
        
    def update_labels(self,*args,**kwargs):
        if args:
            if len(args)>=3 and self.y2:
                self.update_y2_label(args[2])
            if len(args)>=2:
                self.update_y_label(args[1])
            if len(args)>=1:
                self.update_x_label(args[0])
            return
        if kwargs:
            if 'x' in kwargs:
                self.update_x_label(kwargs['x'])
            if 'y1' in kwargs:
                self.update_y_label(kwargs['y1'])
            if 'y2' in kwargs and self.y2:
                self.update_y2_label(kwargs['y2'])
            return
        

    #initlizes the figure
    def init_figure(self):
        self.axy.plot([],[],color='tab:blue')
        self.axy.set_xlim(0,1)
        self.axy.set_ylim(0,1)
        if self.y2:
            self.axy2.plot([],[],color='tab:red')
            self.axy2.set_ylim(0,1)
        
    #clear whole graph
    def clear_graph(self):
        while (len(self.axy.lines)):
            self.axy.lines[-1].remove()
        if self.y2:
            while (len(self.axy2.lines)):
                self.axy2.lines[-1].remove()
        self.init_figure()
    
    #clears last point
    def delete_last_point(self):
        if len(self.figure.plot.axy.lines)!=0:
            x=self.figure.plot.axy.lines[-1].get_xdata()
            y=self.figure.plot.axy.lines[-1].get_ydata()
            self.figure.plot.axy.lines[-1].set_xdata(x[:-1])
            self.figure.plot.axy.lines[-1].set_ydata(y[:-1])
        if self.y2:
            if len(self.figure.plot.axy2.lines)!=0:
                y2=self.figure.plot.axy2.lines[-1].get_ydata()
                self.figure.plot.axy2.lines[-1].set_ydata(y2[:-1])
            
    #if x negative i start from 1.02xmin, if x positive I start from 0
    #0.98 is here if I don't want to use 0 as reference
    def find_min(self,x):
        return min([0,1.02*(npmin(x)),0.98*(npmin(x))])
    #if x negative I start from 0, if x positive I end up with 1.02xmax
    #0.98 is here if I don't want to use 0 as reference
    def find_max(self,x):
        return max([0,1.02*(npmax(x)),0.98*(npmax(x))])
    
    #plots the data it receives (appending should be done in main if needed)
    def plot_data(self,x,y,y2):
        if len(x)==len(y):
            self.plot.axy.set_xlim(self.find_min(x),self.find_max(x))
            self.plot.axy.set_ylim(self.find_min(y),self.find_max(y))
        if len(self.figure.plot.axy.lines)!=0:
            self.figure.plot.axy.lines[-1].set_xdata(x)
            self.figure.plot.axy.lines[-1].set_ydata(y)
            
        if self.y2:
            if len(x)==len(y2):
                self.plot.axy2.set_ylim(self.find_min(y2),self.find_max(y2))
            
            if len(self.figure.plot.axy2.lines)!=0:
                self.figure.plot.axy2.lines[-1].set_ydata(y2)
    
    #appends and then plots data
    def append_plot_data(self,x,y,y2):
        if len(self.figure.plot.axy.lines)!=0:
            xold=self.figure.plot.axy.lines[-1].get_xdata()
            yold=self.figure.plot.axy.lines[-1].get_ydata()
        x=npappend(xold,x)
        y=npappend(yold,y)
        if self.y2:
            if len(self.figure.plot.axy2.lines)!=0:
                y2old=self.figure.plot.axy2.lines[-1].get_ydata()

            y2=npappend(y2old,y2)
            self.plot_data(x,y,y2)
        else:
            self.plot_data(x,y)
    