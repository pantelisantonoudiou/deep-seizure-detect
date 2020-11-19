# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 13:04:58 2020

@author: panton01
"""

### ------------------- Imports ------------------- ###
import os, json
### ----------------------------------------------- ###

# get configuration file name
conf_file = 'config.json'

def main_func():
    """
    Get path and save settings from user

    Returns
    -------
    bool, False if operation fails.

    """
    # get user input
    path = input('Enter Path for analysis: \n')
    
    # check if path exists
    if os.path.isdir(path) == 0: # if path exists
        print('\n************ The input', '"'+ path +'"' ,'is not a valid path. Please try again ************\n')
        return False
    
    # pass current experiment path to config file 
    try:
        # Load config file and update with current experiment path 
        property_dict = open(conf_file, 'r').read() # get json to memory
        property_dict = json.loads(property_dict) # parse json to dict
        property_dict['main_path'] = path # update dict with path
        open(conf_file, 'w').write(json.dumps(property_dict)) # save dict to json
    except Exception as err:
        print('Unable to write the config file.\n',err)

    print('\n------> Settings saved to config.json <------\n')
    
# Execute if module runs as main program
if __name__ == '__main__' :
    main_func() # run function 