#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
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
import random
import re
from pathlib import Path
import serial

def display_ins(STR, keyPressLIST = None):
    '''
    設定欲呈現的字串及指定的反應鍵後，將會呈現字串，並需按下指定反應鍵才會進到下一個字串。
    若未指定反應鍵，則任意鍵皆可換下一張刺激
    i.e display("啦啦啦", ['space'])
    '''
    instructionsLIST = STR.split("\\\\")
    keyPressLIST = keyPressLIST

    for t in instructionsLIST:
        instructions = visual.TextStim(win=win, text=t)
        instructions.draw()
        win.flip()
        ansSTR = event.waitKeys(keyList=keyPressLIST)
        print(ansSTR)
        win.flip()
    return ansSTR

def display_fix():
    '''
    呈現"+"於螢幕中央
    '''
    fixation = visual.TextStim(win=win, text="+")
    fixation.draw()
    win.flip()

def display_start():
    '''
    呈現"Start"於螢幕中央，暗示音檔即將要播出了。
    '''
    fixation = visual.TextStim(win=win, text="Start")
    fixation.draw()
    win.flip()

# The EEG trigger port info
#port = serial.Serial("COM4", 115200)  # check the COM? every time we inpluge the trigger ; 115200 == how many bites were transmissed per second

if __name__ == "__main__":
    ## The path needs to be modified ##
    # For key-in the id of the subject
    sub_id = str(input("Subject: "))
    sub_cond = str(input("Condition: "))
    
    # Set up the data path (For Win)
    root_data_path = Path("D:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_pre-school")
    target_w_stim_data_path = root_data_path / "LDT-8 target words"
    result_data_path = root_data_path / "LTTC_pre-school_results"
    result_data_path.mkdir(exist_ok=True)
   
    # the path for testing only (For Mac)
    #root_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_pre-school")
    #target_w_stim_data_path = root_data_path / "LDT-8 target words"
    #result_data_path = root_data_path / "LTTC_pre-school_results"
    #result_data_path.mkdir(exist_ok=True)
    
    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到幾段文章，文章結束後，\n請依照實驗指示進行按鍵反應。\n\n當你準備好的時候，\n實驗將開始"""
    instructions_2 = """請問有聽懂剛剛那一篇文章嗎？\n\n評分完畢後，將會直接播放下一篇文章"""
    instructions_3 = """現在為1分鐘的休息時間\n請稍作休息，\n休息好後請跟我們說"""
    instructions_4 = """本實驗結束，謝謝您的參與"""

    # Set up the keypress types
    keypressLIST_space = ["space"]
    #keypressLIST_ans = ["6", "7", "8", "9"]  # "6"==1分; "7"==2分; "8"==3分; "9"==4分 (右手由上往下的順序)

    # Answer wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    resultKeyLIST = []
    responseLIST = []

    # Full screen
    win = visual.Window(size=[500, 500], color=[-1, -1, -1], units="pix")   #, fullscr=True)   # Present screen_Full, fullscr == [1280 1024](for MEG)
    #win = visual.Window(color=[-1, -1, -1], units="pix", fullscr=True)
    # Testing small screen
    #win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    
    ## To collect the stim base on the conditions
    story_stim_data_path =  root_data_path / Path("LTTC-stories/Set_%s" %sub_cond)
    if sub_cond == "A":
        print(story_stim_data_path)
        audio_stimLIST = [path.name for path in story_stim_data_path.iterdir() if re.match(r'Set_A_', path.name)]
        #print(audio_stimLIST)
        #print(len(audio_stimLIST))
        
    elif sub_cond == "B":
        print(story_stim_data_path)
        audio_stimLIST = [path.name for path in story_stim_data_path.iterdir() if re.match(r'Set_B_', path.name)]
        #print(audio_stimLIST)
        #print(len(audio_stimLIST))
    
    ## Random shuffle the tape
    random.shuffle(audio_stimLIST)
    
    ## To group the stimLIST per 3 tape
    item_numINT = 3
    n_audio_stimLIST = []
    for tape_count in range(0, len(audio_stimLIST), item_numINT):
        tmp_stimLIST = audio_stimLIST[tape_count:tape_count+item_numINT]
        n_audio_stimLIST.append(tmp_stimLIST)
    pprint(n_audio_stimLIST)
    #print(len(n_audio_stimLIST))
    
    # Set up the tape num according to the block design
    #numLIST = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

    #"""
    for i in range(4):  # need to loop a total 4 times

        # display instructions for Reading Comprehension phase
        display_ins(instructions_1, keypressLIST_space)
        #win.flip()
        core.wait(0.5)

        for tapeINT in range(3): # need to loop a total 3 times == 3 tapes per unit

            # display "Start" to indicate the start of the audio
            display_start()
            core.wait(1)

            # display fixation for subject to look at when listening to the tape
            display_fix()

            # This is the tape num creation
            tape_numSTR = str(n_audio_stimLIST[i][tapeINT])  #str(int("%d%d" %(i, tapeINT))+1)
            print(tape_numSTR[0:11])
            
            # get the length of each audio files of every text
            sample_rate, data = wavfile.read(story_stim_data_path / Path(tape_numSTR))   # the %s value in here will need to rewrite
            len_data = len(data) # holds length of the numpy array
            t = len_data / sample_rate # returns duration but in floats
            print("SoundFile{} length = ".format(tape_numSTR[0:11]), t)
            print("SoundFile{} length = ".format(tape_numSTR[0:11]), int(t+1))

            # Play the audio files section by section
            LTTC_audio_stm = story_stim_data_path / Path(tape_numSTR)
            Script_Sound = sound.Sound(LTTC_audio_stm)   #value=str(Alice_stm), secs = 60)
            Script_Sound.play()
            
            '''
            # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
            port.write(b'1') #This is the num_tag for opening the trigger
            core.wait(.01); # Stay for 10 ms
            '''
            
            # set core wait time that match with the length of each audio files
            core.wait(5) #(int(t+1))

            '''
            # TO MARK THE AUDIO FILE ENDS
            port.write(b'9') #This is the num_tag for opening the trigger
            core.wait(.01); # Stay for 10 ms
            '''

            print("SoundFile{}".format(tape_numSTR[0:11]), "DONE")
            print("Pause for 5 seconds.")
            core.wait(0.5)

            '''
            # TO MARK THE QUESTION BEGINS
            port.write(b'4') #This is the num_tag for opening the trigger
            core.wait(.01); # Stay for 10 ms
            '''
            win.flip()

            # Display the quesitons for each tape
            ans_keypressSTR = display_ins(instructions_2, keypressLIST_space)
            '''
            # TO MARK THE QUESTION ENDS
            port.write(b'9') #This is the num_tag for opening the trigger
            core.wait(.01); # Stay for 10 ms
            '''
            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            dateLIST.append(day)
            responseLIST.append(ans_keypressSTR)

            # the Gap between each audio files
            #core.wait(5)
            #print("Continue for the SoundFile{}".format(int(tape_numSTR)+1))
        # ask the participant to evaluate how well they understand the presented text
        if i == 3:
            display_ins(instructions_4, keypressLIST_space)  # End of experiment
        else:
            display_ins(instructions_3, keypressLIST_space)  # 1 miute break


    print("FINISHIED!")
    # close the window  at the end of the experiment
    win.close()


    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             'Date':dateLIST,
                             'Response':responseLIST
                             })

    # Save the file
    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LTTC_pre-school_testing_results.csv' %sub_id
    save_path = result_data_path / Path(file_name)
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    #"""
    # close all the Psychopy application
    core.quit()
