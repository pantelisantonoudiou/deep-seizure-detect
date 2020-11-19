# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:10:48 2020

@author: panton01
"""

### -------- IMPORTS ---------- ###
import os, sys, json, tables
from pick import pick
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, SpanSelector, TextBox
# User Defined
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if ( os.path.join(parent_path,'helper') in sys.path) == False:
    sys.path.extend([parent_path, os.path.join(parent_path,'helper'),
                     os.path.join(parent_path,'data_preparation')])
from array_helper import find_szr_idx
### ------------------------------------------ ####

       
class UserVerify:
    """
    Class for User verification of detected seizures.
    
    """
    
    # class constructor (data retrieval)
    def __init__(self, input_path):
        """
        lab2mat(main_path)

        Parameters
        ----------
        input_path : Str, Path to raw data.

        """
        # pass general path (parent)
        self.gen_path = input_path
        
        # load object properties as dict
        jsonpath = os.path.join(self.gen_path, 'organized.json') # name of dictionary where propeties are stored
        openpath = open(jsonpath, 'r').read(); obj_props = json.loads(openpath)
        
        # get data path
        self.org_rawpath = os.path.join(self.gen_path, obj_props['org_rawpath'])
        
        # get raw prediction path
        self.rawpred_path = os.path.join(self.gen_path, obj_props['rawpred_path'])
        
        # create user verified path
        verpred_path = 'verified_predictions'
        obj_props.update({'verpred_path' : verpred_path})
        self.verpred_path = os.path.join(self.gen_path, verpred_path)
        
        # write attributes to json file using a dict
        open(jsonpath, 'w').write(json.dumps(obj_props))
        
        # make path if it doesn't exist
        if os.path.exists( self.verpred_path) is False:
            os.mkdir( self.verpred_path)

        # get sampling rate
        self.fs = round(obj_props['fs'] / obj_props['down_factor'])
        
        # get win in seconds
        self.win = obj_props['win']
   
        
    def select_file(self):
        """
        select_file(self)
        
        Returns
        -------
        option : Str, selection of file id

        """
       
        # get all files in raw predictions folder 
        rawpredlist = list(filter(lambda k: '.csv' in k, os.listdir(self.rawpred_path)))
       
        # get all files in user verified predictions
        verpredlist = list(filter(lambda k: '.csv' in k, os.listdir(self.verpred_path)))
       
        # get unique list
        not_analyzed_filelist = list(set(rawpredlist) - set(verpredlist))
        
        # remaining filelist
        analyzed_filelist = list(set(rawpredlist) - set(not_analyzed_filelist))
        
        # filelist
        filelist = [' *** ' + s for s in analyzed_filelist] +  not_analyzed_filelist           
        
        # select from command list
        title = 'Please select file for analysis: '
        option, index = pick(filelist, title, indicator = '-> ')
        return option.replace(' *** ','')


    def main_func(self, file_id):
        """
        main_func(self, file_id)

        Parameters
        ----------
        file_id : String

        Returns
        -------
        data : 3d Numpy Array (1D = segments, 2D = time, 3D = channel)
        idx_bounds : 2D Numpy Array (rows = seizures, cols = start and end points of detected seizures)

        """
        
        print('-> File being analyzed: ', file_id,'\n')

        # Get predictions
        pred_path = os.path.join(self.rawpred_path, file_id) # get path
        bin_pred = np.loadtxt(pred_path, delimiter=',', skiprows=0) # get predictions
        idx_bounds = find_szr_idx(bin_pred, np.array([0,1])) # find seizure oundaries
           
        # load raw data for visualization
        data_path = os.path.join(self.org_rawpath, file_id.replace('.csv','.h5'))
        f = tables.open_file(data_path, mode='r')
        data = f.root.data[:]
        f.close()
        
        # check whether to continue
        print('>>>>',idx_bounds.shape[0] ,'seizures detected')
        
        return data, idx_bounds
               
    def save_emptyidx(self, data_len,file_id):
         """
         Save user predictions to csv file as binary
        
         Returns
         -------
         None.
        
         """
         # pre allocate file with zeros
         ver_pred = np.zeros(data_len)
         
         # save file
         np.savetxt(os.path.join(self.verpred_path, file_id), ver_pred, delimiter=',',fmt='%i')
         print('Verified predictions for ', file_id, ' were saved\n')
         
     
# Execute if module runs as main program
if __name__ == '__main__' :
    
    # ------>>>>> USER INPUT <<<<<< --------------
    input_path = r'C:\Users\panton01\Desktop\08-August\5394_5388_5390_5391'
    # file_id = '082820_5390a.csv'
    # -------<<<<<<<<<<
    
    # create instance
    obj = UserVerify(input_path)
    file_id = obj.select_file() # user file selection
    data, idx_bounds = obj.main_func(file_id) # get data and seizure index
    
    if idx_bounds is not False:
        
        if idx_bounds.shape[0] == 0: # check for zero seizures
            obj.save_emptyidx(data.shape[0],file_id)
            
        else: # otherwise proceed with gui creation
    
            # get gui
            from verify_gui import matplotGui,fig,ax
            fig.suptitle('To Submit Press Enter; To Select Drag Mouse Pointer : '+file_id, fontsize=12)
               
            # init object
            callback = matplotGui(data,idx_bounds,obj, file_id)
            
            # add buttons
            axprev = plt.axes([0.625, 0.05, 0.13, 0.075]) # previous
            bprev = Button(axprev, 'Previous: <')
            bprev.on_clicked(callback.previous)
            axnext = plt.axes([0.765, 0.05, 0.13, 0.075]) # next
            bnext = Button(axnext, 'Next: >')
            bnext.on_clicked(callback.forward)
            axaccept = plt.axes([0.125, 0.05, 0.13, 0.075]) # accept
            baccept = Button(axaccept, 'Accept: y')
            baccept.on_clicked(callback.accept)
            axreject = plt.axes([0.265, 0.05, 0.13, 0.075]) # reject
            breject = Button(axreject, 'Reject: n')
            breject.on_clicked(callback.reject)
            axbox = plt.axes([0.5, 0.055, 0.05, 0.05]) # seizure number
            text_box = TextBox(axbox, 'Szr #', initial='0')
            text_box.on_submit(callback.submit)
            
            # add key press
            idx_out = fig.canvas.mpl_connect('key_press_event', callback.keypress)
            
            # set useblit True on gtkagg for enhanced performance
            span = SpanSelector(ax, callback.onselect, 'horizontal', useblit=True,
                rectprops=dict(alpha=0.5, facecolor='red'))
            plt.show()
    
    

       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        