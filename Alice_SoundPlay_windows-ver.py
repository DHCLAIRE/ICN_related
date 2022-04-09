#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock #, parallel   # if you change the setting, this command must be put after the prefs's command
#import json
print(sound.Sound)

import scipy
from scipy.io import wavfile
import numpy as np

"""
# function to convert the information into
# some readable format
def output_duration(length):
    hours = length // 3600 # calculate in hours
    length %= 3600
    mins = length // 60 # calculate in minutes
    length %= 60
    seconds = length # calculate in seconds

    return hours, mins, seconds
"""

# 想想要如何同時撥出十字和音檔 >> or not
def display_fix():
    '''
    呈現"+"於螢幕中央
    '''
    fixation = visual.TextStim(win = win, text = "+")
    fixation.draw()
    win.flip()


# For setting up the Trigger?? >> I guess
n = 0
port = 'COM3'
baudRate = 115200
InputBufferSize = 8
readTimeout = 1
portSettings = 'BaudRate=%d InputBufferSize=%d Terminator=0 ReceiveTimeout=%f ReceiveLatency=0.0001'%(
    baudRate, InputBufferSize, readTimeout)

[handle, errmsg] = ptb.IOPort('OpenSerialPort', port, portSettings)
ptb.IOPort('Flush', handle)

win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full

if __name__ == "__main__":
    data_path = "E:/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/"

    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file


    display_fix()

    for i in range(12):

        # get the length of each audio files of Alice in the Wonderland Chapter one
        sample_rate, data = wavfile.read(data_path + 'DownTheRabbitHoleFinal_SoundFile{}.wav'.format(i+1))
        len_data = len(data) # holds length of the numpy array
        t = len_data / sample_rate # returns duration but in floats
        print("SoundFile{} length = ".format(i+1), t)
        print("SoundFile{} length = ".format(i+1), int(t+1))

        # Play the audio files section by section
        Alice_stm = data_path + "DownTheRabbitHoleFinal_SoundFile{}.wav".format(i+1)
        Script_Sound = sound.Sound(Alice_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        Script_Sound.play()
        
        # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(i+1)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger

        core.wait(int(t+1))  # switch this num into the length of each audio files

        print("SoundFile{}".format(i+1), "DONE")
        print("Pause for 5 seconds.")

        # TO MARK THE AUDIO FILE ENDS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(99),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger

        # the Gap between each audio files
        core.wait(5)

        print("Continue for the SoundFile{}".format(i+2))

    print("FINISHIED!")
    core.quit()
