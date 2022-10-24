#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
import scipy.signal
from pydub import AudioSegment
import subprocess

if __name__ == "__main__":
    
    data_path = "/Users/ting-hsin/Docs/Github/ICN_related/LTTC/S002_audios/"
    
    # files
    src = data_path + "S002_textaudio_1.mp3"
    dst = "S002_test_1.wav"
    """
    ## convert wav to mp3
    audSeg = AudioSegment.from_mp3(src)
    audSeg.export(dst, format="wav")
    
    ##open data to check the sampling rate
    sample_rate, data = wavfile.read(dst) #.format(i+1))
    print(sample_rate)
    print("The data points of tape 1 is", len(data))
    """
    subprocess.call(['ffmpeg', '-i', src, dst])
    