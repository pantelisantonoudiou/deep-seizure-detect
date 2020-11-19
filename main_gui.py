# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 12:27:27 2020

@author: panton01
"""
### ---------------------- IMPORTS ---------------------- ###
import json
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, SpanSelector, TextBox
from user_gui.user_verify import UserVerify
### ----------------------------------------------------- ###

if __name__ == '__main__' :
    
    # Load config file 
    try:
        config = open('config.json', 'r').read()
        config = json.loads(config)
    except Exception as err:
        raise FileNotFoundError(f"Unable to read the config file.\n{err}")
    
    # Get variables from config dictionary
    input_path = config['main_path']

    # Create instance
    obj = UserVerify(input_path)
    file_id = obj.select_file() # user file selection
    data, idx_bounds = obj.main_func(file_id) # get data and seizure index
    
    if idx_bounds is not False:
        if idx_bounds.shape[0] == 0: # check for zero seizures
            obj.save_emptyidx(data.shape[0],file_id)
            
        else: # otherwise proceed with gui creation
    
            # get gui
            from user_gui.verify_gui import matplotGui,fig,ax
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