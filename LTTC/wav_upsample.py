#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
import scipy.signal
from pprint import pprint
from pathlib import Path

if __name__ == "__main__":
    # The original script
    # https://gist.github.com/alexjaw/09af24d58ac99e1e4cafba092e063fe3
    root_data_path  = Path("/Users/ting-hsin/Downloads/S005-S007/")
    
    data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG")
    #stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_LDT_pw_audios/"
    
    new_fs = 44100
    
    """
    pseudowordLIST = ["aegliy", "baepay", "baydiy", "browmey", "chaeviy", "laelaxst", "laeviy", "maeskiy", "paenliy", "payliy", "vaesow", "weyaet"]
    for wordSTR in pseudowordLIST:
        # open data
        sample_rate, data = wavfile.read(stim_data_path + '{}_v3_female.wav'.format(wordSTR))
    
        print(sample_rate)
        print("The data points of tape", wordSTR,"is" ,len(data))
        
        # resample data
        new_num_samples = round(len(data)*float(new_fs)/sample_rate)
        data = scipy.signal.resample(data, new_num_samples).astype(np.int16)  # no astype(np.int16)'s dtype == float64
        #data_dtype = data.dtype
        #print(data_dtype)
        value = data[-1]  # what does this means??   # data[-1]== -1, <class 'numpy.int16'>
        new_data = np.append(data, value)
        
        
        wavfile.write(filename=stim_data_path+'{}_v3_female.wav'.format(wordSTR), rate=44100, data=new_data)    
    """
    
    for subj in range(19, 20):
        subj_id = '%.3d' %subj
        audio_data_path = data_path / Path("LTTC_MEG_S%s/S%s_audios" %(subj_id, subj_id))
        print(subj_id)
        for i in range(30):
            # open data
            sample_rate, data = wavfile.read(audio_data_path / Path('S{}_textaudio_{}.wav'.format(subj_id, i+1)))
            
            print(sample_rate)
            print("The data points of tape", i+1,"is" ,len(data))
        
            # resample data
            new_num_samples = round(len(data)*float(new_fs)/sample_rate)
            data = scipy.signal.resample(data, new_num_samples).astype(np.int16)  # no astype(np.int16)'s dtype == float64
            #data_dtype = data.dtype
            #print(data_dtype)
            value = data[-1]  # what does this means??   # data[-1]== -1, <class 'numpy.int16'>
            new_data = np.append(data, value)
        
        
            wavfile.write(filename=audio_data_path / Path("S{}_textaudio_{}.wav".format(subj_id, i+1)), rate=44100, data=new_data)
        
    
        # open NEW data
        sample_rate_new, data_new = wavfile.read(data_path + "S999_modified_{}.wav".format(i+1))
    
        print(sample_rate_new)
        print("The NEW data points of tape", i+1,"is" ,len(data_new))
    """
    
    tmp_data_path = "/Users/ting-hsin/Downloads/S005-S007/LTTC_MEG_S013/S013_audios/"
    sample_rate, data = wavfile.read(tmp_data_path + 'S013_textaudio_4.wav')
    
    #print(sample_rate)
    #print("The data points of tape", i+1,"is" ,len(data))
    
    # resample data
    new_num_samples = round(len(data)*float(new_fs)/sample_rate)
    data = scipy.signal.resample(data, new_num_samples).astype(np.int16)  # no astype(np.int16)'s dtype == float64
    #data_dtype = data.dtype
    #print(data_dtype)
    value = data[-1]  # what does this means??   # data[-1]== -1, <class 'numpy.int16'>
    new_data = np.append(data, value)
    
    
    wavfile.write(filename=tmp_data_path+"S013_textaudio_4.wav", rate=44100, data=new_data)
    """
    """
    for i in range(20):
        # open data
        sample_rate, data = wavfile.read(tmp_data_path  + 'S013_modified_{}.wav'.format(i+11))
        
        print(sample_rate)
        print("The data points of tape", i+1,"is" ,len(data))
    
        # resample data
        new_num_samples = round(len(data)*float(new_fs)/sample_rate)
        data = scipy.signal.resample(data, new_num_samples).astype(np.int16)  # no astype(np.int16)'s dtype == float64
        #data_dtype = data.dtype
        #print(data_dtype)
        value = data[-1]  # what does this means??   # data[-1]== -1, <class 'numpy.int16'>
        new_data = np.append(data, value)
    
    
        wavfile.write(filename=data_path+"S013_modified_{}.wav".format(i+11), rate=44100, data=new_data)
    """
    """
    # open NEW data
    sample_rate_new, data_new = wavfile.read(data_path + "S999_modified_{}.wav".format(i+11))

    print(sample_rate_new)
    print("The NEW data points of tape", i+1,"is" ,len(data_new))
    """