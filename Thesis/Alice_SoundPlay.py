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
    questionsLIST = ["1\tWhen Alice peeked into her sister's book on the bank, what did it NOT* have?\n", 'a\tNo sign of her sister’s name.\n', 'b\tNo pictures or conversations.\n', 'c\tNo pages at all.\n', 'd\tNo interesting story.\n', 'Answer\tb\n', '\t\n', '2\tWhat two things are immediately most striking to Alice about the rabbit?\n', "a\tIt is talking and won't respond to her.\n", 'b\tIt has a waistcoast-pocket and a watch.\n', 'c\tIt is running late and yelling loudly.\n', 'd\tIt walks and talks just as a human.\n', 'Answer\tb\n', '\t\n', '3\tWhen Alice fell down the well, she took down a jar from one of the shelves as she passed. What was it labeled?\n', 'a\t"Orange Marmalade"\n', 'b\t"Strawberry Marmalade"\n', 'c\t"Blueberry Jam"\n', 'd\t"Apricot Jam"\n', 'Answer\ta\n', '\t\n', '4\tWhen Alice thinks she might have fell right through the earth and come out among people that walk backwards, what countries does she think they are from?\n', 'a\tArgentina\n', 'b\tUnited States and Canada\n', 'c\tIndia\n', 'd\tAustralia and New Zealand\n', 'Answer\td\n', '\t\n', '5\tWhat does Alice land on at the bottom of the well?\n', 'a\tThe hard stone floor\n', 'b\tAn overstuffed armchair\n', 'c\tA heap of sticks and dry leaves\n', 'd\tA large, purple couch\n', 'Answer\tc\n', '\t\n', "6\tWhat is the name of Alice's cat?\n", 'a\tSelima\n', 'b\tChester\n', 'c\tDinah\n', 'd\tFelix\n', 'Answer\tc\n', '\t\n', '7\tWhat material is the key which Alice finds made of?\n', 'a\tBrass\n', 'b\tSilver\n', 'c\tBronze\n', 'd\tGold\n', 'Answer\td\n', '\t\n', '8\tWhat device does Alice "shut up like"?\n', 'a\tA telescope\n', 'b\tA clam\n', 'c\tA bite\n', 'd\tA lantern\n', 'Answer\ta\n', '\t\n', '9\tWhat are the effects of drinking from the bottle and eating the cake?\n', 'a\tDrinking makes Alice smaller and eating makes her larger.\n', 'b\tDrinking makes Alice larger and eating makes her smaller.\n', 'c\tBoth drinking and eating make her smaller.\n', 'd\tBoth drinking and eating make her larger.\n', 'Answer\ta\n', '\t\n', '10\tDrinking from the bottle has a variety of tastes. What does it *NOT* taste like?\n', 'a\tCherry tart\n', 'b\tPineapple\n', 'c\tTea\n', 'd\tRoast turkey\n', 'Answer\tc\n', '\t\n', '11\tWhy did Alice box her own ears once?\n', 'a\tFor checking out her new boxing gloves.\n', 'b\tFor cheating herself in a game of croquet.\n', 'c\tFor not knowing the capital of Bulgaria.\n', 'd\tFor forgetting to give Dina her milk at tea-time.\n', 'Answer\tb\n', '\t\n', '12\tWhere did Alice find the cake?\n', 'a\tFloating in the pond of her tears.\n', 'b\tIn a little wooden box that was lying on the table.\n', 'c\tIn a little glass box that was lying under the table.\n', 'd\tShe did not find it -- the rabbit gave it to her.\n', 'Answer\tc']
    keypressLIST = ["space"] #["a", "b", "c", "d"]
    
    for i in range(2):
        
        # display fixation
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
        
        # set core wait time that match with the length of each audio files
        core.wait(int(t+1))
        
        
        """
        # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(i+1)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        # Display the quesitons per tape
        display_ins(questionsLIST[i], keyPressLIST= keypressLIST)
        
        
        print("SoundFile{}".format(i+1), "DONE")
        print("Pause for 5 seconds.")
        
        """
        # TO MARK THE AUDIO FILE ENDS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(99),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        
        
        
        
        # the Gap between each audio files
        core.wait(5)
        print("Continue for the SoundFile{}".format(i+2))
        
        
        
        
        
        
        
        # Add ESC could core.quit() function in the middle of the experiments process
        
    
    print("FINISHIED!")
    core.quit()
    
