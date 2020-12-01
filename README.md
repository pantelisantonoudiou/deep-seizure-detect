# deep-seizure-detect
:snake: Semi-automated batch seizure detection using deep learning. 

-> Check out the online [version](https://github.com/matteocargnelutti/maguire-lab-seizure-detection-webapp) :zap: developed by [@matteocargnelutti](https://github.com/matteocargnelutti).

---
## How to install
1) Download and install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your platform
2) Clone or Download [deep-seizure-detect](https://github.com/pantelisantonoudiou/deep-seizure-detect)
3) Start Anaconda's shell prompt, navigate to */deep-seizure-detect*:

        # create conda environment with python version 3.7.7
        conda create --name myenv python=3.7.7     
        
        # enter conda environment
        conda activate myenv
        
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
        
---

## How to use

Start Anaconda's shell prompt
        
        # navigate to *deep-seizure-detect* folder
        cd ./deep-seizure-detect

        # enter conda environment
        conda activate myenv

        # Get path of the folder containing reorganized_data subfolder with data to generate predictions       
        python get_path.py
        
        # generate predictions
        python batch_predict.py
        
        # verify seizures
        python app.py
        
<img src="docs/app-UI.png" width="500">

---        
## Configuration settings and file preparation
For configuration settings and file preparation check this guide -> [configuration](docs/configuration.md)

---
## About the model
The model is a convolutional neural net that was built using [Keras](https://keras.io/) API with a Tensorflow-backend. It was trained on LFP data from
chronically epileptic mice that were generated using intra-hippocampal kainate injections by [Dr. Trina Basu](https://twitter.com/trina_basu).
 
---
## Development
deep-seizure-detect was developed by [Pantelis Antonoudiou](https://github.com/pantelisantonoudiou).
This open-source software is distributed under [the Apache 2.0 License](/LICENSE).
        
        
        
        
        
        
        
        
