#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']
"""
# Get a dictionary of all playback devices >> do this everytime we run the audio experiments
from psychopy.tools.systemtools import getAudioPlaybackDevices
from pprint import pprint 
device_list = getAudioPlaybackDevices()

print("\n--- Available Audio Playback Devices (via systemtools) ---")
pprint(device_list)
print("----------------------------------------------------------\n")

# For R605 audio experiment setting
from psychopy import prefs

# 1. Set the preferred audio library to PTB (or the one you want to use)
prefs.hardware['audioLib'] = ['PTB'] 
prefs.hardware['audioLatencyMode'] = 3

# 2. Assign the exact device name
# Note: Ensure you are using the correct characters (喇叭)
prefs.hardware['audioDevice'] = '喇叭 (Realtek(R) Audio)' 

# 3. Now you can import the sound module
#from psychopy import sound 

# Example: play a sound
# tone = sound.Sound(440, secs=0.5) 
# tone.play()



# Import ptb and other psychopy packages
import psychtoolbox as ptb
from psychopy import sound, core, visual, event, parallel, gui, monitors, clock   
#, parallel   # if you change the setting, this command must be put after the prefs's command
#import json
print(sound.Sound)

import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
#from pprint import pprint
import random

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

def display_ins(STR, keyPressLIST = None):
    '''
    設定欲呈現的字串及指定的反應鍵後，將會呈現字串，並需按下指定反應鍵才會進到下一個字串。
    若未指定反應鍵，則任意鍵皆可換下一張刺激
    i.e display("啦啦啦", ['space'])
    '''
    instructionsLIST = STR.split("\\\\")
    keyPressLIST = keyPressLIST

    for t in instructionsLIST:
        instructions = visual.TextStim(win = win, text = t)
        instructions.draw()
        win.flip()
        ansSTR = event.waitKeys(keyList = keyPressLIST)
        print(ansSTR)
    win.flip()
    return ansSTR

def display_fix():
    '''
    呈現"+"於螢幕中央
    '''
    fixation = visual.TextStim(win = win, text = "+")
    fixation.draw()
    win.flip()

def display_start():
    '''
    呈現"Start"於螢幕中央，暗示音檔即將要播出了。
    '''
    fixation = visual.TextStim(win = win, text = "Start")
    fixation.draw()
    win.flip()

"""
# For setting up the Trigger in NCU ICN Room608 EEG
n = 0
port = 'COM3'
baudRate = 115200
InputBufferSize = 8
readTimeout = 1
portSettings = 'BaudRate=%d InputBufferSize=%d Terminator=0 ReceiveTimeout=%f ReceiveLatency=0.0001'%(
    baudRate, InputBufferSize, readTimeout)

[handle, errmsg] = ptb.IOPort('OpenSerialPort', port, portSettings)
ptb.IOPort('Flush', handle)
"""

# This is the trigger port for R605 EEG
port = parallel.ParallelPort(address='0xE030')
port.setData(0)  # set all pins low

if __name__ == "__main__":
    data_path = "C:/Users/user/Desktop/Ting_R605 EEG Demo/" #"/Users/ting-hsin/Downloads/R605_EEG_SSAEP_MaterialsTest/"
    results_data_path = "C:/Users/user/Desktop/Ting_R605 EEG Demo/SSAEP_results/" #"/Users/ting-hsin/Downloads/R605_EEG_SSAEP_MaterialsTest/SSAEP_results/"

    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file

    # display fixation
    #display_fix()
    
    instructions = """接下來你會聽到一連串相同的單音重複出現，\n中間間隔將會隨機調整，\n請專心聆聽即可，\n當你準備好的時候，\n請按下空白鍵開始"""
    keypressLIST_space = ["space"]
    
    # SSAEP wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    ISI_FLOAT_LIST = []
    Trial_numLIST = []

    # key in number for notifying which subject it is
    sub_id = str(input("Subject: "))

    # Full screen
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    # Testing small screen
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")

    # display instructions
    display_ins(instructions, keypressLIST_space)

    for i in range(70):
        # display fixation for subject to look at when listening to the tape
        display_fix()
        
        # get the length of each audio files of Alice in the Wonderland Chapter one
        sample_rate, data = wavfile.read(data_path + 'am_40Hz.wav')
        len_data = len(data) # holds length of the numpy array
        t = len_data / sample_rate # returns duration but in floats
        
        port.setData(0)  # set all pins low
        # Play the audio files section by section
        fourtyHz_2s_stm = data_path + "am_40Hz.wav"
        Script_Sound = sound.Sound(fourtyHz_2s_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        port.setData(i+1)  # set all pins low
        Script_Sound.play()
        
        """
        # Produce 40 Hz Pure Tone that last 2s in numpy
        # Set parameters
        freq_Hz = 40
        duration_s = 2.0
        sample_rate_Hz = 44100

        # Set time axis
        t = np.linspace(0, duration_s, int(sample_rate_Hz*duration_s), endpoint=False)

        # Generate a sine waves
        tone = np.sin(2*np.pi*freq_Hz*t)
        
        # Let Psychopy play that tone
        sound_40Hz = sound.Sound(value=tone, sampleRate=sample_rate_Hz)
        sound_40Hz.play()
        """

        # set core wait time that match with the length of each audio files
        core.wait(int(t)) # second not milisecond
        port.setData(0)  # set all pins low

        win.flip()
        port.setData(i+1)  # set all pins low
        # Custimize the ISI from 200 ms to 1000 ms, with a 50 ms as the interval
        ISI_FLOAT = round(float(random.randrange(200, 1050, 50)*0.001), 4)
        print(ISI_FLOAT)
        core.wait(ISI_FLOAT)
        port.setData(i+1)  # set all pins low
        
        #port.setData(0)  # set all pins low
        
        # making the wanted info into the List form for future use
        sub_idLIST.append(sub_id)
        dateLIST.append(day)
        ISI_FLOAT_LIST.append(ISI_FLOAT)
        Trial_numLIST.append(i+1)
        """
        # Add ESC could core.quit() function in the middle of the experiments process
    """
    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             'Date':dateLIST,
                             'Trial_num':Trial_numLIST,
                             'ISI_second':ISI_FLOAT_LIST,
                             })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = sub_id + '_40Hz_results.csv'
    save_path = results_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    

    # close all the Psychopy application
    core.quit()
