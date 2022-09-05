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
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
from pprint import pprint

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

if __name__ == "__main__":
    data_path = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/"
    results_data_path = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results/12Qs_Ans/"
    
    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file
    
    # display fixation
    #display_fix()
    instructions = """接下來你會聽到幾段故事，\n每段故事結束後會有一題單選題，\n請依照剛剛聽到的內容進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵開始"""
    questionsLIST = [
        "When Alice peeked into her sister's book on the bank, what did it NOT* have?\n1. No sign of her sister’s name.\n2. No pictures or conversations.\n3. No pages at all.\n4. No interesting story.",
        "What two things are immediately most striking to Alice about the rabbit?\n1. It is talking and won't respond to her.\n2. It has a waistcoast-pocket and a watch.\n3. It is running late and yelling loudly.\n4. It walks and talks just as a human.",
        "When Alice fell down the well, she took down a jar from one of the shelves as she passed. What was it labeled?\n1. Orange Marmalade\n2. Strawberry Marmalade\n3. Blueberry Jam\n4. Apricot Jam",
        "When Alice thinks she might have fallen right through the earth and come out among people that walk backwards, what countries does she think they are from?\n1. Argentina\n2. United States and Canada\n3. India\n4. Australia and New Zealand",
        "What is the name of Alice's cat?\n1. Selima\n2. Chester\n3. Dinah\n4. Felix",
        "What does Alice land on at the bottom of the well?\n1. The hard stone floor\n2. An overstuffed armchair\n3. A heap of sticks and dry leaves\n4. A large, purple couch",
        "What material is the key which Alice finds made of?\n1. Brass\n2. Silver\n3. Bronze\n4. Gold",
        "What device does Alice 'shut up like'?\n1. A telescope\n2. A clam\n3. A bite\n4. A lantern",
        "Drinking from the bottle has a variety of tastes. What does it NOT* taste like?\n1. Cherry tart\n2. Pineapple\n3. Tea\n4. Roast turkey",
        "What are the effects of drinking from the bottle and eating the cake?\n1. Drinking makes Alice smaller and eating makes her larger.\n2. Drinking makes Alice larger and eating makes her smaller.\n3. Both drinking and eating make her smaller.\n4. Both drinking and eating make her larger.",
        "Why did Alice box her own ears once?\n1. For checking out her new boxing gloves.\n2. For cheating herself in a game of croquet.\n3. For not knowing the capital of Bulgaria.\n4. For forgetting to give Dina her milk at tea-time.",
        "Where did Alice find the cake?\n1. Floating in the pond of her tears.\n2. In a little wooden box that was lying on the table.\n3. In a little glass box that was lying under the table.\n4. She did not find it -- the rabbit gave it to her."
    ]
    
    keypressLIST_space = ["space"]
    keypressLIST_ans = ["1", "2", "3", "4"]
    
    # Answer 12Qs wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    Ques_textLIST = []
    resultKeyLIST = []
    #correctnessLIST = []
    responseLIST = []
    Q_numLIST = []
    
    # key in number for notifying which subject it is
    sub_id = str(input("Subject: "))
    
    # Full screen
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    # Testing small screen
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    
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
        core.wait(0.5)
        """
        # TO MARK THE QUESTION BEGINS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(i+51)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        win.flip()
        # Display the quesitons for each tape
        ans_keypressSTR = display_ins(questionsLIST[i], keypressLIST_ans)

        """
        # TO MARK THE QUESTION ENDS
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(int(99)),np.uint8(0)]))  #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        ptb.IOPort('Write', handle, np.uint8([109,104,np.uint8(0),np.uint8(0)])) #This is close the trigger
        """
        
        # making the wanted info into the List form for future use
        sub_idLIST.append(sub_id)
        dateLIST.append(day)
        Ques_textLIST.append(questionsLIST[i])
        responseLIST.append(ans_keypressSTR)
        Q_numLIST.append(int(i+1))
        #correctnessLIST.append(correctLIST)

        # the Gap between each audio files
        #core.wait(5)
        print("Continue for the SoundFile{}".format(i+2))
        
        

        # Add ESC could core.quit() function in the middle of the experiments process
    print("FINISHIED!")
    # close the window  at the end of the experiment
    win.close()
    
    
    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             'Date':dateLIST,
                             'Q_num':Q_numLIST,
                             'Stimuli':Ques_textLIST,
                             'Response':responseLIST,
                             #'LDT_RT':LDT_rtLIST,
                             #'Correctness':correctnessLIST
                             })
    
    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = sub_id + '_12Qs_results.csv'
    save_path = results_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")


    # close all the Psychopy application
    core.quit()
