# deep-seizure-detect
Offline semi-automated seizure detection using deep learning

<img src="docs/app-UI.svg" width="500">

---
## How to Install
1) Download and Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your platform
2) Clone or Download [deep-seizure-detect](https://github.com/pantelisantonoudiou/deep-seizure-detect)
3) Start Anaconda prompt, navigate to */deep-seizure-detect* and execute:

        # create conda environment with python version 3.7.7
        conda create --name test python=3.7.7     
        
        # example creation of conda environment *deeplearn*
        conda create --name deeplearn --file requirements.txt
        
        # install dependencies
        conda install -c anaconda keras
        conda install -c anaconda scikit-learn
        conda install -c anaconda matplotlib
        conda install -c anaconda seaborn
        conda install -c anaconda numba
        conda install -c anaconda tqdm
        pip install tables
        pip install pick
        
        # optional for gpu usage
        conda install tensorflow-gpu
