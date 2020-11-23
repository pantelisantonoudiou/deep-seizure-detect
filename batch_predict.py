# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:18:28 2020

@author: Pante
"""


# Add path to model
model_path = r'models\cnn3.h5'

               ## ---<<<<<<<< ##              
               
### ------------------------ IMPORTS -------------------------------------- ###               
import os, tables, json
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
        # class constructor (data retrieval from config.json)
        

        Returns
        -------
        None.

        """
        
        # load properties from configuration file
        jsonpath = os.path.join(self.gen_path, 'config.json') 
        openpath = open(jsonpath, 'r').read(); 
        obj_props = json.loads(openpath)
        
        # Get parent and re-oranized data path 
        self.gen_path = obj_props['main_path']
        self.org_rawpath = os.path.join(self.gen_path , obj_props['org_rawpath'])
        
        # Get model path
        self.model_path = os.path.join(self.gen_path , obj_props['model_path'])
        
        # sel channel
        self.channel_sel
        

    def mainfunc(self):
        """


        """
        
       
        # make path
        if os.path.exists(self.rawpred_path) is False:
            os.mkdir( self.rawpred_path)
        
        # get file list
        mainpath = os.path.join(self.gen_path, self.org_rawpath)
        filelist = list(filter(lambda k: '.h5' in k, os.listdir(mainpath)))
        
        # load model object to memory to get path
        model = load_model(self.model_path)
        
        
        # loop files (multilple channels per file)
        for i in tqdm(range(len(filelist))):
            
            # get organized data
            filepath = os.path.join(mainpath, filelist[i])
            f = tables.open_file(filepath, mode='r')
            data = f.root.data[:]
            f.close()
            
            # get predictions (1D-array)
            binpred = self.get_predictions(data,model)
            
            # save predictions as .csv
            file_id = filelist[i].replace('.h5', '.csv')
            np.savetxt(os.path.join(self.rawpred_path,file_id), binpred, delimiter=',',fmt='%i')
            
            
    def get_predictions(self,data,model):
        """
        get_predictions(data,model,ch_sel)
    
        Parameters
        ----------
        data : Numpy array
    
        model : keras model
    
        ch_sel : List
            Containing selected channels.
    
        Returns
        -------
        binpred : Numpy array (rows = segments, columns = channels)
        Model binary predictions

        """
        # init array
        binpred = np.zeros(data.shape[0], dtype = int)
        
        # get predictions    
        pred = model.predict(data) 
        
        # convert to binary predictions
        binpred = np.argmax(pred, axis = 1) 
      
        return binpred # return predictions
        
            
# Execute if module runs as main program
if __name__ == '__main__':
    
    # init object
    obj = batchPredict()
    
    # get predictions in binary format and store in csv
    obj.mainfunc()    
    
    
    
   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            