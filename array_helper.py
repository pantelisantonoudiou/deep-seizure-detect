# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:05:34 2020

@author: panton01
"""
import numpy as np
from numba import jit
from scipy import signal

def find_nearest(array,value,**kwargs):
    """
    idx = find_nearest(array,value,**kwargs)
    idx = find_nearest(a,2,start = 1,order = 1)
    
    Parameters
    ----------
    array : list/numpy array
    value : int/float
        value to be found.
    **kwargs : TYPE
    START = starting index
    ORDER : 1, search forwards
          :-1, search reverse

    Returns
    -------
    index
    """ 
    # Ensure variable is defined
    try:
        kwargs['start']
    except KeyError:
        kwargs['start'] = 1
  
    try:
        kwargs['order']
    except KeyError:
         kwargs['order'] = 1
    

    if kwargs['order'] == 1:     
        for i in range(kwargs['start'],len(array)):
            if array[i] == value:
                return int(i)
            
    elif kwargs['order'] == -1:
        for i in range(kwargs['start'],-1,-1):
            if array[i] == value:
                return int(i)
            
@jit(nopython=True)               
def remove_zeros(ref_pred, pred_array,bounds):
    """   
    ref_pred = remove_zeros(ref_pred, pred_array,bounds)    
    
    Parameters
    ----------
    ref_pred : ndarray, boolean array
    pred_array : ndarray, boolean array
    bounds : TYPE

    Returns
    -------
    ref_pred : NUMPY ARRAY (szr_n,2), neighbor threshold

    """
    # remove neighbours that have zeros
    for i in range(bounds[0], pred_array.shape[0] - bounds[1]):
        if np.sum(pred_array[i-bounds[0]:i+bounds[1]+1]) != np.sum(bounds)+1:
            ref_pred[i] = 0
    return ref_pred
            
         
def find_szr_idx(pred_array,bounds):
    """
    idx_bounds = find_szr_idx(pred_array,bounds)
    idx_bounds = find_szr_idx(rawpred, [2,2])
    
    Parameters
    ----------
    pred_array : ndarray, boolean array
    bounds: two element list, denoting neighbours bounds 
       
    Returns
    -------
    idx_bounds : NUMPY ARRAY (szr_n,2)
        index bounds for seizures.
    
    """
    
    # make a copy of the array
    ref_pred = np.copy(pred_array)
    
    # get min peak distance
    distance = 1
    
    if np.sum(bounds) > 0:
        distance = sum(bounds) 
        # remove zeros
        ref_pred = remove_zeros(ref_pred, pred_array,bounds)
    
    # make the first segments zero
    ref_pred[0:1] = 0
    
    # get signal peaks        
    idx = signal.find_peaks(ref_pred,height = 1, distance = distance)[0]
  
    # get index bounds
    idx_bounds = np.zeros([len(idx),2],dtype=int)
   
    for i in range(len(idx)):
        idx_bounds[i,0] = find_nearest(ref_pred,0,start = idx[i],order = -1) + 1
        idx_bounds[i,1] = find_nearest(ref_pred,0,start = idx[i],order = 1) - 1
        
    # recreate original boundaries that were trimmed
    idx_bounds[:,0] -= bounds[0]
    idx_bounds[:,1] += bounds[1]
    idx_bounds[idx_bounds < 0] = 0 # replace with zero
    
    return idx_bounds


def merge_close(bounds, merge_margin = 5):
    """
    merge_close(bounds, merge_margin = 5)

    Parameters
    ----------
    bounds : 2D ndarray (rows = seizure segments, columns =[start,stop])
    merge_margin : Int, optional

    Returns
    -------
    bounds_out : 2D ndarray, merged array (rows = seizure segments, columns =[start,stop])

    """
    
    if bounds.shape[0] < 2: # if less than two seizures exit
        return bounds
    
    # copy of bounds
    bounds_out = np.copy(bounds) 
    
    # create delta array
    delta = np.zeros(bounds.shape[0]-1); delta = delta.astype(np.int64)
    for i in range(bounds.shape[0]-1):  
        delta[i] = bounds[i+1,0]-bounds[i,1]
   
    # get merged index
    merge_idx = delta < merge_margin; # find indices separated by less than merge_margin
    
    # padd with zeros for peak detection
    merge_idx = np.insert(merge_idx,0,False)# add one false to allow peak detection at zero index
    merge_idx = np.insert(merge_idx,merge_idx.shape[0],False)# add one false to allow peak detection at zero index
    merge_idx = find_szr_idx(merge_idx,[0,0]); # get index of merged segments 
    merge_idx -= 1 # (-1 for false addition at 0 element)
    
    # make a copy and leave unchanged, index for original array
    idx = np.copy(merge_idx)

    for i in range(merge_idx.shape[0]): # loop though index
        low = merge_idx[i,0]; upper = merge_idx[i,1] # get upper and lower boundaries
        bounds_out[ merge_idx[i,0],:] = [bounds[idx[i,0],0], bounds[idx[i,1],1]] # replace merged  
        rmv_idx = np.linspace(low, upper, np.int(upper-low)+1) # get removal index
        rmv_idx = np.delete(rmv_idx,0).astype(np.int64) # remove first element and convert to int
        bounds_out = np.delete(bounds_out, rmv_idx , axis=0) # delete next element
        merge_idx -= rmv_idx.shape[0] # remove one from index because of deleted element 
        
    return bounds_out
        

# find matching seizures     
@jit(nopython=True) 
def match_szrs(idx_true, idx_pred, err_margin = 5):
    """
    match_szrs(idx_true,idx_pred, err_margin)

    Parameters
    ----------
    idx_true : Bool, ndarray, User defined (ground truth) boolean index
    idx_pred : Bool, ndarray, Predicted index
    err_margin : Int, optional, Default values = 5.

    Returns
    -------
    matching : Int, number of matching seizures

    """
    matching = 0 # number of matching seizures
    
    for i in range(idx_true.shape[0]):
        
        # does min bound match within error margin?
        min_bound = np.any(np.abs(np.subtract(idx_true[i,0],idx_pred[:,0]))<err_margin)
        
        # does max bound match within error margin?
        max_bound  = np.any(np.abs(np.subtract(idx_true[i,1],idx_pred[:,1]))<err_margin)
        
        # do both bounds match?
        if max_bound is True & min_bound is True:
            matching += 1
            
    return matching

# find matching seizures method 2 with index 
@jit(nopython=True) 
def match_szrs_idx(idx_true, y_pred):
    """
    find index of matching seizures
    
    Parameters
    ----------
    idx_true : np.array, index of true seizures  
    y_pred : np.array, binary predictions of model
    
    Returns
    -------
    idx, containing ones or zeros
    
    """
    # create empty vector
    idx = np.zeros(idx_true.shape[0])
    
    for i in range(idx_true.shape[0]):
        
        # get predictions in seizure range
        pred = y_pred[idx_true[i,0]:idx_true[i,1]+1]
        
        # get sum of continous predictions > more than 10 seconds
        sum_continous_segments = np.sum(remove_zeros(pred.copy(), pred, np.array([0,1])))    
        
        # pass to index array
        idx[i] = sum_continous_segments
 
    return idx > 0 # convert to logic


@jit(nopython=True)  
def binvector_from_index(idx, length):
    """
    Get a binary vector from index numpy array
    
    Parameters
    ----------
    idx : 2d-Numpy array, Seizure index (rows = seizures, columns = [start, end index])
    length : Int, Seizure vector length
    
    Returns
    -------
    pred : 1d- Numpy array
    """

    # pre allocate file with zeros
    pred = np.zeros(length)
    for i in range(idx.shape[0]): # assign index to 1
        pred[idx[i,0]:idx[i,1]+1] = 1
    return  pred
























            
            


