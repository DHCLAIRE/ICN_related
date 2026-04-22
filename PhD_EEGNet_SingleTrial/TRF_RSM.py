#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path
import re
import matplotlib.pyplot as plt
from matplotlib import pyplot
import eelbrain
import mne
#import trftools

from pprint import pprint
import numpy as np

if __name__ == "__main__":
    STIMULI = [str(i) for i in range(1, 13)]
    DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    Native_SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'S\d*', path.name)]
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR.mkdir(exist_ok=True)
    print(Native_SUBJECTS)
    print(len(Native_SUBJECTS))
    
    
    ##Step 1: Load in the TRF .pickle files so that later the RSM of each timpoint can be extracted.
    
    n_rowsLIST = []
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        trf = eelbrain.load.unpickle(TRF_DIR / Path('S%.2d/S%.2d envelope.pickle'%(int(subj[1:3]), int(subj[1:3]))))
        #print(trf.h[0])
        #print(trf.h_scaled)
        print(trf.x_mean)
        n_rowsLIST.append([n_subj, trf.proportion_explained, trf.h[0]])#.abs()])
        
    ##Step 2: Get the channels by timepoint matrix from TRF
    
    ##Step 3: Transpose the data from channels(rows) by timepoints(col) into timepoints(rows) by channels(col)
    # Below are unchange Gemini codes
    # Transpose the data to shape: (150 timepoints, 64 channels)
    X = trf_data.T 
    
    print(f"Shape for RSA: {X.shape} (Timepoints, Channels)")
    
    ##Step 4: Compute the RSM
    # Compute the correlation matrix between all time points
    # The resulting shape will be (n_timepoints, n_timepoints)
    similarity_matrix = np.corrcoef(X)
    
    # Alternatively, if you want a Dissimilarity Matrix (RDM):
    # dissimilarity_matrix = 1 - similarity_matrix
    
    print(f"RSM Shape: {similarity_matrix.shape}")
    
    ##Step 5: Visualize the RSM
    # Set up the plot
    plt.figure(figsize=(8, 6))
    
    # Plot the RSM using seaborn for a nice heatmap
    sns.heatmap(similarity_matrix, 
                cmap='RdBu_r',       # Red-Blue colormap (standard for correlations)
                center=0,            # Center the colormap at 0 correlation
                vmin=-1, vmax=1,     # Correlations range from -1 to 1
                square=True,         # Make the cells square
                cbar_kws={'label': "Pearson Correlation (r)"})
    
    # Add labels and title
    plt.title("TRF Representational Similarity Matrix (RSM)")
    plt.xlabel("Time Point (lag)")
    plt.ylabel("Time Point (lag)")
    
    # Invert Y axis so time 0 starts at the top left (standard practice)
    plt.gca().invert_yaxis()
    
    #plt.show()
    #(change it into) plt.save!!!
    