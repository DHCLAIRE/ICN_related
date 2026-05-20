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
    
    
    """
    ## Natives RSM (within subjs) ##
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
        print("natives sensors: ", trf_ndvar.sensor.names)
        
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
        #plt.savefig(DST / f'Natives_S{n_subj}_envelope_TRF_RSM.png')
        
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
    

    """
    ## ESLs pre-VST RSM (within subjs) on Env/F0/EnvOnset
    ## Compute the RSM of each subject on the timepoint ##
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
    
    """
    
    ### Include VST as proficiency level indicator##
    ### To arrange the ESL according to the VST scores.
    ### VST score of each sub of ESL ##
    #VST_Score_STR_LIST = ['6.7', '7.3', '7.8', '8.2', '8.4', '6.4', '7.5', '6.7', '5.2', '5.3', '6.5'
                     #, '5.1', '6.1', '7.9', '8.7', '8.0', '8.8', '6.4', '7.0', '7.4', '6.6', '7.2'
                     #, '7.0', '7.3', '7.3', '7.7']  # 26 subs
    #VST_Score_float_LIST = [6.7, 7.3, 7.8, 8.2, 8.4, 6.4, 7.5, 6.7
                            #, 5.2, 5.3, 6.5, 5.1, 6.1, 7.9, 8.7, 8.0
                            #, 8.8, 6.4, 7.0, 7.4, 6.6, 7.2, 7.0, 7.3, 7.3, 7.7]
    ## exclude sub: 14 / 18 / 33 / 37
    #sub_idLIST = [10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27
                  #, 28, 29, 30, 31, 32, 34, 35, 36, 38, 39]
    ## Female = 1; Male = 2
    #sub_SexLIST = ["F", "M", "M", "F", "F", "M", "F", "M", "M", "F", "M", "F", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"]
     
    ## dictionary of lists 
    #VST_df = pd.DataFrame({'id': sub_idLIST, 'VST': VST_Score_float_LIST, 'gender':sub_SexLIST})
       
    ##VST_df = pd.DataFrame(id_VST_DICT)
       
    #print(VST_df) 
    ##print(type(VST_df["VST"][0]))
    ##print(VST_df.loc[0])
    """
    ## ESL's within group's RSM  ##
    ## ESL RSM of Within Groups on Time X Time RSMs based on VST Starts ##
    # ... [Insert your VST_df creation code here] ...
    
    # 1. Sort the DataFrame by VST score in descending order (High to Low)
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    print(VST_df_sorted)
    
    # 2. Extract the original indices of the sorted subjects
    # This tells us how to shuffle the rows/columns of the RSM array
    sorted_indices = VST_df_sorted.index.to_numpy()
    
    # 3. Create new labels for plotting so we can see the VST score next to the Subject ID
    sorted_labels = [f"S{row['id']} ({row['VST']})" for _, row in VST_df_sorted.iterrows()]
    
    print(f"New Subject Order by Index: {sorted_indices}")
    
    
    ## To compute the intersubject RSM based on timepoints ##
    
    all_subjects_data = []
    subject_labels = []
    original_subject_ids = [] # Keep track of the raw IDs for matching later
    
    # 1. Gather the data across all subjects
    for subject in ESL_SUBJECTS:
        n_subj = int(subject[5:8])
        subject_labels.append(f"S{n_subj}") # Save labels for plotting later
        original_subject_ids.append(n_subj)
        
        n_trf = eelbrain.load.unpickle(TRF_DIR / subject[4:8] / f'{subject[4:8]} Fzero+envelope+env_onset.pickle')
        
        # Extract Fzero NDVar
        f0_index = n_trf.x.index('Fzero')
        f0_ndvar = n_trf.h[f0_index]
        
        # Extract the data as (time, sensor)
        X_f0 = f0_ndvar.get_data(dims=('time', 'sensor'))
        all_subjects_data.append(X_f0)
    
    # 2. Stack into a 3D array: Shape becomes (Subjects, Timepoints, Sensors)
    group_data = np.array(all_subjects_data)
    n_subjects, n_timepoints, n_sensors = group_data.shape
    
    print(f"Group data assembled with shape: {group_data.shape}")
    
    # 3. Compute Subject x Subject RSM for each time point
    time_by_time_rsms = []
    
    for t in range(n_timepoints):
        # Slice the data at time point 't'
        spatial_pattern_at_t = group_data[:, t, :] 
        
        # Compute correlation matrix
        subj_rsm = np.corrcoef(spatial_pattern_at_t)
        time_by_time_rsms.append(subj_rsm)
    
    # Convert the result to a 3D numpy array: Shape (Timepoints, Subjects, Subjects)
    time_by_time_rsms = np.array(time_by_time_rsms)
    print(f"Final RSM array shape: {time_by_time_rsms.shape} (Time, Subject, Subject)")
    
    
    # ==========================================
    # 3.5 SORTING BY VST SCORE (NEWLY ADDED)
    # ==========================================
    
    # Sort the DataFrame from High to Low VST
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    
    sorted_indices = []
    sorted_labels = []
    
    # Match the sorted DataFrame IDs to the original array index order
    for _, row in VST_df_sorted.iterrows():
        subj_id = int(row['id'])
        if subj_id in original_subject_ids:
            # Find where this subject is in our 3D array
            idx = original_subject_ids.index(subj_id)
            sorted_indices.append(idx)
            # Create a new label combining ID and VST score for the plot
            sorted_labels.append(f"S{subj_id} ({row['VST']})")
    
    # Convert to numpy array for advanced indexing
    sorted_indices = np.array(sorted_indices)
    
    # Reorder the rows and columns of the entire 3D RSM array
    sorted_time_by_time_rsms = time_by_time_rsms[:, sorted_indices, :] # Reorder rows
    sorted_time_by_time_rsms = sorted_time_by_time_rsms[:, :, sorted_indices] # Reorder columns
    
    
    # ==========================================
    # 4. PLOTTING THE SORTED RSM
    # ==========================================
    
    time_axis = f0_ndvar.time.times 
    target_time_sec = -0.100 
    
    t_index = np.argmin(np.abs(time_axis - target_time_sec))
    actual_time = time_axis[t_index]
    
    # Extract the SORTED RSM for that specific time point
    rsm_to_plot = sorted_time_by_time_rsms[t_index]
    
    plt.figure(figsize=(12, 10)) # Slightly wider to accommodate longer labels
    
    sns.heatmap(rsm_to_plot, 
                cmap='RdBu_r', 
                center=0, 
                vmin=-1, vmax=1, 
                square=True,
                xticklabels=sorted_labels,  # Use the new VST labels
                yticklabels=sorted_labels)
    
    plt.title(f"ESL Subject x Subject RSM (Sorted by VST) for 'Fzero' at {actual_time * 1000:.0f} ms")
    plt.xlabel("Subject ID (VST Score)")
    plt.ylabel("Subject ID (VST Score)")
    
    plt.tight_layout() 
    # plt.show()    
    plt.savefig(DST / f'ESLs_time{target_time_sec}_Fzero_TRF_RSM_SortedVST.png')
    ## ESL RSM of Within Groups on Time X Time RSMs based on VST ENDs ##
    """
    
    """
    ## RSM of Between Groups only on Time X Time RSMs Starts ##
    ## VERSION 2 : Calculate Between group RSM regardless the chn montages ##
    
    ## Calculate Between group RSM using a Time Window ##
    #TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'
    #TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'
    
    # --- [Assume VST_df is already created and sorted here] ---
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}
    
    all_subject_vectors = []
    combined_labels = []
    
    ## ==========================================
    ## NEW: DEFINE YOUR TIME WINDOW (Seperately)
    ## ==========================================
    ## Instead of one target time, define a window (e.g., 0.650s to 0.750s)
    #tmin = 0.950
    #tmax = 1.000
    
    # ==========================================
    # 1. DEFINE THE TIME PARAMETERS
    # ==========================================
    step = 0.050  # 50 ms interval
    start_times = np.arange(0, 1.000, step)  # Creates [0.0, 0.05, 0.1, ..., 0.95]
    
    # ==========================================
    # 2. THE MAIN TEMPORAL LOOP
    # ==========================================
    for tmin in start_times:
        tmax = tmin + step
        print(f"--- Processing Window: {tmin*1000:.0f}ms to {tmax*1000:.0f}ms ---")
        
        all_subject_vectors = []
        combined_labels = []        
        # ==========================================
        # 1. LOAD NATIVES & COMPUTE TIME x TIME RSM
        # ==========================================
        for subj in Native_SUBJECTS:
            n_subj = int(subj[1:3])
            combined_labels.append(f"Nat_{n_subj}") 
            
            n_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Fzero+envelope+env_onset.pickle')
            f0_index = n_trf.x.index('onset')
            f0_ndvar = n_trf.h[f0_index]
            
            # MODIFICATION: Use .sub(time=...) to extract only the specific time window
            windowed_ndvar = f0_ndvar.sub(time=(tmin, tmax))
            X_f0 = windowed_ndvar.get_data(dims=('time', 'sensor'))
            
            time_time_rsm = np.corrcoef(X_f0)
            upper_triangle_vector = time_time_rsm[np.triu_indices_from(time_time_rsm, k=1)]
            all_subject_vectors.append(upper_triangle_vector)
        
        num_natives = len(Native_SUBJECTS)
        
        
        # ==========================================
        # 2. LOAD ESLs & COMPUTE TIME x TIME RSM
        # ==========================================
        for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
            if esl_id in esl_subj_dict:
                subject_str = esl_subj_dict[esl_id]
                combined_labels.append(f"ESL_{esl_id} ({vst})")
                
                n_trf = eelbrain.load.unpickle(TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} Fzero+envelope+env_onset.pickle')
                f0_index = n_trf.x.index('onset')
                f0_ndvar = n_trf.h[f0_index]
                
                # MODIFICATION: Use .sub(time=...) to extract only the specific time window
                windowed_ndvar = f0_ndvar.sub(time=(tmin, tmax))
                X_f0 = windowed_ndvar.get_data(dims=('time', 'sensor'))
                
                time_time_rsm = np.corrcoef(X_f0)
                upper_triangle_vector = time_time_rsm[np.triu_indices_from(time_time_rsm, k=1)]
                all_subject_vectors.append(upper_triangle_vector)
        # ==========================================
        # 3. COMPUTE SECOND-ORDER RSM & PLOT
        # ==========================================
        second_order_rsm = np.corrcoef(np.array(all_subject_vectors))
        
        plt.figure(figsize=(14, 12))
        sns.heatmap(second_order_rsm,
                    cmap='RdBu_r',
                    center=0,
                    vmin=-1,
                    vmax=1,
                    square=True,
                    xticklabels=combined_labels,  
                    yticklabels=combined_labels)
        
        # Visual Dividers
        plt.axhline(num_natives, color='black', linewidth=2) #len(Native_SUBJECTS), color='black', linewidth=2)
        plt.axvline(num_natives, color='black', linewidth=2) #len(Native_SUBJECTS), color='black', linewidth=2)
        
        plt.title(f"Second-Order Inter-Subject RSM: EnvOnset ({tmin*1000:.0f}-{tmax*1000:.0f} ms)")
        
        # Save each plot with a unique name
        filename = f'Combined_EnvOnset_RSM_{int(tmin*1000):04d}_{int(tmax*1000):04d}ms.png'
        plt.savefig(DST_ESLs / filename)
        plt.close() # Important: Close plot to free up memory during the loop        
        
        
        ## Time X Time RSM (BEFORE LOOP) ##
        # ==========================================
        # 3. COMPUTE THE SECOND-ORDER GROUP RSM
        # ==========================================
        group_temporal_data = np.array(all_subject_vectors)
        second_order_rsm = np.corrcoef(group_temporal_data)
        
        
        # ==========================================
        # 4. PLOT THE NATIVE VS ESL MATRIX
        # ==========================================
        plt.figure(figsize=(14, 12))
        
        sns.heatmap(second_order_rsm, 
                    cmap='RdBu_r', 
                    center=0, 
                    vmin=-1, vmax=1, 
                    square=True,
                    xticklabels=combined_labels,  
                    yticklabels=combined_labels)
        
        plt.axhline(num_natives, color='black', linewidth=2)
        plt.axvline(num_natives, color='black', linewidth=2)
        
        
        ## Before LOOP ##
        # MODIFICATION: Update the title to reflect the time window
        plt.title(f"Second-Order Inter-Subject RSM: Envelope Processing ({tmin*1000:.0f} ms to {tmax*1000:.0f} ms)")
        plt.xlabel("Subject ID")
        plt.ylabel("Subject ID")
        
        plt.tight_layout() 
        plt.savefig(DST / f'Combined_SecondOrder_Envelope_TRF_RSM_{tmin*1000:.0f}to{tmax*1000:.0f}ms.png')
        ## RSM of Between Groups only on Time X Time RSMs Ends ##
        
    """
    """
    ## VERSION one of between groups (F0 dynamics) on Time X Time RSM Start ##
    # --- [Assume VST_df is already created and sorted here] ---
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}
    
    all_subject_vectors = []
    combined_labels = []
    
    # ==========================================
    # 1. LOAD NATIVES & COMPUTE TIME x TIME RSM
    # ==========================================
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        combined_labels.append(f"Nat_{n_subj}") 
        
        n_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Fzero+envelope+env_onset.pickle')
        f0_index = n_trf.x.index('Fzero')
        f0_ndvar = n_trf.h[f0_index]
        
        # Shape: (Timepoints, 61 Sensors)
        X_f0 = f0_ndvar.get_data(dims=('time', 'sensor'))
        
        # np.corrcoef correlates rows. X_f0 is (Time, Sensor), so this yields (Time, Time)
        time_time_rsm = np.corrcoef(X_f0)
        
        # Extract the upper triangle (excluding the diagonal) and flatten to a 1D vector
        upper_triangle_vector = time_time_rsm[np.triu_indices_from(time_time_rsm, k=1)]
        all_subject_vectors.append(upper_triangle_vector)
    
    num_natives = len(Native_SUBJECTS)
    
    # ==========================================
    # 2. LOAD ESLs & COMPUTE TIME x TIME RSM
    # ==========================================
    for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
        if esl_id in esl_subj_dict:
            subject_str = esl_subj_dict[esl_id]
            combined_labels.append(f"ESL_{esl_id} ({vst})")
            
            n_trf = eelbrain.load.unpickle(TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} Fzero+envelope+env_onset.pickle')
            f0_index = n_trf.x.index('Fzero')
            f0_ndvar = n_trf.h[f0_index]
            
            # Shape: (Timepoints, 64 Sensors)
            X_f0 = f0_ndvar.get_data(dims=('time', 'sensor'))
            
            # Yields (Time, Time)
            time_time_rsm = np.corrcoef(X_f0)
            
            # Extract the upper triangle and flatten to a 1D vector
            upper_triangle_vector = time_time_rsm[np.triu_indices_from(time_time_rsm, k=1)]
            all_subject_vectors.append(upper_triangle_vector)
    
    # ==========================================
    # 3. COMPUTE THE SECOND-ORDER GROUP RSM
    # ==========================================
    # Stack all 1D temporal fingerprint vectors. 
    # Shape: (Total Subjects, Number of Temporal Relationships)
    group_temporal_data = np.array(all_subject_vectors)
    
    # Correlate the subjects' temporal fingerprints against each other
    # Yields a final (Total Subjects, Total Subjects) matrix
    second_order_rsm = np.corrcoef(group_temporal_data)
    
    
    # ==========================================
    # 4. PLOT THE NATIVE VS ESL MATRIX
    # ==========================================
    plt.figure(figsize=(14, 12))
    
    sns.heatmap(second_order_rsm, 
                cmap='RdBu_r', 
                center=0, 
                vmin=-1, vmax=1, 
                square=True,
                xticklabels=combined_labels,  
                yticklabels=combined_labels)
    
    # Draw lines to separate Natives and ESLs into 4 quadrants (L1-L1, L2-L2, L1-L2)
    plt.axhline(num_natives, color='black', linewidth=2)
    plt.axvline(num_natives, color='black', linewidth=2)
    
    plt.title("Second-Order Inter-Subject RSM: Temporal Dynamics of F0 Processing")
    plt.xlabel("Subject ID")
    plt.ylabel("Subject ID")
    
    plt.tight_layout() 
    plt.savefig(DST / 'Combined_SecondOrder_Fzero_TRF_RSM.png')
    ## VERSION one of between groups (F0 dynamics) on Time X Time RSM End ##
    """
    
    """
    ## Compute Between groups' RSM? ##
    #import numpy as np
    #import pandas as pd
    #import matplotlib.pyplot as plt
    #import seaborn as sns
    #import eelbrain
    #from pathlib import Path
    TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'
    
    # --- [Assume VST_df is already created and sorted here] ---
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    
    # Create a dictionary to easily look up ESL folder/file strings by their ID
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}
    
    all_subjects_data = []
    combined_labels = []
    
    # ==========================================
    # 1. DEFINE COMMON SENSORS (61 vs 64 fix)
    # ==========================================
    # (You will need to manually define this list based on the intersection 
    # of your Native and ESL cap montages. For example:)
    # common_sensors = ['Fz', 'Cz', 'Pz', 'O1', 'O2', ...] 
    # For now, assuming you have this list:
    common_sensors = [...] # INSERT YOUR COMMON SENSOR STRINGS HERE
    
    
    # ==========================================
    # 2. LOAD NATIVE SUBJECTS (Group 1)
    # ==========================================
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        combined_labels.append(f"Nat_{n_subj}") 
        
        # NOTE: Ensure this path correctly points to the Native TRFs containing Fzero
        # Assuming it's formatted similarly to the ESLs:
        n_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Fzero+envelope+env_onset.pickle')
        
        f0_index = n_trf.x.index('Fzero')
        f0_ndvar = n_trf.h[f0_index]
        
        # Sub-select only the common sensors so the shapes match!
        f0_common = f0_ndvar.sub(sensor=common_sensors)
        X_f0 = f0_common.get_data(dims=('time', 'sensor'))
        all_subjects_data.append(X_f0)
    
    num_natives = len(Native_SUBJECTS) # Save this number to draw the quadrant lines later
    
    # ==========================================
    # 3. LOAD SORTED ESL SUBJECTS (Group 2)
    # ==========================================
    # By loading them in sorted order, we don't have to sort the array later!
    for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
        if esl_id in esl_subj_dict:
            subject_str = esl_subj_dict[esl_id]
            combined_labels.append(f"ESL_{esl_id} ({vst})")
            
            n_trf = eelbrain.load.unpickle(TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} Fzero+envelope+env_onset.pickle')
            
            f0_index = n_trf.x.index('Fzero')
            f0_ndvar = n_trf.h[f0_index]
            
            # Sub-select common sensors
            f0_common = f0_ndvar.sub(sensor=common_sensors)
            X_f0 = f0_common.get_data(dims=('time', 'sensor'))
            all_subjects_data.append(X_f0)
    
    
    # ==========================================
    # 4. COMPUTE THE COMBINED RSM
    # ==========================================
    # Shape becomes: (Natives + ESLs, Timepoints, Common_Sensors)
    group_data = np.array(all_subjects_data)
    n_subjects, n_timepoints, n_sensors = group_data.shape
    
    print(f"Combined group data assembled with shape: {group_data.shape}")
    
    time_by_time_rsms = []
    
    for t in range(n_timepoints):
        spatial_pattern_at_t = group_data[:, t, :] 
        subj_rsm = np.corrcoef(spatial_pattern_at_t)
        time_by_time_rsms.append(subj_rsm)
    
    time_by_time_rsms = np.array(time_by_time_rsms)
    
    
    # ==========================================
    # 5. PLOT WITH QUADRANT DIVIDERS
    # ==========================================
    time_axis = f0_common.time.times 
    target_time_sec = 0.700 
    t_index = np.argmin(np.abs(time_axis - target_time_sec))
    actual_time = time_axis[t_index]
    
    rsm_to_plot = time_by_time_rsms[t_index]
    
    plt.figure(figsize=(14, 12))
    
    sns.heatmap(rsm_to_plot, 
                cmap='RdBu_r', 
                center=0, 
                vmin=-1, vmax=1, 
                square=True,
                xticklabels=combined_labels,  
                yticklabels=combined_labels)
    
    # Draw lines to separate Natives and ESLs into 4 distinct quadrants
    plt.axhline(num_natives, color='black', linewidth=2)
    plt.axvline(num_natives, color='black', linewidth=2)
    
    plt.title(f"Native vs ESL (Sorted by VST) RSM for 'Fzero' at {actual_time * 1000:.0f} ms")
    plt.xlabel("Subject ID")
    plt.ylabel("Subject ID")
    
    plt.tight_layout() 
    plt.savefig(DST / f'Combined_time{target_time_sec}_Fzero_TRF_RSM.png')
    """
    
    ## Spatial RSM ##
    ## Interpolate the Native's 61 channels ##
    # ==========================================
    # 0. SETUP: DIRECTORIES & ESL SORTING
    # ==========================================
    #TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'
    #TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'
    
    ## Set predictor's name ##
    #predictorLIST = ["Fzero", "envelope", "onset"]  #Fzero+envelope+env_onset.pickle
    predictorLIST = ['word', 'lexical', 'non_lexical']  #words+lexical.pickle
    
    predictorSTR = predictorLIST[0]
    
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
    
    ## Set VST as ESL's Rank ##
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}
    
    # ==========================================
    # 1. SETUP: DYNAMIC MNE "SUPER-CAP" INTERPOLATION
    # ==========================================
    # Load the raw 61-channel Native montage coordinates
    native_montage = mne.channels.read_custom_montage('/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results/TRFs_pridictors/easycapM10-acti61_elec.sfp')
    
    # --- MODIFICATION START ---
    # Load the FIRST Native subject temporarily just to see which 59 sensors survived preprocessing
    sample_subj = int(Native_SUBJECTS[0][1:3])
    sample_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{sample_subj:02d}' / f'S{sample_subj:02d} words+lexical.pickle' ) #Fzero+envelope+env_onset.pickle')
    
    # Extract the exact 59 channel names actually present in your data
    actual_native_chs = sample_trf.h[sample_trf.x.index(predictorSTR)].sensor.names #index('onset')].sensor.names
    
    # Create safe names ONLY for those 59 channels
    native_chs_safe = [f"NAT_{ch}" for ch in actual_native_chs]
    # --- MODIFICATION END ---
    
    # Define the 64-channel ESL montage
    esl_montage = mne.channels.make_standard_montage('standard_1020') 
    esl_chs = esl_montage.ch_names[:64] 
    
    # Build the 123-channel combined Info object (59 Native + 64 ESL)
    all_chs = native_chs_safe + esl_chs
    info_combined = mne.create_info(ch_names=all_chs, sfreq=500, ch_types=['eeg'] * len(all_chs))
    
    # Map the 3D coordinates
    combined_positions = {}
    native_positions = native_montage.get_positions()['ch_pos']
    esl_positions = esl_montage.get_positions()['ch_pos']
    
    # Only extract coordinates for the 59 channels that actually exist
    for i, ch in enumerate(actual_native_chs):
        combined_positions[native_chs_safe[i]] = native_positions[ch]
    
    for ch in esl_chs:
        combined_positions[ch] = esl_positions[ch]
    
    combined_montage = mne.channels.make_dig_montage(ch_pos=combined_positions)
    info_combined.set_montage(combined_montage)
    
    print(f"Success! Super-montage created with {len(info_combined.ch_names)} channels.")    
    
    # ==========================================
    # 1. DEFINE THE TIME PARAMETERS
    # ==========================================
    step = 0.2#010 
    start_times = np.arange(0, 1.000, step)  
    
    # --- NEW: Lists to store data for the line graph ---
    plot_times = []
    median_r_natives = []
    median_r_esls = []
    perm_95th_thresholds = []
    
    # --- NEW: Lists to accumulate the 3D matrices across time ---
    all_time_raw_data = [] # Will hold the raw 64-sensor data
    all_time_rsms = []     # Will hold the 59x59 correlation matrices    
    
    # ==========================================
    # 2. THE MAIN TEMPORAL LOOP
    # ==========================================
    for tmin in start_times:
        tmax = tmin + step
        print(f"--- Processing Window: {tmin*1000:.0f}ms to {tmax*1000:.0f}ms ---")
        
        all_subjects_spatial_data = []
        combined_labels = []
        
        # --- A. Process Natives (Requires Interpolation) ---
        for subj in Native_SUBJECTS:
            n_subj = int(subj[1:3])
            combined_labels.append(f"Nat_{n_subj}") 
            
            n_trf = eelbrain.load.unpickle(TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} words+lexical.pickle') #Fzero+envelope+env_onset.pickle')
            
            # --- MODIFICATION: Slice the time window immediately! ---
            f0_ndvar_window = n_trf.h[n_trf.x.index(predictorSTR)].sub(time=(tmin, tmax)) #index('Fzero')].sub(time=(tmin, tmax))
            
            native_data = f0_ndvar_window.get_data(dims=('sensor', 'time'))
            # --- MODIFICATION: Slice the time window immediately! ---
            # ==========================================
            # THE TRUTH TEST
            # ==========================================
            print(f"\n--- TESTING NATIVE {n_subj} ---")
            print(f"Is native_data completely empty (all zeros) BEFORE we add the padding? : {np.all(native_data == 0)}")
            print(f"First 3 sensors, First 3 timepoints from Eelbrain:\n{native_data[:3, :3]}")
            # ==========================================
            n_times = native_data.shape[1]
            
            combined_data = np.vstack((native_data, np.zeros((len(esl_chs), n_times))))
            pprint(combined_data)
            evoked = mne.EvokedArray(combined_data, info_combined)
            evoked.info['bads'] = esl_chs 
            evoked.interpolate_bads(reset_bads=True, verbose=False)
            
            interpolated_data = evoked.copy().pick_channels(esl_chs).data
            
            # --- MODIFICATION: Average across the time window to get 1 spatial map ---
            # Shape goes from (64 Sensors, n_times) to just (64 Sensors,)
            mean_spatial_map = interpolated_data.mean(axis=1)
            #all_subjects_spatial_data.append(mean_spatial_map)
        
            # --- NEW FIX: Z-Score the 64-sensor spatial map ---
            # ADDed for avoiding NaN crash the median
            # --- SAFE Z-SCORE ---
            if np.std(mean_spatial_map) == 0:
                zscored_spatial_map = np.zeros_like(mean_spatial_map)
            else:
                zscored_spatial_map = zscore(mean_spatial_map)
                
            all_subjects_spatial_data.append(zscored_spatial_map)
            
        num_natives = len(Native_SUBJECTS)
        
        # --- B. Process ESLs (With Dynamic Interpolation & Sorting) ---
        print("--- Processing and sorting ESL group... ---")
        for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
            if esl_id in esl_subj_dict:
                subject_str = esl_subj_dict[esl_id]
                combined_labels.append(f"ESL_{esl_id} ({vst})")
    
                n_trf = eelbrain.load.unpickle(TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} words+lexical.pickle') #Fzero+envelope+env_onset.pickle')
    
                # --- MISSING FIX 1: Slice the time window immediately! ---
                f0_ndvar_window = n_trf.h[n_trf.x.index(predictorSTR)].sub(time=(tmin, tmax)) #index('Fzero')].sub(time=(tmin, tmax))
    
                # ==========================================
                # --- CASE-SENSITIVITY TRANSLATOR ---
                # ==========================================
                raw_esl_chs = list(f0_ndvar_window.sensor.names)
                standard_case_map = {ch.upper(): ch for ch in esl_montage.ch_names}
                esl_actual_chs = [standard_case_map.get(ch.upper(), ch) for ch in raw_esl_chs]
                # ==========================================
    
                missing_chs = [ch for ch in esl_chs if ch not in esl_actual_chs]
    
                if len(missing_chs) > 0:
                    # Note: We use ('sensor', 'time') so the math matches the Native block
                    actual_data = f0_ndvar_window.get_data(dims=('sensor', 'time'))
                    n_times = actual_data.shape[1]
    
                    combined_data = np.vstack((actual_data, np.zeros((len(missing_chs), n_times))))
    
                    current_all_chs = esl_actual_chs + missing_chs
                    info_esl = mne.create_info(ch_names=current_all_chs, sfreq=500, ch_types=['eeg'] * len(current_all_chs))
    
                    info_esl.set_montage(esl_montage) 
    
                    evoked = mne.EvokedArray(combined_data, info_esl)
                    evoked.info['bads'] = missing_chs
                    evoked.interpolate_bads(reset_bads=True, verbose=False)
    
                    # Extract the 64 channels. Shape: (64 Sensors, n_times)
                    esl_data_final = evoked.copy().pick_channels(esl_chs).data
                else:
                    # --- NO INTERPOLATION NEEDED ---
                    ch_indices = [esl_actual_chs.index(ch) for ch in esl_chs]
    
                    # Note: Kept as ('sensor', 'time') to match the interpolated shape
                    raw_data = f0_ndvar_window.get_data(dims=('sensor', 'time')) 
    
                    # Extract and sort the 64 channels simultaneously. Shape: (64 Sensors, n_times)
                    esl_data_final = raw_data[ch_indices, :]
    
                # --- MISSING FIX 2: Average across the time window! ---
                # Shape goes from (64 Sensors, n_times) to just (64 Sensors,)
                mean_spatial_map = esl_data_final.mean(axis=1)
                # Append the 1D spatial map, matching the Natives exactly
                #all_subjects_spatial_data.append(mean_spatial_map)
                
                # --- NEW FIX: Z-Score the 64-sensor spatial map ---
                # ADDed for avoiding NaN crash the median
                # --- SAFE Z-SCORE ---
                if np.std(mean_spatial_map) == 0:
                    zscored_spatial_map = np.zeros_like(mean_spatial_map)
                else:
                    zscored_spatial_map = zscore(mean_spatial_map)
                    
                # Append the 1D spatial map, matching the Natives exactly
                all_subjects_spatial_data.append(zscored_spatial_map) # Append the z-scored version
                
        
        # ==========================================
        # 3. FIRST-ORDER (SPATIAL) RSM COMPUTATION & PERMUTATION
        # ==========================================
        # Shape is perfectly (Total Subjects, 64 Sensors)
        group_data = np.array(all_subjects_spatial_data)
        num_total_subj = group_data.shape[0]
    
        # A. Calculate the REAL spatial RSM
        spatial_rsm_real = np.corrcoef(group_data)

        # --- NEW: Save this window's raw data and RSM to our accumulator lists ---
        all_time_raw_data.append(group_data)
        all_time_rsms.append(spatial_rsm_real)
        
        # B. Run the Permutation Test (1000 iterations)
        n_permutations = 1000
        print(f"   Running {n_permutations} permutations...")
        null_rsms = np.zeros((n_permutations, num_total_subj, num_total_subj))
        
        for i in range(n_permutations):
            shuffled_data = np.zeros_like(group_data)
            for s in range(num_total_subj):
                shuffled_data[s, :] = np.random.permutation(group_data[s, :])
            null_rsms[i, :, :] = np.corrcoef(shuffled_data)
    
        # ==========================================
        # --- NEW: EXTRACT MEDIANS & THRESHOLD ---
        # ==========================================
        # 1. Native Group Median (Top-Left Quadrant)
        native_block = spatial_rsm_real[:num_natives, :num_natives]
        idx_nat = np.triu_indices(num_natives, k=1) # Exclude diagonal
        median_r_natives.append(np.nanmedian(native_block[idx_nat]))  # change from np.median() to np.nanmedian(), so that the median value won't be crashed by the NaN subjects
    
        # 2. ESL Group Median (Bottom-Right Quadrant)
        esl_block = spatial_rsm_real[num_natives:, num_natives:]
        idx_esl = np.triu_indices(num_total_subj - num_natives, k=1)
        median_r_esls.append(np.nanmedian(esl_block[idx_esl])) # change from np.median() to np.nanmedian(), so that the median value won't be crashed by the NaN subjects
    
        # 3. Permutation Threshold (95th percentile of the absolute fake correlations)
        idx_all = np.triu_indices(num_total_subj, k=1)
        fake_corrs_off_diag = null_rsms[:, idx_all[0], idx_all[1]]
        threshold_95 = np.nanpercentile(np.abs(fake_corrs_off_diag), 95)
        perm_95th_thresholds.append(threshold_95)
    
        # 4. Save the timepoint (using the start of the window, in ms)
        plot_times.append(tmin * 1000)
        
        # ==========================================
        # --- MISSING FIX: CALCULATE P-VALUES FOR THE HEATMAP ---
        # ==========================================
        # Count how many times the fake correlation was >= the real correlation
        exceedances = np.sum(np.abs(null_rsms) >= np.abs(spatial_rsm_real), axis=0)
        p_values = exceedances / n_permutations
        
        ## OLD VERSION STARTS ##
        #for i in range(n_permutations):
            #shuffled_data = np.zeros_like(group_data)
    
            ## Shuffle the 64 channels independently for EVERY subject
            #for s in range(num_total_subj):
                #shuffled_data[s, :] = np.random.permutation(group_data[s, :])
    
            ## Calculate the fake RSM for this iteration
            #null_rsms[i, :, :] = np.corrcoef(shuffled_data)
    
        ## C. Calculate P-values
        ## Count how many times the fake correlation was >= the real correlation
        ## We use np.abs() to test for both strong positive and strong negative correlations (Two-tailed test)
        #exceedances = np.sum(np.abs(null_rsms) >= np.abs(spatial_rsm_real), axis=0)
        #p_values = exceedances / n_permutations
        ## OLD VERSION ENDS ##    
        
        # ==========================================
        # 4. PLOT THE THRESHOLDED SPATIAL RSM
        # ==========================================
        plt.figure(figsize=(14, 12))
        
        alpha_threshold = 0.05
        mask = (p_values > alpha_threshold) | (np.eye(num_total_subj, dtype=bool))
        
        sns.heatmap(spatial_rsm_real, 
                        cmap='RdBu_r', 
                        center=0, 
                        vmin=-1, vmax=1, 
                        square=True,
                        mask=mask, 
                        xticklabels=combined_labels,  
                        yticklabels=combined_labels,
                        cbar_kws={'label': "Pearson's r (p < 0.05)"}) 
        
        plt.axhline(num_natives, color='black', linewidth=2)
        plt.axvline(num_natives, color='black', linewidth=2)
        
        plt.title(f"Thresholded Spatial RSM: {predictorSTR}-Zed ({tmin*1000:.0f}-{tmax*1000:.0f} ms)\nPermutations: {n_permutations}, α = {alpha_threshold}") 
        plt.xlabel("Subject ID")
        plt.ylabel("Subject ID")
        
        filename = f'Thresholded_FirstOrder_Spatial_{predictorSTR}-Zed_RSM_{tmin*1000:.0f}-{tmax*1000:.0f}ms.png'
        plt.tight_layout() 
        plt.savefig(DST_ESLs / filename)
        plt.close()

    # <--- NOTICE HOW WE UNINDENTED EVERYTHING BELOW THIS LINE TO BE OUTSIDE THE LOOP! --->
    
    # ==========================================
    # 5. PLOT THE TIME-SERIES LINE GRAPH
    # ==========================================
    print("--- Generating Time-Series Graph... ---")
    print("Checking Native Data:", median_r_natives[:5])
    print("Checking Native Data:", median_r_esls[:5])
    plt.figure(figsize=(12, 6))
    
    # Plot the three lines
    plt.plot(plot_times, median_r_natives, label='Native Group (Median r)', color='#1f77b4', linewidth=2.5, marker='o')
    plt.plot(plot_times, median_r_esls, label='ESL Group (Median r)', color='#d62728', linewidth=2.5, marker='o')
    plt.plot(plot_times, perm_95th_thresholds, label='Permutation Threshold (α=0.05)', color='black', linestyle='--', linewidth=2)
    
    # Aesthetics
    plt.title(f"Spatial Similarity Dynamics over Time: Natives vs. ESLs ({predictorSTR}-Zed)_10msINV", fontsize=14)
    plt.xlabel("Time Window Start (ms)", fontsize=12)
    plt.ylabel("Median Pearson's r", fontsize=12)
    
    # Set x-ticks to match your 50ms intervals
    plt.xticks(plot_times, rotation=45)
    
    # Add a subtle grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(DST_ESLs / f'Median_RSM_TimeSeries_{predictorSTR}-Zed_10msINV.png')
    plt.close()
    
    print("--- Pipeline Complete! ---")
    
    # ==========================================
    # 6. SAVE THE 3D ARRAYS TO DISK (.npy)
    # ==========================================
    print("--- Saving 3D Arrays for Machine Learning & Analysis... ---")
    
    # 1. Save the Raw Data
    # Stacks the list into a 3D array. Shape: (20 Timepoints, 59 Subjects, 64 Sensors)
    final_3d_raw = np.array(all_time_raw_data)
    raw_filename = f'Raw_Spatial_Maps_{predictorSTR}-Zed_10msINV_AllWindows.npy'
    np.save(DST_ESLs / raw_filename, final_3d_raw)
    print(f"Saved Raw Data: {raw_filename} | Shape: {final_3d_raw.shape}")
    
    # 2. Save the RSM Data
    # Stacks the list into a 3D array. Shape: (20 Timepoints, 59 Subjects, 59 Subjects)
    final_3d_rsm = np.array(all_time_rsms)
    rsm_filename = f'FirstOrder_Spatial_{predictorSTR}-Zed_RSM_10msINV_AllWindows.npy'
    np.save(DST_ESLs / rsm_filename, final_3d_rsm)
    print(f"Saved RSM Data: {rsm_filename} | Shape:{final_3d_rsm.shape}")
    
    print("--- Pipeline Complete! ---")
                    
        ## ==========================================
        ## 3. FIRST-ORDER (SPATIAL) RSM COMPUTATION
        ## ==========================================
        ## Shape is now perfectly (Total Subjects, 64 Sensors)
        #group_data = np.array(all_subjects_spatial_data)
        
        ## We no longer need t_index! Just correlate the spatial maps directly.
        #spatial_rsm = np.corrcoef(group_data)
        
        ## ==========================================
        ## 4. PLOT THE SPATIAL RSM
        ## ==========================================
        #plt.figure(figsize=(14, 12))
        
        #sns.heatmap(spatial_rsm, 
                    #cmap='RdBu_r', 
                    #center=0, 
                    #vmin=-1, vmax=1, 
                    #square=True,
                    #xticklabels=combined_labels,  
                    #yticklabels=combined_labels)
        
        #plt.axhline(num_natives, color='black', linewidth=2)
        #plt.axvline(num_natives, color='black', linewidth=2)
        
        #plt.title(f"Spatial RSM: Envelope_Zscored ({tmin*1000:.0f}-{tmax*1000:.0f} ms)") 
        #plt.xlabel("Subject ID")
        #plt.ylabel("Subject ID")
        
        #filename = f'FirstOrder_Spatial_Envelope_RSM_Zscored_{tmin*1000:.0f}-{tmax*1000:.0f}ms.png'
        #plt.tight_layout() 
        #plt.savefig(DST_ESLs / filename)
        #plt.close()