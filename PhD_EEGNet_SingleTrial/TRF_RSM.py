#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path
import re
import matplotlib.pyplot as plt
from matplotlib import pyplot
import eelbrain
import mne
#import trftools
import seaborn as sns

from pprint import pprint
import numpy as np

if __name__ == "__main__":
    STIMULI = [str(i) for i in range(1, 13)]
    """
    ## Alice_Natives ##
    DATA_ROOT = Path("/Volumes/DH_4GB/Neurolang_1_Copy(ver20231203)/Master Program/New_Thesis_topic/Experiments_Results")#("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    Native_SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'S\d*', path.name)]
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR.mkdir(exist_ok=True)
    DST = TRF_DIR / 'Natives_figures'
    DST.mkdir(exist_ok=True)
    print(Native_SUBJECTS)
    print(len(Native_SUBJECTS))
    
    ##Step 1: Load in the TRF .pickle files so that later the RSM of each timpoint can be extracted.
    n_rowsLIST = []
    all_subj_rsms = []
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        trf = eelbrain.load.unpickle(TRF_DIR / Path('S%.2d/S%.2d envelope.pickle'%(int(subj[1:3]), int(subj[1:3]))))
        #print(trf.h[0])
        #print(trf.h_scaled)
        #print(trf.x_mean)
        #n_rowsLIST.append([n_subj, trf.proportion_explained, trf.h[0]])#.abs()])
        
        # 2. Extract the NDVar for the envelope predictor
        trf_ndvar = trf.h[0] 
        
        # 3. Extract the NumPy array for the RSM
        # By specifying dims=('time', 'sensor'), Eelbrain returns an array of shape (timepoints, channels).
        # This becomes our 'X' matrix directly.
        X = trf_ndvar.get_data(dims=('time', 'sensor'))
        
        # 4. Compute the RSM (Pearson correlation across time points)
        # np.corrcoef expects variables as rows, so X needs to be (time, sensors)
        similarity_matrix = np.corrcoef(X)
        
        # Save the Subject ID, proportion explained, and the computed RSM
        n_rowsLIST.append([n_subj, trf.proportion_explained, similarity_matrix])
        all_subj_rsms.append(similarity_matrix)
        
        print(f"Subject {n_subj}: RSM computed with shape {similarity_matrix.shape}")
        
        # Optional: Convert the list of RSMs to a 3D numpy array (Subjects x Time x Time)
        # This is highly useful for computing the grand average RSM across your group
        group_rsm_array = np.array(all_subj_rsms)
        grand_average_rsm = np.mean(group_rsm_array, axis=0)
        
        ##Step 5: Visualize the RSM
        # Set up the plot
        # Extract the time axis values directly from the NDVar to label your plot nicely
        time_axis = trf_ndvar.time.times 
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(grand_average_rsm, 
                    cmap='RdBu_r', 
                    center=0, 
                    vmin=-1, vmax=1, 
                    square=True,
                    xticklabels=np.round(time_axis, 2), # Add actual TRF time lags
                    yticklabels=np.round(time_axis, 2))
        
        # Only show every 10th label to prevent the axes from getting cluttered
        plt.xticks(np.arange(0, len(time_axis), 10), np.round(time_axis[::10], 2))
        plt.yticks(np.arange(0, len(time_axis), 10), np.round(time_axis[::10], 2))
        
        plt.title(f"L1_S{n_subj} Envelope TRF Representational Similarity Matrix")
        plt.xlabel("Time Lag (s)")
        plt.ylabel("Time Lag (s)")
        plt.gca().invert_yaxis()
        
        #plt.show() #(change it into save)
        plt.savefig(DST / f'Natives_S{n_subj}_envelope_TRF_RSM.png')
        
        '''
        ## (Useless)OLD CODES ##
        ##Step 3: Transpose the data from channels(rows) by timepoints(col) into timepoints(rows) by channels(col)
        # Below are unchange Gemini codes
        # Transpose the data to shape: (150 timepoints, 64 channels)
        X = trf.h[0].T  #trf_data.T 
        
        print(f"Shape for RSA: {X.shape} (Timepoints, Channels)")
        
        ##Step 4: Compute the RSM
        # Compute the correlation matrix between all time points
        # The resulting shape will be (n_timepoints, n_timepoints)
        similarity_matrix = np.corrcoef(X)
        
        # Alternatively, if you want a Dissimilarity Matrix (RDM):
        # dissimilarity_matrix = 1 - similarity_matrix
        
        print(f"RSM Shape: {similarity_matrix.shape}")
        '''
        '''
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
        '''
    
    """

    ## Alice_ESLs ##
    
    #STIMULI = [str(i) for i in range(1, 13)]
    #DATA_ROOT = Path("/Volumes/DH_4GB/Neurolang_1_Copy(ver20231203)/Master Program/New_Thesis_topic/Experiments_Results") #("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    #DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    #PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    #PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'
    IMF_DIR = DATA_ROOT/ "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/F0_predictors"
    IMFsLIST = [path.name for path in IMF_DIR.iterdir() if re.match(r'Alice_IF_IMF_*', path.name)] 
    ESL_SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'n_2_S\d*', path.name)]  #S01_alice-raw.fif
    
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR.mkdir(exist_ok=True)
    print(ESL_SUBJECTS)
    print(len(ESL_SUBJECTS))  # 26
    DST = TRF_DIR / 'ESLs_figures'
    DST.mkdir(exist_ok=True)
    
    """
    #PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors' 
    #PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'
    ESL_SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'n_2_S\d*', path.name)]  #S01_alice-raw.fif
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR.mkdir(exist_ok=True)
    print(ESL_SUBJECTS)
    print(len(ESL_SUBJECTS))  # 26
    
    DST = TRF_DIR / 'ESLs_figures'
    DST.mkdir(exist_ok=True)
    """
    
    ## TRFs Envelope  ##
    #subj_sLIST = []
    #for subj_name in ESL_SUBJECTS:
        #subj_sLIST.append(int(subj_name[5:8]))
    n_ESL_rowsLIST = []
    all_ESL_subj_rsmsLIST = []
    for subj in  ESL_SUBJECTS:
        ESL_subj = int(subj[5:8])
        res = eelbrain.load.unpickle(TRF_DIR / Path('S%.3d/S%.3d Fzero+envelope+env_onset.pickle'%(ESL_subj, ESL_subj))) #envelope
        #rowsLIST.append([subj, res.proportion_explained, res.h[0]])#.abs()])

        
        # 2. Extract the NDVar for the envelope predictor
        # (For those have more than one NDVar in one pickle files) Find the index of the 'Fzero' predictor in the model
        # Note: Make sure the string matches exactly what is printed by n_trf.x 
        # (e.g., 'Fzero' or 'f0' depending on how you named it)
        res.x = ['f0', 'f0env', 'f0envenvon']
        predictor_name = 'f0'
        f0_index = res.x.index(predictor_name)
        
        ESL_trf_ndvar = res.h[f0_index] #[0]
        
        # 3. Extract the NumPy array for the RSM
        # By specifying dims=('time', 'sensor'), Eelbrain returns an array of shape (timepoints, channels).
        # This becomes our 'X' matrix directly.
        X = ESL_trf_ndvar.get_data(dims=('time', 'sensor'))
        
        # 4. Compute the RSM (Pearson correlation across time points)
        # np.corrcoef expects variables as rows, so X needs to be (time, sensors)
        similarity_matrix = np.corrcoef(X)
        
        # Save the Subject ID, proportion explained, and the computed RSM
        n_ESL_rowsLIST.append([ESL_subj, res.proportion_explained, similarity_matrix])
        all_ESL_subj_rsmsLIST.append(similarity_matrix)
        
        print(f"Subject {ESL_subj}: RSM computed with shape {similarity_matrix.shape}")
        
        # Optional: Convert the list of RSMs to a 3D numpy array (Subjects x Time x Time)
        # This is highly useful for computing the grand average RSM across your group
        group_rsm_array = np.array(all_ESL_subj_rsmsLIST)
        grand_average_rsm = np.mean(group_rsm_array, axis=0)
        
        ##Step 5: Visualize the RSM
        # Set up the plot
        # Extract the time axis values directly from the NDVar to label your plot nicely
        time_axis = ESL_trf_ndvar.time.times 
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(grand_average_rsm, 
                    cmap='RdBu_r', 
                    center=0, 
                    vmin=-1, vmax=1, 
                    square=True,
                    xticklabels=np.round(time_axis, 2), # Add actual TRF time lags
                    yticklabels=np.round(time_axis, 2))
        
        # Only show every 10th label to prevent the axes from getting cluttered
        plt.xticks(np.arange(0, len(time_axis), 10), np.round(time_axis[::10], 2))
        plt.yticks(np.arange(0, len(time_axis), 10), np.round(time_axis[::10], 2))
        
        plt.title(f"ESL_S{ESL_subj} {predictor_name} TRF Representational Similarity Matrix")
        plt.xlabel("Time Lag (s)")
        plt.ylabel("Time Lag (s)")
        plt.gca().invert_yaxis()
        
        #plt.show() #(change it into save)
        plt.savefig(DST / f'ESLs_S{ESL_subj}_{predictor_name}_TRF_RSM.png')
        #"""