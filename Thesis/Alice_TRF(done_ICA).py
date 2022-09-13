#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# The normal packages for nlp
from pprint import pprint
import csv
import json
import random
from random import sample
from datetime import datetime,date
import pandas as pd
from collections import Counter

# TRF required packages
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import scipy.io as sio
from scipy import stats
import numpy as np
import mne
import eelbrain
from itertools import islice

"""
# Things that need to be prepared to do TRF
1. wordVec: the list of the content word in the text.
2. onset time of the word
3. offset time of the word
4. Sentence boundaries >> this one need to be calculate by myself >> the info is in the csv file.
CPS (closure positive shift), happened when the boundary started. 

the parameters of the envolope of the audio files need to be collect, then to downsample to 128 Hz.
** Alice's audio need to be downsample and calculate the envelope

mastoid channels >> use the soft bone behind both ears as the references (M1 / M2)

DC mode> without high pass filter >> add it on in the later analysis

EEG needs to match with the envelope data
"""

"""

ICA(derivatives_in open data):
1. remove the noise
2. remove the motion artifacts

"""



# Self-defined function by Kevin Hsu
def get_raw_EEG(Sid, runid):
    """
    Turn the EEG data from matlab .mat form into eelbrain tolerable form
    """
    # sio in scipy>> named by oneself
    # Because the file in here is from matlab, therefore , use sio to load .mat
    audio = sio.loadmat("data/Stimuli/Envelopes/audio%d_128Hz.mat"%runid)
    text = sio.loadmat("data/Stimuli/Text/Run%d.mat"%runid)
    EEG = sio.loadmat("data/EEG/Subject%d/Subject%d_Run%d.mat"%(Sid,Sid,runid))
    eeg_scalp = EEG["eegData"] # time by channels
    eeg_mas = EEG["mastoids"]

    # time by channels >> channels by times
    eeg_scalp = np.transpose( eeg_scalp, (1, 0)) 
    eeg_mas = np.transpose( eeg_mas, (1, 0)) 

    # combine the eeg_scalp & eeg_mas together
    eeg_ = np.concatenate((eeg_scalp, eeg_mas), axis = 0) #axis = 0 >> use the first axis to combine (axis x)
    audio = audio["env"]
    # use the shorter data as the main shape of the final data
    if eeg_.shape[1] > audio.shape[0]:
        eeg_ = eeg_[:, :audio.shape[0]]

    if eeg_.shape[1] < audio.shape[0]:
        audio = audio[:eeg_.shape[1]]

    tstep = 1. / 128 # 1. >>use the "." to help calculate the decimal #tstep = 點跟點之間停留多長 = sampling rate's 倒數
    n_times = audio.shape[0]
    time = eelbrain.UTS(0, tstep, n_times)
    # the 3 commands above are required to form the following thing >> envelope
    envelope = eelbrain.NDVar(audio.ravel(), (time,), name='envelope')
#####
    temp = mne.channels.make_standard_montage("biosemi128")
    ch_names = temp.ch_names
    ch_names.append("M1")
    ch_names.append("M2")
    ch_types = ['eeg'] * 130 # create 130 EEG channels
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=128)

    raw = mne.io.RawArray(eeg_ * 1e-6, info) # the original unit of EEG is volt >> we turned it into micro volt >> *1e-6
    raw.set_eeg_reference(["M1", "M2"]).pick('all', exclude=["M1", "M2"]).set_montage('biosemi128')
    print(raw)

    return raw, envelope, time

def raw2NDvar(raw, time):
    """
    Turn the raw data into NDVar objects
    """
    montage_x = eelbrain.load.fiff.sensor_dim(raw.info)
    temp_data = raw.get_data().T *1e+6
    eegNDVar = eelbrain.NDVar(temp_data, (time, montage_x), name='EEG', info={'unit': 'µV'}) #'µV'(micro volt) >> 'V' (volt)
    return eegNDVar

def word_onsets_NDVar(runid, time):
    """
    Turn the word_onset(int) into the NDVar objects
    """
    text = sio.loadmat("data/Stimuli/Text/Run%d.mat"%runid)
    words = [x[0][0] for x in text["wordVec"]]
    onsets = [x[0] for x in text["onset_time"]]

    onset_word = eelbrain.NDVar(np.zeros(len(time)), time, name='Word_on')
    for x in onsets:
        onset_word[x] = 1
        pass
    return onset_word


if __name__ == "__main__":
    
    # After the neural data has been preprocessed(ICA)
    # If you want to see the pic>> please save it instead of pop it out
    
    
    # Turn the eeg data (neural data) into NDVar
    eegNDVar = raw2NDvar(raw, time)
     # plot the NDVar to see a certain timepoint
    p = eelbrain.plot.TopoButterfly(eegNDVar, xlim=5, w=7, h=2)
    p.set_time(1.300)
    
    # Turn the envelope value into UTS (and eelbrain class objects)
    eelbrain.plot.UTS(envelope, xlim=20, w=12, h=2)
    
    
    """
    2 ways of examine the TRF
    1. average all TRFs
    2. To see the correlations of TRFs between subjects
    """
    
    # Boosting is to create the TRF function
    res = eelbrain.boosting(eegNDVar, envelope,  -0.100, 0.600, error='l1',
                            basis=0.050, partitions=5, test=1)
    p = eelbrain.plot.TopoButterfly(res.h_scaled, w=10, h=4)
    p.set_time(.180)
    
    # plotting the res.h_scaled by using eelbrain  # what is the res.h_scaled????
    p = eelbrain.plot.TopoButterfly(res.h_scaled, w=10, h=4)
    p.set_time(.45)
    
    # Do the same routine of turn raw into NDVar for the second section of the eeg data from the same subject
    raw2, envelope2, time2 = get_raw_EEG(1, 2)
    raw2.filter(1, 20)
    ica.apply(raw2) # exclude the same ICA component as the first round 
    eegNDVar2 = raw2NDvar(raw2, time2)
    p = eelbrain.plot.TopoButterfly(eegNDVar2, xlim=5, w=7, h=2)
    p.set_time(1.300)
    
    
    # perform the same procedure on the same subject's different runs (part3-5)
    raw3, envelope3, time3 = get_raw_EEG(1, 3)
    raw3.filter(1, 20)
    ica.apply(raw3)
    eegNDVar3 = raw2NDvar(raw3, time3)
    
    raw4, envelope4, time4 = get_raw_EEG(1, 4)
    raw4.filter(1, 20)
    ica.apply(raw4)
    eegNDVar4 = raw2NDvar(raw4, time4)
    
    raw5, envelope5, time5 = get_raw_EEG(1, 5)
    raw5.filter(1, 20)
    ica.apply(raw5)
    eegNDVar5 = raw2NDvar(raw5, time5)
    
    # combine 5 NDVar data that we just created
    env_ = eelbrain.concatenate([envelope, envelope2, envelope3, envelope4, envelope5])
    eegNDVar_ = eelbrain.concatenate([eegNDVar, eegNDVar2, eegNDVar3, eegNDVar4, eegNDVar5])
    
    # to see the envelope and the word_onset info
    print(eegNDVar_)
    # to calculate the length of the data
    print(115204 / 128.)  # Divided by the sampling rate will get the length of the data
    
    print(eegNDVar)
    print(22729 / 128.)
    
    p = eelbrain.plot.TopoButterfly(eegNDVar_, w=7, h=2)
    p.set_time(1.300)
    
    # partitions=5 >> divide the EEG data into 5 portions, so that the model could compare the training data with the testing data
    res = eelbrain.boosting(eegNDVar_, env_, -0.100, 0.600, error='l1', basis=0.050, partitions=5, test=1)
    p = eelbrain.plot.TopoButterfly(res.h_scaled, w=6, h=2)
    p.set_time(.180)
    
    
    p = eelbrain.plot.Topomap(res.proportion_explained, w=6, h=4)
    p.set_vlim(-0.01, 0.01)
    # proportion_explained: is the results of the highest TRF similarity of every channel
    # remember to save the result of it for further examination of
    
    # Sace the envelope's TRF in a pickle file form
    Subj = 1
    eelbrain.save.pickle(res, 'Subj%d_TRFs_envelop.pickle'%(Subj))
    
    # if you already saved the pickle file in the preoprocessing step, there's a command for you to open the saved pickle file
    Subj = 1
    res = eelbrain.load.unpickle('Subj%d_TRFs_envelop.pickle'%(Subj))
    p = eelbrain.plot.TopoButterfly(res.h_scaled, w=10, h=4)
    p.set_time(.180)
    
    #Making the Word onset TRFs >> if onset = 1
    onset_word = word_onsets_NDVar(1, time)
    eelbrain.plot.UTS(onset_word, xlim=10, w=6, h=2)
    
    # repeat the same procedure to get run1 to run5's 
    onset_word2 = word_onsets_NDVar(2, time2)
    onset_word3 = word_onsets_NDVar(3, time3)
    onset_word4 = word_onsets_NDVar(4, time4)
    onset_word5 = word_onsets_NDVar(5, time5)
    
    # create
    w_on = eelbrain.concatenate([onset_word, onset_word2, onset_word3, onset_word4, onset_word5])
    eelbrain.plot.UTS(w_on, xlim=100, w=10, h=4)
    
    # combine the envelope TRF and the word_onset's TRF into one pickle
    res_v2 = eelbrain.boosting(eegNDVar_, [env_, w_on],  -0.1, 0.6, error='l1',
                            basis=0.050, partitions=5, test=1, selective_stopping=True)
    #[env_, w_on] >> 這裡放envelope & word onset 的 TRFs, if you want more, then add it into the list
    Subj = 1
    eelbrain.save.pickle(res_v2, 'Subj%d_TRFs_envelop_w_on.pickle'%(Subj))
    
    p = eelbrain.plot.TopoButterfly(res_v2.h_scaled, w=6, h=2)
    p.set_time(.180)
    
    
    


