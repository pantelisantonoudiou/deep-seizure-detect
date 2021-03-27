# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 12:27:27 2020

@author: panton01
"""
### ---------------------- IMPORTS ---------------------- ###
import json
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from user_gui.user_verify import UserVerify
### ----------------------------------------------------- ###

if __name__ == '__main__' :
    
    # Load config file 
    try:
        # load object properties as dict
        jsonpath = 'config.json' # name of dictionary where propeties are stored
        openpath = open(jsonpath, 'r').read(); 
        prop_dict = json.loads(openpath)
    except Exception as err:
        raise FileNotFoundError(f"Unable to read the config file.\n{err}")

    # Create instance for UserVerify class
    obj = UserVerify(prop_dict)
    file_id = obj.select_file() # user file selection
    data, idx_bounds = obj.main_func(file_id) # get data and seizure index
    
    if idx_bounds is not False:
        if idx_bounds.shape[0] == 0: # check for zero seizures
            obj.save_emptyidx(data.shape[0],file_id)
            
        else: # otherwise proceed with gui creation
    
            # get gui
            from user_gui.verify_gui import matplotGui
               
            # init gui object
            callback = matplotGui(data, idx_bounds, obj, file_id)
            plt.subplots_adjust(bottom=0.15) # create space for buttons
            
            # add title and labels
            callback.fig.suptitle('To Submit Press Enter; To Select Drag Mouse Pointer : '+file_id, fontsize=12)        # title
            callback.fig.text(0.5, 0.09,'Time Bins (' + str(prop_dict['win']) + ' Sec.)', ha="center")                                                     # xlabel
            callback.fig.text(.02, .5, 'Amp. (V)', ha='center', va='center', rotation='vertical')                       # ylabel
            callback.fig.text(0.9, 0.04,'** KEY = Previous : <-, Next: ->, Accept: Y, Reject: N **' ,                   # move/accept labels
                              ha="right", bbox=dict(boxstyle="square", ec=(1., 1., 1.), fc=(0.9, 0.9, 0.9),))              
                                                            
            # add key press
            idx_out = callback.fig.canvas.mpl_connect('key_press_event', callback.keypress)
            
            # set useblit True on gtkagg for enhanced performance
            span = SpanSelector(callback.axs[0], callback.onselect, 'horizontal', useblit=True,
                rectprops=dict(alpha=0.5, facecolor='red'))
            plt.show()