#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core   # if you change the setting, this command must be put after the prefs's command
#import json
print(sound.Sound)

import scipy
from scipy.io import wavfile

# function to convert the information into
# some readable format
def output_duration(length):
    hours = length // 3600 # calculate in hours
    length %= 3600
    mins = length // 60 # calculate in minutes
    length %= 60
    seconds = length # calculate in seconds

    return hours, mins, seconds

if __name__ == "__main__":
    data_path = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/"
    #Alice_stm = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/DownTheRabbitHoleFinal_SoundFile{}.wav".format()
    
    # Method 3

    
    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file
    for i in range(12):
        
        sample_rate, data = wavfile.read(data_path + 'DownTheRabbitHoleFinal_SoundFile{}.wav'.format(i+1))
    
        len_data = len(data) # holds length of the numpy array
    
        t = len_data / sample_rate # returns duration but in floats
    
        hours, mins, seconds = output_duration(int(t))
        print('SoundFile{}'.format(i+1),'Total Duration: {}:{}:{}'.format(hours, mins, seconds))
    
    
    """
    for i in range(12):
        Alice_stm = data_path + "DownTheRabbitHoleFinal_SoundFile{}.wav".format(i+1)
        Script_Sound = sound.Sound(Alice_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        Script_Sound.play()#when = now + 0.5)  # play in EXACTLY 0.5s
        core.wait(60)  # how to solve the length difference between audio files?
        pass
    """    