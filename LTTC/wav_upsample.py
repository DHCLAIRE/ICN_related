#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
import scipy.signal

if __name__ == "__main__":
    # The original script
    # https://gist.github.com/alexjaw/09af24d58ac99e1e4cafba092e063fe3
    
    data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"
    
    new_fs = 44100
    
    for i in range(30):
        # open data
        sample_rate, data = wavfile.read(data_path + 'S001_textaudio_modified_{}.wav'.format(i+1))
    
        print(sample_rate)
        print("The data points of tape", i+1,"is" ,len(data))
        
        # resample data
        new_num_samples = round(len(data)*float(new_fs)/sample_rate)
        data = scipy.signal.resample(data, new_num_samples).astype(np.int16)
        value = data[-1]  # what does this means??
        new_data = np.append(data, value)
        
        wavfile.write(filename=data_path+"testing_{}.wav".format(i+1), rate=44100, data=new_data)
        
        # open NEW data
        sample_rate_new, data_new = wavfile.read(data_path + 'testing_{}.wav'.format(i+1))
    
        print(sample_rate_new)
        print("The NEW data points of tape", i+1,"is" ,len(data_new))
        