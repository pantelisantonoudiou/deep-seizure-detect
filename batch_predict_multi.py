# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:18:28 2020

@author: Pante
"""


##    >>>>>>>>> USER INPUT <<<<<<<<          ##
# Add path to raw data folder in following format -> r'PATH'
input_path = r'C:\Users\panton01\Desktop\Trina-seizures\3642_3641_3560_3514\raw_data'

# Add path to model
model_path = r'models\cnn3.h5'

               ## ---<<<<<<<< ##              
               
### ------------------------ IMPORTS -------------------------------------- ###               
import os, tables, json
import numpy as np
from keras.models import load_model
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
from multich_dataPrep import lab2mat
from path_helper import sep_dir
### ------------------------------------------------------------------------###

              
class batchPredict:
    """
    Class for batch seizure prediction
    """
    
    # class constructor (data retrieval)
    def __init__(self, input_path):
        """
        lab2mat(main_path)

        Parameters
        ----------
        input_path : STRING
            Raw data path.

        """
        # pass input path
        self.input_path = input_path

        # Get general and inner paths
        self.gen_path, innerpath = sep_dir(input_path,1)
        
        # load object properties as dict
        jsonfile = 'organized.json'
        obj_props = lab2mat.load(os.path.join(self.gen_path, jsonfile))
        self.org_rawpath = obj_props['org_rawpath']
        
        # create raw pred path
        rawpred_path = 'raw_predictions'
        obj_props.update({'rawpred_path' : rawpred_path})
        self.rawpred_path = os.path.join(self.gen_path, rawpred_path)
        
        # write attributes to json file using a dict
        jsonpath = os.path.join(self.gen_path, jsonfile)
        open(jsonpath, 'w').write(json.dumps(obj_props))


    def mainfunc(self,model_path):
        """
        mainfunc(input_path,model_path,ch_sel)
    
        Parameters
        ----------
        input_path : String
            Path to raw data.
        model_path : String
            Path to model.
    
        """
        
       
        # make path
        if os.path.exists( self.rawpred_path) is False:
            os.mkdir( self.rawpred_path)
        
        # get file list
        mainpath = os.path.join(self.gen_path, self.org_rawpath)
        filelist = list(filter(lambda k: '.h5' in k, os.listdir(mainpath)))
        
        # load model object to memory to get path
        model = load_model(model_path)
        
        
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
    obj = batchPredict(input_path)
    
    # get predictions in binary format and store in csv
    obj.mainfunc(model_path)    
    
    
    
   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            