#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
import numpy as np
import os


class container():
    pass

            
class Files_RW():
    #to have it here although not used
    def Add_items(self,text,itemlist,sep):
        for item in itemlist:
            text=text+str(item)+sep
        return text[:-1]
            
    def check_IV_measure_ini(self,dirname,filename,split):
        out=container()
        with open(os.path.join(dirname,filename), 'r') as f:
            for line in f:
                a=line.strip()
                tmp=a.split(split)
                if tmp[0]=='save_file_path':
                    out.savedir=tmp[-1]
        return out
    
    def check_IV_measure_inst_file(self,dirname,filename,split):
        ip_list=[]
        with open(os.path.join(dirname,filename), 'r') as f:
            for line in f:
                a=line.strip()
                tmp=a.split(split)
                ip_list.append(tmp[-1])
        return ip_list
    
        
    def write_to_file(self,dirname,filename,write):
        with open(os.path.join(dirname,filename),'w') as f:
            for line in write:
                np.savetxt(f, [line], delimiter='\t', newline='\n', fmt='%s')
    
    def write_header_data(self,dirname,filename,header,data,fmtlist):
        with open(os.path.join(dirname,filename),'w') as f:
            for line in header:
                np.savetxt(f, [line], delimiter='\t', newline='\n', fmt='%s')
            for line in data:
                np.savetxt(f, [line], delimiter='\t', newline='\n', fmt=fmtlist)

#    def read_dsp(self,filename):
#        out=container()
#        setup_marker=0
#        setup=[]
#        data_marker=0
#        out.data=[]
#        out.error=''
#        try: 
#            with open(filename,'r') as f:
#                for line in f:
#                    tmp=line.strip()                   
#                    if tmp.startswith('%'):
#                        setup_marker=0
#                        out.type=tmp
#                    if setup_marker:
#                        setup.append(float(tmp));
#                    if tmp=='nm':
#                        setup.append(tmp)
#                        setup_marker=1
#                    if data_marker:
#                        out.data.append(float(tmp))
#                    if tmp=='#DATA':
#                        data_marker=1
#        except:
#            out.error='File cannot be read!'
#        #to be furthered improved             
#        out.wlength=np.linspace(setup[1],setup[2],setup[4])
#        out.units=setup[0]
#        out.data=np.array(out.data)
#        return out
#    
#             
#    def load_reference_TMM(self,filename):
#        out=container()
#        header_marker=1
#        data_marker=0
#        out.wlength=[]
#        out.data=[]
#        out.error=''
#        try:
#            with open(filename, 'r') as f:
#                for line in f:
#                    tmp=line.strip()
#                    if data_marker:
#                        data=tmp.split('\t')
#                        out.wlength.append(float(data[0]))
#                        out.data.append(float(data[1]))
#                    if header_marker:
#                        header=tmp.split('\t')
#                        winfo=header[0].split()#['wlength,'(nm)'']
#                        out.units=winfo[1][1:-1] #units='nm'
#                        header_marker=0
#                        data_marker=1
#                        #maybe remove this last part
#                        if header[1]!='Input media':
#                            out.error='Wrong file loaded!'
#        except:
#            out.error='Wrong file loaded!'
#        
#        out.type='Reflectance (%)'
#        out.wlength=np.array(out.wlength)
#        out.data=np.array(out.data)
#        return out
#    
#    def load_dtsp(self,filename):#very similar to reference file
#        out=container()
#        header_marker=1
#        data_marker=0
#        out.wlength=[]
#        out.data=[]
#        out.error=''
#        try:
#            with open(filename, 'r') as f:
#                for line in f:
#                    tmp=line.strip()
#                    if data_marker:
#                        data=tmp.split('\t')
#                        out.wlength.append(float(data[0]))
#                        out.data.append(float(data[1]))
#                    if header_marker:
#                        header=tmp.split('\t')
#                        winfo=header[0].split()#['wlength,'(nm)'']
#                        out.units=winfo[1][1:-1] #units='nm'
#                        header_marker=0
#                        data_marker=1
#                        #maybe remove this last part
#                        if header[1].startswith('%'):
#                            out.type=header[1]
#                        else:
#                            out.error='Wrong file loaded!'
#        except:
#            out.error='Wrong file loaded!'
#        
#        out.wlength=np.array(out.wlength)
#        out.data=np.array(out.data)
#        return out    