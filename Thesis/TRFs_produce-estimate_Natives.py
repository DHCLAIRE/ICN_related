#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""This script estimates TRFs for several models and saves them"""
from pathlib import Path
import re

import eelbrain
import mne
import trftools

if __name__ == "__main__":
    
    STIMULI = [str(i) for i in range(1, 13)]
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results") #Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    IMF_DIR = DATA_ROOT/ "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/F0_predictors"
    IMFsLIST = [path.name for path in IMF_DIR.iterdir() if re.match(r'Alice_IF_IMF_*', path.name)]
    EEG_DIR = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'S\d*', path.name[:4])]
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR.mkdir(exist_ok=True)
    print(SUBJECTS)
    print(len(SUBJECTS))
    print(IMFsLIST)  # ['Alice_IF_IMF_6.pickle', 'Alice_IF_IMF_4.pickle', 'Alice_IF_IMF_2.pickle', 'Alice_IF_IMF_5.pickle', 'Alice_IF_IMF_1.pickle', 'Alice_IF_IMF_3.pickle']
    
    # Load stimuli
    # ------------
    # Make sure to name the stimuli so that the TRFs can later be distinguished
    # Load the gammatone-spectrograms; use the time axis of these as reference
    gammatone = [eelbrain.load.unpickle(PREDICTOR_audio_DIR / f'{stimulus}~gammatone-8.pickle') for stimulus in STIMULI]
    
    # Resample the spectrograms to 100 Hz (time-step = 0.01 s), which we will use for TRFs
    gammatone = [x.bin(0.01, dim='time', label='start') for x in gammatone]
    
    # Pad onset with 100 ms and offset with 1 second; make sure to give the predictor a unique name as that will make it easier to identify the TRF later
    gammatone = [trftools.pad(x, tstart=-0.100, tstop=x.time.tstop + 1, name='gammatone') for x in gammatone]
    
    # Load the broad-band envelope and process it in the same way
    envelope = [eelbrain.load.unpickle(PREDICTOR_audio_DIR / f'{stimulus}~gammatone-1.pickle') for stimulus in STIMULI]  # Load in the data
    envelope = [x.bin(0.01, dim='time', label='start') for x in envelope]
    envelope = [trftools.pad(x, tstart=-0.100, tstop=x.time.tstop + 1, name='envelope') for x in envelope]
    onset_envelope = [eelbrain.load.unpickle(PREDICTOR_audio_DIR / f'{stimulus}~gammatone-on-1.pickle') for stimulus in STIMULI]
    onset_envelope = [x.bin(0.01, dim='time', label='start') for x in onset_envelope]
    onset_envelope = [trftools.pad(x, tstart=-0.100, tstop=x.time.tstop + 1, name='onset') for x in onset_envelope]
    
    # Load onset spectrograms and make sure the time dimension is equal to the gammatone spectrograms
    gammatone_onsets = [eelbrain.load.unpickle(PREDICTOR_audio_DIR / f'{stimulus}~gammatone-on-8.pickle') for stimulus in STIMULI]
    gammatone_onsets = [x.bin(0.01, dim='time', label='start') for x in gammatone_onsets]
    gammatone_onsets = [eelbrain.set_time(x, gt.time, name='gammatone_on') for x, gt in zip(gammatone_onsets, gammatone)]
    
    # Load word tables and convert tables into continuous time-series with matching time dimension
    word_tables = [eelbrain.load.unpickle(PREDICTOR_word_DIR / f'{stimulus}~Ngram-CFG_word.pickle') for stimulus in STIMULI]
    word_onsets = [eelbrain.event_impulse_predictor(gt.time, ds=ds, name='word') for gt, ds in zip(gammatone, word_tables)] # not sure why they could get the word onset this way
    
    # Function and content word impulses based on the boolean variables in the word-tables
    word_lexical = [eelbrain.event_impulse_predictor(gt.time, value='lexical', ds=ds, name='lexical') for gt, ds in zip(gammatone, word_tables)]
    word_nlexical = [eelbrain.event_impulse_predictor(gt.time, value='nlexical', ds=ds, name='non_lexical') for gt, ds in zip(gammatone, word_tables)]
    
    # NGRAM/CFG word impulses based on the values in the word-tables
    word_Ngram = [eelbrain.event_impulse_predictor(gt.time, value='NGRAM', ds=ds, name='n-gram') for gt, ds in zip(gammatone, word_tables)]
    word_CFG = [eelbrain.event_impulse_predictor(gt.time, value='CFG', ds=ds, name='cfg') for gt, ds in zip(gammatone, word_tables)]
    
    # Extract the duration of the stimuli, so we can later match the EEG to the stimuli
    durations = [gt.time.tmax for stimulus, gt in zip(STIMULI, gammatone)]
    
    # Get the calculated IMFs
    # IMFsLIST : ['Alice_IF_IMF_6.pickle', 'Alice_IF_IMF_4.pickle', 'Alice_IF_IMF_2.pickle', 'Alice_IF_IMF_5.pickle', 'Alice_IF_IMF_1.pickle', 'Alice_IF_IMF_3.pickle']
    imf1 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[4])  # old: IMFsLIST[0] = Alice_IF_IMF_6.pickle
    imf2 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[2])  # old: IMFsLIST[1] = Alice_IF_IMF_4.pickle
    imf3 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[5])  # old: IMFsLIST[2] = Alice_IF_IMF_2.pickle
    imf4 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[1])  # old: IMFsLIST[3] = Alice_IF_IMF_5.pickle
    imf5 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[3])  # old: IMFsLIST[4] = Alice_IF_IMF_1.pickle
    imf6 = eelbrain.load.unpickle(IMF_DIR / IMFsLIST[0])  # old: IMFsLIST[5] = Alice_IF_IMF_3.pickle
    
    # Get the calculated F0s
    #F_zero = eelbrain.load.unpickle(F0_DIR / f'Alice_F0_all.pickle')
    
    # Models
    # ------
    # Pre-define models here to have easier access during estimation. In the future, additional models could be added here and the script re-run to generate additional TRFs.
    models = {
        
        # IFs
        'IMF1':[imf1],
        'IMF12':[imf1, imf2],
        'IMF123':[imf1, imf2, imf3],
        'IMF1234':[imf1, imf2, imf3, imf4],
        'IMF12345':[imf1, imf2, imf3, imf4, imf5],
        'IMFAll':[imf1, imf2, imf3, imf4, imf5, imf6],

        # All auditory features model
        #'All_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical]  >> already have, therefore don't run again
        #'All_Aud_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical, imf1, imf2, imf3, imf4, imf5, imf6, F_zero]
        # All model
        #'All_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical, word_CFG, word_Ngramm, imf_1, imf_2, imf_3, imf_4, imf_5, imf_6, F_zero]
    }
    """
    # Acoustic models
    'envelope': [envelope],
    'envelope+onset': [envelope, onset_envelope],
    'acoustic': [gammatone, gammatone_onsets],
    # Models with word-onsets and word-class
    'words': [word_onsets],
    'words+lexical': [word_onsets, word_lexical, word_nlexical],
    'acoustic+words': [gammatone, gammatone_onsets, word_onsets],
    'acoustic+words+lexical': [gammatone, gammatone_onsets, word_onsets, word_lexical, word_nlexical],
    # Language Models
    'Ngram': [word_Ngram, word_onsets, word_lexical, word_nlexical],
    'CFG': [word_CFG, word_onsets, word_lexical, word_nlexical],
    'Ngram-CFG_all': [word_Ngram, word_CFG, word_onsets, word_lexical, word_nlexical],
    
    # IFs
    'IMF1':[imf1], # old name in file is >>'IMF_1':[imf_1]
    'IMF12':[imf1, imf2],
    'IMF123':[imf1, imf2, imf3],
    'IMF1234':[imf1, imf2, imf3, imf4],
    'IMF12345':[imf1, imf2, imf3, imf4, imf5],
    'IMFAll':[imf1, imf2, imf3, imf4, imf5, imf6],   # old name in file is :'IMF_All':[imf_1, imf_2, imf_3, imf_4, imf_5, imf_6]

    # F0
    'Fzero+envelope': [F_zero]
    'Fzero+envelope': [envelope, onset_envelope, F_zero]

    # All auditory features model
    'All_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical]
    #'All_Aud_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical, imf1, imf2, imf3, imf4, imf5, imf6, F_zero]
    # All model
    #'All_model':[envelope, onset_envelope, word_onsets, word_lexical, word_nlexical, word_CFG, word_Ngramm, imf_1, imf_2, imf_3, imf_4, imf_5, imf_6, F_zero]
    }
    """
    
    # Estimate TRFs
    # -------------
    # Loop through subjects to estimate TRFs
    for subject in SUBJECTS:
        subject_trf_dir = TRF_DIR / subject[:3]
        subject_trf_dir.mkdir(exist_ok=True)
        # Generate all TRF paths so we can check whether any new TRFs need to be estimated
        trf_paths = {model: subject_trf_dir / f'{subject[:3]} {model}.pickle' for model in models}
        # Skip this subject if all files already exist
        #if all(path.exists() for path in trf_paths.values()):
            #continue
        # Load the EEG data
        raw = mne.io.read_raw_fif(EEG_DIR / f'{subject}', preload=True)  # subject /
        # Band-pass filter the raw data between 0.5 and 20 Hz
        raw.filter(0.5, 20)
        # Interpolate bad channels
        raw.interpolate_bads()
        # Extract the events marking the stimulus presentation from the EEG file
        events = eelbrain.load.fiff.events(raw)
        # Not all subjects have all trials; determine which stimuli are present
        trial_indexes = [STIMULI.index(stimulus) for stimulus in events['event']]
        # Extract the EEG data segments corresponding to the stimuli
        trial_durations = [durations[i] for i in trial_indexes]
        eeg = eelbrain.load.fiff.variable_length_epochs(events, -0.100, trial_durations, connectivity='auto')  #, decim=5 #decim=5 meaning to resample to sfreq=100Hz
        # Since trials are of unequal length, we will concatenate them for the TRF estimation.
        eeg_concatenated = eelbrain.concatenate(eeg)
        for model, predictors in models.items():
            path = trf_paths[model]
            # Skip if this file already exists
            #if path.exists():
                #continue
            print(f"Estimating: {subject[:3]} ~ {model}")
            # Select and concetenate the predictors corresponding to the EEG trials
            predictors_concatenated = []
            for predictor in predictors:
                #print(predictor)
                predictors_concatenated.append(eelbrain.concatenate([predictor[i] for i in trial_indexes]))
            #print(predictors_concatenated)
            # Fit the mTRF
            trf = eelbrain.boosting(eeg_concatenated, predictors_concatenated, -0.100, 1.000, error='l1', basis=0.050, partitions=5, test=1, selective_stopping=True)
            #p = eelbrain.plot.TopoButterfly(trf.h_scaled) # to check the boosted trf is not None
            #p
            
            # Save the TRF for later analysis
            eelbrain.save.pickle(trf, path)
