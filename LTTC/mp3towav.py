#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
import scipy.signal
from pydub import AudioSegment
import subprocess

if __name__ == "__main__":
    
    data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S002/S002_audios/"
    
    # files
    #src = data_path + "S002_textaudio_1.mp3"
    #dst = "S002_test_1.wav"
    
    ## convert wav to mp3
    #audSeg = AudioSegment.from_mp3(data_path+"S002_textaudio_1.mp3")
    #audSeg.export(dst, format="wav")
    
    ##open data to check the sampling rate
    #sample_rate, data = wavfile.read(data_path + 'S002_test_1.wav') #.format(i+1))
    #print(sample_rate)
    ##print("The data points of tape 1 is", len(data))
    
    subprocess.call(['ffmpeg', '-i', data_path + "S002_textaudio_1.mp3",data_path + 'S002_test_1.wav'])
    