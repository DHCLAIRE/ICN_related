#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""This script estimates TRFs for several models and saves them"""
from pathlib import Path
import re

import eelbrain
import mne
import trftools

import numpy as np

if __name__ == "__main__":
    
    STIMULI = [str(i) for i in range(1, 13)]
    DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    #DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'
    SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'n_2_S\d', path.name)]  #S01_alice-raw.fif
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR.mkdir(exist_ok=True)
    print(SUBJECTS)

    
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
    
    
    """ ### MUTE THESE FOR NOW ###
    # Load word tables and convert tables into continuous time-series with matching time dimension
    word_tables = [eelbrain.load.unpickle(PREDICTOR_word_DIR / f'{stimulus}~Ngram-CFG_word.pickle') for stimulus in STIMULI]
    word_onsets = [eelbrain.event_impulse_predictor(gt.time, ds=ds, name='word') for gt, ds in zip(gammatone, word_tables)]
    
    # Function and content word impulses based on the boolean variables in the word-tables
    word_lexical = [eelbrain.event_impulse_predictor(gt.time, value='lexical', ds=ds, name='lexical') for gt, ds in zip(gammatone, word_tables)]
    word_nlexical = [eelbrain.event_impulse_predictor(gt.time, value='nlexical', ds=ds, name='non_lexical') for gt, ds in zip(gammatone, word_tables)]
    
    # NGRAM/CFG word impulses based on the values in the word-tables
    word_Ngram = [eelbrain.event_impulse_predictor(gt.time, value='NGRAM', ds=ds, name='n-gram') for gt, ds in zip(gammatone, word_tables)]
    word_CFG = [eelbrain.event_impulse_predictor(gt.time, value='CFG', ds=ds, name='cfg') for gt, ds in zip(gammatone, word_tables)]
    
    # Extract the duration of the stimuli, so we can later match the EEG to the stimuli
    durations = [gt.time.tmax for stimulus, gt in zip(STIMULI, gammatone)]
    """
    # Models
    # ------
    # Pre-define models here to have easier access during estimation. In the future, additional models could be added here and the script re-run to generate additional TRFs.
    models = {
        # Acoustic models
        'envelope': [envelope],
        'envelope+onset': [envelope, onset_envelope]
    }
    
    """
    models = {
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
        'Ngram-CFG_all': [word_Ngram, word_CFG, word_onsets, word_lexical, word_nlexical]
    }
    """
    # Estimate TRFs
    # -------------
    # Loop through subjects to estimate TRFs
    for subject in SUBJECTS:  #type(subject) == str
        subject_trf_dir = TRF_DIR / subject[4:8]
        subject_trf_dir.mkdir(exist_ok=True)
        # Generate all TRF paths so we can check whether any new TRFs need to be estimated
        trf_paths = {model: subject_trf_dir / f'{subject[4:8]} {model}.pickle' for model in models}
        # Skip this subject if all files already exist
        #if all(path.exists() for path in trf_paths.values()):
            #continue
        # Load the EEG data
        raw = mne.io.read_raw_fif(EEG_DIR / f'{subject}', preload=True)
        # Band-pass filter the raw data between 0.5 and 20 Hz
        raw.filter(0.5, 20)  #.resample(sfreq=100)  # >> already resample to sfreq=100
        
        # Interpolate bad channels  
        #raw.interpolate_bads()  #>> to rewrite if there're no bad channels to interpolate, skip it
        
        # Extract the events marking the stimulus presentation from the EEG file
        events = eelbrain.load.fiff.events(raw)  # To check to events
        #print(events)
        # Not all subjects have all trials; determine which stimuli are present
        trial_indexes = [STIMULI.index(stimulus) for stimulus in events['event'] if stimulus in STIMULI]  # type(trial_indexes)==LIST
        #print(trial_indexes)
        
        # Extract the EEG data segments corresponding to the stimuli
        trial_durations = [durations[i] for i in trial_indexes]  # needs modification for having questions inbetween the tapes
        #print(trial_durations)
        
        #all_trial_durations = np.sum(np.array(trial_durations))
        #print(all_trial_durations)
        
        #eeg = eelbrain.load.fiff.variable_length_epochs(events, -0.100, trial_durations, decim=5, connectivity='auto')  #, decim=5  #trial_durations >> figure out how to cut on the right time
        #print(eeg)
        
        
        # Since trials are of unequal length, we will concatenate them for the TRF estimation.
        #eeg_concatenated = eelbrain.concatenate(eeg)
        #print(eeg_concatenated)
        
        for model, predictors in models.items():
            path = trf_paths[model]
            # Skip if this file already exists
            #if path.exists():
                #continue
            print(f"Estimating: {subject} ~ {model}")
            # Select and concetenate the predictors corresponding to the EEG trials
            predictors_concatenated = []
            for predictor in predictors:
                #print(predictor)
                predictors_concatenated.append(eelbrain.concatenate([predictor[i] for i in trial_indexes]))
            #print(predictors_concatenated)
            
            # Homemade NDVar instead of using .fiff.variable_length_epochs()
            eeg_ = raw.get_data()
            
            #[<NDVar 'envelope': 5863 time>, <NDVar 'envelope': 6194 time>, <NDVar 'envelope': 6435 time>, <NDVar 'envelope': 7108 time>, 
            # <NDVar 'envelope': 6737 time>, <NDVar 'envelope': 6487 time>, <NDVar 'envelope': 6399 time>, <NDVar 'envelope': 5840 time>, 
            # <NDVar 'envelope': 5832 time>, <NDVar 'envelope': 6236 time>, <NDVar 'envelope': 5726 time>, <NDVar 'envelope': 4808 time>]
            #[<NDVar 'envelope': 73665 time>]
            
            # Check if the data length is the same as the stimuli's length
            if eeg_.shape[1] > 73665:
                eeg_ = eeg_[:, :73665]
            
            # produce the time for NDVar production
            tstep = 1. / raw.info["sfreq"]  # already resample to 100Hz
            n_times = eeg_.shape[1] #audio.shape[0]
            time = eelbrain.UTS(0, tstep, n_times)
            #print(time)
        
            # NDVar production
            montage_x = eelbrain.load.fiff.sensor_dim(raw.info)
            temp_data = eeg_.T *1e+6
            eeg_concatenated = eelbrain.NDVar(temp_data, (time, montage_x), name='EEG', info={'unit': 'µV'})
            #print(eegNDVar)
            
            # Fit the mTRF
            trf = eelbrain.boosting(eeg_concatenated, predictors_concatenated, -0.100, 1.000, error='l1', basis=0.050, partitions=5, test=1, selective_stopping=True)
            # Save the TRF for later analysis
            eelbrain.save.pickle(trf, path)
            
