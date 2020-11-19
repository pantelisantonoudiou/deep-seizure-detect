# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:37:05 2020

@author: panton01
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# get figure and axis
fig, (ax,ax1,ax2) = plt.subplots(3,1,sharex = True, figsize=(8,8))
plt.subplots_adjust(bottom=0.2) # create space for buttons

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)


class matplotGui(object):
    
    # set internal counter
    ind = 0
       
    def __init__(self,data,idx_bounds,obj,file_id):
        """   
        Parameters
        ----------
        data : Numpy array

        idx_bounds : Nupy array (2 columns, 1 = start, 2 = stop index)

        obj: UserVerify object
        
        file_id: String - file anme

        """
        
        # pass object attributes
        self.data = data[:,:,0] # data
        self.data1 = data[:,:,1] # data
        self.data2 = data[:,:,2] # data
        
        self.idx = np.copy(idx_bounds) # original idex
        self.idx_out = np.copy(idx_bounds) # output idex
        self.facearray = ['w']*idx_bounds.shape[0] # color list
        self.bounds = 60 # surrounding region in seconds
        self.win = obj.win # window (defualt 5 seconds)  
        self.fs = obj.fs # samplin rate
        self.verpred_path = obj.verpred_path
        self.file_id = file_id
        
        # create first plot
        self.plot_data()
    
    @staticmethod
    def get_hours(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        str = '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))
        return (str)
        
        
    def save_idx(self):
           """
           Save user predictions to csv file as binary

           Returns
           -------
           None.

           """
           # pre allocate file with zeros
           ver_pred = np.zeros(self.data.shape[0])

   
           for i in range(self.idx_out.shape[0]): # assign index to 1
           
               if self.idx_out[i,0] > 0:
                   # add 1 to stop bound because of python indexing
                   ver_pred[self.idx_out[i,0]:self.idx_out[i,1]+1] = 1
               
           # save file
           np.savetxt(os.path.join(self.verpred_path,self.file_id), ver_pred, delimiter=',',fmt='%i')
           print('Verified predictions for ', self.file_id, ' were saved.\n')    
        
        
    def get_index(self):
        """
        get i, start and stop

        Returns
        -------
        None.

        """
        self.seg = round(self.bounds/self.win) # get surround time
        self.i = self.ind % self.idx.shape[0] # get index
        
        if self.idx_out[self.i,1] == -1: # if seizure rejected
            self.start = self.idx[self.i,0] # get start
            self.stop = self.idx[self.i,1] # get stop
        else: 
            self.start = self.idx_out[self.i,0] # get start
            self.stop = self.idx_out[self.i,1] # get stop
        
    def plot_data(self,**kwargs):
        """
        plot_data(self)
        plot self y and t and mark seizure

        """
        # get index, start and stop times
        self.get_index()
        
        # Plot seizure with nearby 1 minute segments
        y = self.data[self.start-self.seg : self.stop+self.seg,:].flatten()
        y1 = self.data1[self.start-self.seg : self.stop+self.seg,:].flatten()
        y2 = self.data2[self.start-self.seg : self.stop+self.seg,:].flatten()
        t = np.linspace(self.start-self.seg, self.stop+self.seg,len(y))

        # Plot seizure with surrounding region
        ax.clear();ax1.clear(); ax2.clear()# clear graph
        timestr = matplotGui.get_hours(self.start*self.win)
        timestr = '#' + str(self.i) + ' - '+ timestr
        ax.plot(t, y, color='k', linewidth=0.75, alpha=0.9, label= timestr) 
        ax.set_facecolor(self.facearray[self.i]);ax.legend(loc = 'upper right')
        ax1.plot(t, y1, color='gray', linewidth=0.75, alpha=0.9)
        ax2.plot(t, y2, color='gray', linewidth=0.75, alpha=0.9)
        
        ax.set_title('vHPC', loc ='left')
        ax1.set_title('Frontal', loc ='left')
        ax2.set_title('EMG', loc ='left')
        ax1.set_ylabel('Amp. (V)')
        ax2.set_xlabel('Time (Sec.)')
     
        # concatenate segments
        if 'usr_start' in kwargs: # plot user define
            start = kwargs['usr_start']; stop = kwargs['usr_stop']
        else: # plot model defined
            start = self.start; stop = self.stop
            
        y = self.data[start: stop,:].flatten()
        t = np.linspace(start, stop, len(y))
        # plot highlighted region
        ax.plot(t,y, color='orange', linewidth=0.75, alpha=0.9)
        fig.canvas.draw()
          
        
    ## ------ Mouse Button Press ------ ##   
    def forward(self, event):
        self.ind += 1 # add one to class index
        self.plot_data() # plot
        
    def previous(self, event):
        self.ind -= 1 # subtract one to class index
        self.plot_data() # plot
        
    def accept(self, event):
        self.facearray[self.i] = 'palegreen'
        ax.set_facecolor('palegreen')
        if self.idx_out[self.i,1] == -1:
            self.idx_out[self.i,:] = self.idx[self.i,:]
        else:
            self.idx_out[self.i,:] = self.idx_out[self.i,:]
        fig.canvas.draw()
        
    def reject(self, event):
        self.facearray[self.i] = 'salmon'
        ax.set_facecolor('salmon')
        self.idx_out[self.i,:] = -1
        fig.canvas.draw()
        
    def submit(self, text): # to move to a certain seizure number
        self.ind = eval(text)
        self.plot_data() # plot

             
    ## ------  Keyboard press ------ ##     
    def keypress(self,event):
        if event.key == 'right':
            self.ind += 1 # add one to class index
            self.plot_data() # plot
        if event.key == 'left':
            self.ind -= 1 # subtract one to class index
            self.plot_data() # plot
        if event.key == 'y':
            self.facearray[self.i] = 'palegreen'
            ax.set_facecolor('palegreen')
            if self.idx_out[self.i,1] == -1:
                self.idx_out[self.i,:] = self.idx[self.i,:]
            else:
                self.idx_out[self.i,:] = self.idx_out[self.i,:]
                fig.canvas.draw()
        if event.key == 'n':
            self.facearray[self.i] = 'salmon'
            ax.set_facecolor('salmon')
            self.idx_out[self.i,:] = -1  
            fig.canvas.draw()
        if event.key == 'enter': 
            plt.close()
            self.save_idx() # save file to csv
            print(self.idx_out)
            print(self.idx_out.shape[0]-np.sum(self.idx_out[:,0] == -1),'Seizures accepted.\n')
            
    ## ----- User Selection ----##        
    def onselect(self,xmin, xmax):
        """
        onselect(self,xmin, xmax)

        Parameters
        ----------
        xmin : Float
            Xmin-user selection.
        xmax : Float
            Xmax-user selection.

        """
               
        # find user segment index from plot
        indmin = int(xmin); indmax = int(xmax)
        
        # pass to index
        self.idx_out[self.i,0] = indmin
        self.idx_out[self.i,1] = indmax
        
        # highlight user selected region
        self.plot_data(usr_start = indmin, usr_stop = indmax)
        
    

























