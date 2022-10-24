#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scipy.io import wavfile
import scipy.signal

if __name__ == "__main__":
    
    data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"
    
    new_fs = 88200
    
    
    for i in range(5):
        # open data
        sample_rate, data = wavfile.read(data_path + 'S001_textaudio_modified_{}.wav'.format(i+1))
    
        print(sample_rate)
        print("The data points of tape", i+1,"is" ,len(data))
        
        # resample data
        new_num_samples = round(len(data)*float(new_fs)/sample_rate)
        data = scipy.signal.resample(data, new_num_samples)
        wavfile.write(filename=data_path+"testing_{}.wav".format(i+1), rate=88200, data=data)
        
        # open NEW data
        sample_rate_1, data_1 = wavfile.read(data_path + 'testing_{}.wav'.format(i+1))
    
        print(sample_rate_1)
        print("The NEW data points of tape", i+1,"is" ,len(data_1))
        