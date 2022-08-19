#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock  #, parallel   # if you change the setting, this command must be put after the prefs's command
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
        event.waitKeys(keyList = keyPressLIST)
    win.flip()

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
# For setting up the Trigger
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
# Full screen
#win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
# Testing small screen
win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix") 


if __name__ == "__main__":
    data_path = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/"
    
    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file
    
    # display fixation
    #display_fix()
    instructions = """接下來你會聽到幾段故事，\n每段故事結束後會有一題單選題，\n請依照剛剛聽到的內容進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵開始"""
    questionsLIST = ["When Alice peeked into her sister's book on the bank, what did it NOT* have?\na No sign of her sister’s name.\nb No pictures or conversations.\nc No pages at all.\nd No interesting story.", "What two things are immediately most striking to Alice about the rabbit?\na It is talking and won't respond to her.\nb It has a waistcoast-pocket and a watch.\nc It is running late and yelling loudly.\nd It walks and talks just as a human.", 'When Alice fell down the well, she took down a jar from one of the shelves as she passed. What was it labeled?\na "Orange Marmalade"\nb "Strawberry Marmalade"\nc "Blueberry Jam"\nd "Apricot Jam"', 'When Alice thinks she might have fell right through the earth and come out among people that walk backwards, what countries does she think they are from?\na Argentina\nb United States and Canada\nc India\nd Australia and New Zealand', 'What does Alice land on at the bottom of the well?\na The hard stone floor\nb An overstuffed armchair\nc A heap of sticks and dry leaves\nd A large, purple couch', "What is the name of Alice's cat?\na Selima\nb Chester\nc Dinah\nd Felix", 'What material is the key which Alice finds made of?\na Brass\nb Silver\nc Bronze\nd Gold', 'What device does Alice shut up like?\na A telescope\nb A clam\nc A bite\nd A lantern', 'What are the effects of drinking from the bottle and eating the cake?\na Drinking makes Alice smaller and eating makes her larger.\nb Drinking makes Alice larger and eating makes her smaller.\nc Both drinking and eating make her smaller.\nd Both drinking and eating make her larger.', 'Drinking from the bottle has a variety of tastes. What does it *NOT* taste like?\na Cherry tart\nb Pineapple\nc Tea\nd Roast turkey', 'Why did Alice box her own ears once?\na For checking out her new boxing gloves.\nb For cheating herself in a game of croquet.\nc For not knowing the capital of Bulgaria.\nd For forgetting to give Dina her milk at tea-time.', 'Where did Alice find the cake?\na Floating in the pond of her tears.\nb In a little wooden box that was lying on the table.\nc In a little glass box that was lying under the table.\nd She did not find it -- the rabbit gave it to her.']
    keypressLIST_space = ["space"]
    keypressLIST_ans = ["a", "b", "c", "d"]
    
    # display instructions
    display_ins(instructions, keypressLIST_space)
    
    for i in range(2):
        
        # display "Start" to indicate the start of the audio
        display_start()
        core.wait(1)
        
        # display fixation for subject to look at when listening to the tape
        display_fix()
        
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
        
        """
        # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(i+1)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        # set core wait time that match with the length of each audio files
        
        core.wait(int(t+1))
        
        """
        # TO MARK THE AUDIO FILE ENDS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(99),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """        
        
        print("SoundFile{}".format(i+1), "DONE")
        #print("Pause for 5 seconds.")
        
        """
        # TO MARK THE QUESTION BEGINS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(i+50)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        win.flip()
        # Display the quesitons for each tape
        display_ins(questionsLIST[i], keypressLIST_ans)
        
        """
        # TO MARK THE QUESTION ENDS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(99)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        
        # the Gap between each audio files
        #core.wait(5)
        print("Continue for the SoundFile{}".format(i+2))
        
        # Add ESC could core.quit() function in the middle of the experiments process
        
    
    print("FINISHIED!")
    core.quit()
    
