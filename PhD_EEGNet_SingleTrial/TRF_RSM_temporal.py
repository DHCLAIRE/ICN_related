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
import pandas as pd

from pprint import pprint
import numpy as np
from scipy.stats import zscore  # <--- NEW IMPORT
from mne.stats import permutation_cluster_test

# A fast matrix-math function to calculate Pearson r across the subject dimension
def compute_r_map(rsms, behavioral_scores):
    beh_centered = behavioral_scores - np.mean(behavioral_scores)
    rsms_centered = rsms - np.mean(rsms, axis=0)
    
    cov = np.sum(rsms_centered * beh_centered[:, None, None], axis=0)
    beh_std = np.sqrt(np.sum(beh_centered**2))
    rsms_std = np.sqrt(np.sum(rsms_centered**2, axis=0))
    
    # Add a tiny epsilon (1e-8) to prevent division by zero errors on the diagonal
    return cov / (beh_std * rsms_std + 1e-8)

if __name__ == "__main__":
    ## Setting the stim length ##
    STIMULI = [str(i) for i in range(1, 13)]

    ## Set path of Natives & ESLs ##
    ## Alice_Natives ##
    #DATA_ROOT = Path("/Volumes/DH_4GB/Neurolang_1_Copy(ver20231203)/Master Program/New_Thesis_topic/Experiments_Results")
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR_NATs = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    EEG_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'

    ## Setting the Predictors Path ##
    IMF_DIR = DATA_ROOT/ "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/F0_predictors"
    IMFsLIST = [path.name for path in IMF_DIR.iterdir() if re.match(r'Alice_IF_IMF_*', path.name)]

    ## Finding the SUBJs files according to Groups ##
    Native_SUBJECTS = [path.name for path in EEG_DIR_NATs.iterdir() if re.match(r'S\d*', path.name)]
    ESL_SUBJECTS = [path.name for path in EEG_DIR_ESLs.iterdir() if re.match(r'n_2_S\d*', path.name)]  #S01_alice-raw.fif

    ## Define a target directory for TRF estimates and make sure the directory is created ##
    ## ESLs
    TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR_NATs.mkdir(exist_ok=True)
    DST_NATs = TRF_DIR_NATs / 'Natives_figures'
    DST_NATs.mkdir(exist_ok=True)
    print(Native_SUBJECTS)
    print(len(Native_SUBJECTS))

    ## ESLs
    TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR_ESLs.mkdir(exist_ok=True)
    DST_ESLs = TRF_DIR_ESLs / 'ESLs_figures'
    DST_ESLs.mkdir(exist_ok=True)    
    print(ESL_SUBJECTS)
    print(len(ESL_SUBJECTS))  # 26
    
    ## Include VST as proficiency level indicator##
    ## To arrange the ESL according to the VST scores.
    ## VST score of each sub of ESL ##
    VST_Score_STR_LIST = ['6.7', '7.3', '7.8', '8.2', '8.4', '6.4', '7.5', '6.7', '5.2', '5.3', '6.5'
                     , '5.1', '6.1', '7.9', '8.7', '8.0', '8.8', '6.4', '7.0', '7.4', '6.6', '7.2'
                     , '7.0', '7.3', '7.3', '7.7']  # 26 subs
    VST_Score_float_LIST = [6.7, 7.3, 7.8, 8.2, 8.4, 6.4, 7.5, 6.7
                            , 5.2, 5.3, 6.5, 5.1, 6.1, 7.9, 8.7, 8.0
                            , 8.8, 6.4, 7.0, 7.4, 6.6, 7.2, 7.0, 7.3, 7.3, 7.7]
    # exclude sub: 14 / 18 / 33 / 37
    sub_idLIST = [10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27
                  , 28, 29, 30, 31, 32, 34, 35, 36, 38, 39]
    # Female = 1; Male = 2
    sub_SexLIST = ["F", "M", "M", "F", "F", "M", "F", "M", "M", "F", "M", "F", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"]
     
    # dictionary of lists 
    VST_df = pd.DataFrame({'id': sub_idLIST, 'VST': VST_Score_float_LIST, 'gender':sub_SexLIST})
       
    #VST_df = pd.DataFrame(id_VST_DICT)
       
    print(VST_df) 
    #print(type(VST_df["VST"][0]))
    #print(VST_df.loc[0])
    
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}
    

    ## Temporal RSM (Time by Time between Groups)
    # ==========================================
    # 1. LOAD NATIVES & COMPUTE TIME x TIME RSM
    # ==========================================
    print("--- Computing Time x Time RSMs for Native Group ---")
    native_rsms = []
    
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        
        n_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Fzero+envelope+env_onset.pickle')
        f0_ndvar = n_trf.h[n_trf.x.index('envelope')]
        
        # Extract the FULL 0 to 1 second epoch. 
        # Dims must be ('time', 'sensor') so np.corrcoef correlates time against time.
        X_f0 = f0_ndvar.sub(time=(0.0, 1.000)).get_data(dims=('time', 'sensor'))
        
        # Calculate the Time x Time correlation matrix for this single subject
        time_time_rsm = np.corrcoef(X_f0) 
        native_rsms.append(time_time_rsm)
    
    # Stack into a 3D array: Shape (Total Natives, Timepoints, Timepoints)
    native_rsms = np.array(native_rsms)
    time_axis = f0_ndvar.sub(time=(0.0, 1.000)).time.times
    
    # ==========================================
    # 2. LOAD ESLs & COMPUTE TIME x TIME RSM
    # ==========================================
    print("--- Computing Time x Time RSMs for ESL Group ---")
    esl_rsms = []
    
    for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
        if esl_id in esl_subj_dict:
            subject_str = esl_subj_dict[esl_id]
            
            n_trf = eelbrain.load.unpickle(TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} Fzero+envelope+env_onset.pickle')
            f0_ndvar = n_trf.h[n_trf.x.index('envelope')]
            
            X_f0 = f0_ndvar.sub(time=(0.0, 1.000)).get_data(dims=('time', 'sensor'))
            
            time_time_rsm = np.corrcoef(X_f0)
            esl_rsms.append(time_time_rsm)
    
    # Stack into a 3D array: Shape (Total ESLs, Timepoints, Timepoints)
    esl_rsms = np.array(esl_rsms)
    
    # ==========================================
    # 3. COMPUTE SECOND-ORDER (SUBJECT x SUBJECT) RSM
    # ==========================================
    print("--- Computing Second-Order Subject x Subject RSM ---")
    
    # To correlate 2D matrices, we must first flatten them into 1D vectors.
    # We extract only the upper triangle of the Time x Time matrix to avoid duplicate data.
    native_vectors = [rsm[np.triu_indices_from(rsm, k=1)] for rsm in native_rsms]
    esl_vectors = [rsm[np.triu_indices_from(rsm, k=1)] for rsm in esl_rsms]
    
    # Create the label lists so they align perfectly with the axes
    native_labels = [f"Nat_{int(subj[1:3])}" for subj in Native_SUBJECTS]
    esl_labels = []
    for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
        if esl_id in esl_subj_dict:
            esl_labels.append(f"ESL_{esl_id} ({vst})")
            
    combined_labels = native_labels + esl_labels
    num_natives = len(native_labels)
    
    # Stack all subjects together. Shape: (52 Subjects, Total Unique Time Relationships)
    group_temporal_vectors = np.vstack((native_vectors, esl_vectors))
    
    # Correlate the subjects! Shape will be (52 Subjects, 52 Subjects)
    second_order_rsm = np.corrcoef(group_temporal_vectors)

    # ==========================================
    # 4. PLOT THE SECOND-ORDER RSM
    # ==========================================
    plt.figure(figsize=(14, 12))
    
    sns.heatmap(second_order_rsm, 
                cmap='RdBu_r', 
                center=0, 
                vmin=-1, vmax=1, 
                square=True,
                xticklabels=combined_labels,  
                yticklabels=combined_labels,
                cbar_kws={'label': "Spearman's ρ (Temporal Similarity)"})
    
    # Draw Native vs ESL dividing lines
    plt.axhline(num_natives, color='black', linewidth=2)
    plt.axvline(num_natives, color='black', linewidth=2)
    
    plt.title(f"Second-Order Inter-Subject RSM: Full Temporal Dynamics (Envelope)") 
    plt.xlabel("Subject ID (Sorted by descending VST)")
    plt.ylabel("Subject ID (Sorted by descending VST)")
    
    plt.tight_layout() 
    plt.savefig(DST_ESLs / 'SecondOrder_SubjectXSubject_Envelope_Temporal_RSM.png')
    plt.close()
    print("--- Complete! ---")
    
    ## ==========================================
    ## 3. 2D CLUSTER-BASED PERMUTATION TEST
    ## ==========================================
    #print("--- Running 2D Cluster Permutation Test (Native vs ESL) ---")
    #n_permutations = 1000
    #alpha_threshold = 0.05
    
    ## Compare the two groups using a permutation test. 
    ## This automatically handles the shuffling of group labels to find significant temporal clusters.
    #cluster_stats = permutation_cluster_test(
        #[native_rsms, esl_rsms], 
        #n_permutations=n_permutations, 
        #tail=0, # Two-tailed test
        #out_type='mask' # Outputs a boolean mask of significant pixels
    #)
    
    #F_obs, clusters, cluster_p_values, H0 = cluster_stats
    
    ## Build a blank mask and fill it with True ONLY where the cluster survived p < 0.05
    #significant_mask = np.ones((len(time_axis), len(time_axis)), dtype=bool)
    #for c, p_val in zip(clusters, cluster_p_values):
        #if p_val < alpha_threshold:
            #significant_mask[c] = False # False means "do NOT mask this pixel" in Seaborn
    
    ## Calculate the average difference between groups to plot
    #group_difference = native_rsms.mean(axis=0) - esl_rsms.mean(axis=0)
    
    
    ## ==========================================
    ## 4. PLOT THE THRESHOLDED TEMPORAL RSM
    ## ==========================================
    ## Plotting the mathematical difference between groups, highlighting significant clusters
    #plt.figure(figsize=(12, 10))
    
    ## Plot the raw background very lightly (so you can see non-significant trends)
    #sns.heatmap(group_difference, cmap='RdBu_r', center=0, cbar=False, 
                #xticklabels=False, yticklabels=False, alpha=0.2)
    
    ## Overlay the significant clusters at full opacity using the mask
    #sns.heatmap(group_difference, cmap='RdBu_r', center=0, mask=significant_mask,
                #cbar_kws={'label': 'Difference in Pearson r (Clustered p < 0.05)'})
    
    ## Format the axes to show time in milliseconds rather than array indices
    #ticks = np.arange(0, len(time_axis), 50) # Tick every 100ms (50 samples at 500Hz)
    #tick_labels = [f"{time_axis[i]*1000:.0f}" for i in ticks]
    
    #plt.xticks(ticks, tick_labels, rotation=45)
    #plt.yticks(ticks, tick_labels, rotation=0)
    
    #plt.title(f"Temporal RSM: Native vs ESL Difference (Envelope)\nCluster Permutations: {n_permutations}, α = {alpha_threshold}")
    #plt.xlabel("Time (ms)")
    #plt.ylabel("Time (ms)")
    
    #plt.tight_layout() 
    #plt.savefig(DST_ESLs / 'Temporal_TimeXTime_Envelope_RSM_ClusterThresholded.png')
    #plt.close()
    #print("--- Complete! ---")