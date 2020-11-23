# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:18:28 2020

@author: Pante
"""       
               
### ------------------------ IMPORTS -------------------------------------- ###               
import os, sys, tables, json
import numpy as np
from keras.models import load_model
from tqdm import tqdm
### ------------------------------------------------------------------------###

              
class batchPredict:
    """
    Class for batch seizure prediction
    """
    
    # class constructor (data retrieval)
    def __init__(self):
        """
        class constructor (data retrieval from config.json)
        

        Returns
        -------
        None.

        """
        
        # load properties from configuration file
        jsonpath = 'config.json' 
        openpath = open(jsonpath, 'r').read(); 
        prop_dict = json.loads(openpath)
        
        # Get parent and re-oranized data path 
        self.gen_path = prop_dict['main_path']
        self.org_rawpath = os.path.join(self.gen_path , prop_dict['org_rawpath'])
        
        # Get predictions path
        self.rawpred_path = os.path.join(self.gen_path , prop_dict['rawpred_path'])
        
        # Get model path
        self.model_path = prop_dict['model_path']
        
        # get selected channel
        self.ch_list = prop_dict['ch_list']
        

    def mainfunc(self):
        """
        Iterate over files and generate predictions

        Returns
        -------
        None.

        """
        print ('\n----------------------------------------------------------------------')
        print ('-> Generating predictions from:', self.gen_path,'-----------------------')
        print ('----------------------------------------------------------------------\n')
        # make path
        if os.path.exists(self.rawpred_path) is False:
            os.mkdir( self.rawpred_path)
        
        # get file list
        filelist = list(filter(lambda k: '.h5' in k, os.listdir(self.rawpred_path )))
        
        # load model object to memory to get path
        model = load_model(self.model_path)
        
        breakpoint()
        
        # loop files (multilple channels per file)
        for i in tqdm(range(len(filelist)), desc = 'Progress', file=sys.stdout):
            
            # get organized data
            filepath = os.path.join(self.rawpred_path, filelist[i])
            f = tables.open_file(filepath, mode='r')
            data = f.root.data[:]
            f.close()
            
            # get data to right format
            data = data[:, :, self.ch_list].reshape((-1,-1,len(self.ch_list)))
            
            # get predictions (1D-array)
            ypred = model.predict(data) 
            
            # save predictions as .csv
            file_id = filelist[i].replace('.h5', '.csv')
            np.savetxt(os.path.join(self.rawpred_path,file_id), ypred, delimiter=',',fmt='%f')
            
        print ('\n----------------------------------------------------------------------')
        print ('----------------------- Predictions Completed ------------------------')
        print ('----------------------------------------------------------------------\n')
            
    
# Execute if module runs as main program
if __name__ == '__main__':
    
    # init object
    obj = batchPredict()
    
    # get predictions and store in csv
    obj.mainfunc()    
    
    
    
   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            