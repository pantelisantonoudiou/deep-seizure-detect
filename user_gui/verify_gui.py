# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:37:05 2020

@author: panton01
"""

### ---------------------- IMPORTS ---------------------- ###
import os
import numpy as np
import matplotlib.pyplot as plt
### ----------------------------------------------------- ###

# # create figure and axis
# fig, axs = plt.subplots(3,1,sharex = True, figsize=(8,8))
# plt.subplots_adjust(bottom=0.2) # create space for buttons
# fig.text(0.5,0.04,'Time (Sec.)', ha="center")
# fig.text(.05, .5, 'Amp. (V)', ha='center', va='center', rotation='vertical')

# # remove all axes except left 
# for i in range(axs.shape[0]): 
#     axs[i].spines["top"].set_visible(False)
#     axs[i].spines["right"].set_visible(False)
#     axs[i].spines["bottom"].set_visible(False)

class matplotGui(object):
    """
        Matplotlib GUI for user seizure verification.
    """
    
    ind = 0 # set internal counter
       
    def __init__(self, data, idx_bounds, obj, file_id):
        """   
        Parameters
        ----------
        data : 3D Numpy array, (1D = seizure segments, 2D =  columns (samples: window*sampling rate), 3D = channels ) 
        idx_bounds : 2D Numpy array (1D = seizure segments, 2D, 1 = start, 2 = stop index)
        obj: UserVerify object
        file_id: Str, file anme

        """
        
        # pass object attributes to class
        self.data = data                                        # data
        self.idx = np.copy(idx_bounds)                          # original index from model
        self.idx_out = np.copy(idx_bounds)                      # output index
        self.facearray = ['w']*idx_bounds.shape[0]              # color list
        self.bounds = 60                                        # surrounding region in seconds
        self.win = obj.win                                      # window (default 5 seconds)  
        self.fs = obj.fs                                        # sampling rate
        self.verpred_path = obj.verpred_path                    # path to store verified predictions
        self.file_id = file_id                                  # file id
        self.ch_list = ['vHPC','FC', 'EMG']
        
        # create figure and axis
        self.fig, self.axs = plt.subplots(data.shape[2], 1, sharex = True, figsize=(9,9))
        plt.subplots_adjust(bottom=0.2) # create space for buttons
        self.fig.text(0.5,0.04,'Time (Sec.)', ha="center")
        self.fig.text(.1, .5, 'Amp. (V)', ha='center', va='center', rotation='vertical')
        
        # remove all axes except left 
        for i in range(self.axs.shape[0]): 
            self.axs[i].spines["top"].set_visible(False)
            self.axs[i].spines["right"].set_visible(False)
            self.axs[i].spines["bottom"].set_visible(False)
            
        # create first plot
        self.plot_data()
    
    @staticmethod
    def get_hours(seconds):
        """

        Parameters
        ----------
        seconds : Int

        Returns
        -------
        str : Str

        """
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
            self.stop = self.idx[self.i,1]+1 # get stop
        else: 
            self.start = self.idx_out[self.i,0] # get start
            self.stop = self.idx_out[self.i,1]+1  # get stop
        
        
    def plot_data(self, **kwargs):
        """
        plot_data(self)
        plot self y and t and mark seizure

        """
        # get index, start and stop times
        self.get_index()
        
        # get seizure time
        timestr = matplotGui.get_hours(self.start*self.win)
        timestr = '#' + str(self.i) + ' - '+ timestr
        
        # Get boundaries for highlighted region
        if 'usr_start' in kwargs:   # plot user define
            start = kwargs['usr_start']; stop = kwargs['usr_stop']
        else:                       # plot model defined
            start = self.start; stop = self.stop
        
        ###  PLot first channel first with different settings  ###   
        # get seizure with nearby segments
        i = 0  # first channel
        y = self.data[self.start - self.seg : self.stop + self.seg,:, i].flatten()
        t = np.linspace(self.start - self.seg, self.stop + self.seg, len(y)) # get time
        self.axs[i].clear() # clear graph
        self.axs[i].plot(t, y, color='k', linewidth=0.75, alpha=0.9, label= timestr) 
        self.axs[i].set_facecolor(self.facearray[self.i]);
        self.axs[i].legend(loc = 'upper right')
        self.axs[i].set_title(self.ch_list[i], loc ='left')
                 
        # plot remaining channels    
        for i in range(1, self.axs.shape[0]): 
            # Plot seizure with surrounding region
            y = self.data[self.start - self.seg : self.stop + self.seg,:, i].flatten()
            self.axs[i].clear() # clear graph
            self.axs[i].plot(t, y, color='gray', linewidth=0.75, alpha=0.9)
            self.axs[i].set_title(self.ch_list[i], loc ='left') # plot channel title
            
        ###  Plot highlighted region  ###
        i = 0  # first channel
        y = self.data[start: stop,:,i].flatten() # get y values of highlighted region
        t = np.linspace(start, stop, len(y)) # get time of highlighted region
        self.axs[i].plot(t, y, color='orange', linewidth=0.75, alpha=0.9) # plot
        self.fig.canvas.draw() # draw


    ## ------ Mouse Button Press ------ ##   
    def forward(self, event):
        self.ind += 1 # add one to class index
        self.plot_data() # plot
        
    def previous(self, event):
        self.ind -= 1 # subtract one to class index
        self.plot_data() # plot
        
    def accept(self, event):
        self.facearray[self.i] = 'palegreen'
        self.axs[0].set_facecolor('palegreen')
        if self.idx_out[self.i,1] == -1:
            self.idx_out[self.i,:] = self.idx[self.i,:]
        else:
            self.idx_out[self.i,:] = self.idx_out[self.i,:]
        self.fig.canvas.draw()
        
    def reject(self, event):
        self.facearray[self.i] = 'salmon'
        self.axs[0].set_facecolor('salmon')
        self.idx_out[self.i,:] = -1
        self.fig.canvas.draw()
        
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
            self.axs[0].set_facecolor('palegreen')
            if self.idx_out[self.i,1] == -1:
                self.idx_out[self.i,:] = self.idx[self.i,:]
            else:
                self.idx_out[self.i,:] = self.idx_out[self.i,:]
                self.fig.canvas.draw()
        if event.key == 'n':
            self.facearray[self.i] = 'salmon'
            self.axs[0].set_facecolor('salmon')
            self.idx_out[self.i,:] = -1  
            self.fig.canvas.draw()
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
        
    

























