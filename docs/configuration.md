
# Configuration settings

These setting in config.json

    - main_path : parent directory where your subfolders are present, e.g. "C:\\Users\\...\\parent folder"
    - org_rawpath : child folder name where .h5 data present, default is "reorganized_data"
    - rawpred_path : child folder name where raw predictions are present (.csv), default is "raw_predictions"
    - ver_path : child folder name where user verified predictions are present (.csv), default is "verified_predictions" 
    - ch_struct : List containing the names of LFP/EEG channels, e.g. ["vhpc", "pfc", "emg"]
    - ch_list : [0],
    - win : window size in seconds, for the current models needs to be 5
    - fs : sampling rate of .h5 files, for the current models needs to be 100
    - model_path : path to model that will generate predictions, set as -> "models\\cnn1D_3layer.h5"
---
