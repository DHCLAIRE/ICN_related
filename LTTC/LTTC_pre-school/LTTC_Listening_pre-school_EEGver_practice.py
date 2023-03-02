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
    #stim_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id #"E:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"  #"/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/S%s_audios/" %(sub_id, sub_id)
    #result_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id #"E:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/"
    
    # the path for testing only (For Mac)
    root_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_pre-school")
    target_w_stim_data_path = root_data_path / "LDT-8 target words"
    result_data_path = root_data_path / "LTTC_pre-school_results"
    result_data_path.mkdir(exist_ok=True)
    
    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到幾段文章，文章結束後，\n並依照實驗指示進行按鍵反應。\n\n當你準備好的時候，\n將開始實驗"""
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
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    # Testing small screen
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    '''
    LTTC_audio_stm = stim_data_path + "S001_modified_1.wav" #% (sub_id, tape_numSTR)
    Script_Sound = sound.Sound(LTTC_audio_stm)   #value=str(Alice_stm), secs = 60)
    Script_Sound.play()
    core.wait(20)
    '''
    ## The path needs to be modified ##
    # For key-in the id of the subject
    sub_id = str(input("Subject: "))
    sub_cond = str(input("Condition: "))
    
    story_stim_data_path =  root_data_path / Path("LTTC-stories/Set_%s" %sub_cond)
    if sub_cond == "A":
        print(story_stim_data_path)
        audio_stimLIST = [path.name for path in story_stim_data_path.iterdir() if re.match(r'Set_A_', path.name)]
        print(audio_stimLIST)
        print(len(audio_stimLIST))
        
    elif sub_cond == "B":
        print(story_stim_data_path)
        audio_stimLIST = [path.name for path in story_stim_data_path.iterdir() if re.match(r'Set_B_', path.name)]
        print(audio_stimLIST)
        print(len(audio_stimLIST))
    
    random.shuffle(audio_stimLIST)
    
    ## To group the stimLIST per 3 tape
    item_numINT = 3
    n_audio_stimLIST = []
    for tape_count in range(0, len(audio_stimLIST), item_numINT):
        tmp_stimLIST = audio_stimLIST[tape_count:tape_count+item_numINT]
        n_audio_stimLIST.append(tmp_stimLIST)
    pprint(n_audio_stimLIST)
    print(len(n_audio_stimLIST))
    
    """
    for i in range(2):  # need to loop a total 3 times

        # display instructions for Reading Comprehension phase
        display_ins(instructions_1, keypressLIST_space)
        #win.flip()
        core.wait(0.5)

        for tapeINT in range(2): # need to loop a total 10 times

            # display "Start" to indicate the start of the audio
            display_start()
            core.wait(1)

            # display fixation for subject to look at when listening to the tape
            display_fix()

            # This is the tape num creation
            tape_numSTR = str(int("%d%d" %(i, tapeINT))+1)

            # get the length of each audio files of every text
            sample_rate, data = wavfile.read(story_stim_data_path + "S%s_modified_%s.wav" % (sub_id, tape_numSTR))   # the %s value in here will need to rewrite
            len_data = len(data) # holds length of the numpy array
            t = len_data / sample_rate # returns duration but in floats
            print("SoundFile{} length = ".format(tape_numSTR), t)
            print("SoundFile{} length = ".format(tape_numSTR), int(t+1))

            # Play the audio files section by section
            LTTC_audio_stm = stim_data_path + "S%s_modified_%s.wav" % (sub_id, tape_numSTR)
            Script_Sound = sound.Sound(LTTC_audio_stm)   #value=str(Alice_stm), secs = 60)
            Script_Sound.play()

            '''
            # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
            port.setData(2) #This is open the trigger  # MEG channel 193
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            # set core wait time that match with the length of each audio files
            core.wait(10)  #int(t+1))

            '''
            # TO MARK THE AUDIO FILE ENDS
            port.setData(4) #This is open the trigger  # MEG channel 194
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''

            print("SoundFile{}".format(tape_numSTR), "DONE")
            #print("Pause for 5 seconds.")
            core.wait(0.5)

            '''
            # TO MARK THE QUESTION BEGINS
            port.setData(8) #This is open the trigger  # MEG channel 195
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            win.flip()

            # Display the quesitons for each tape
            ans_keypressSTR = display_ins(instructions_2, keypressLIST_space)
            '''
            # TO MARK THE QUESTION ENDS
            port.setData(4) #This is open the trigger  # MEG channel 194
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            dateLIST.append(day)
            responseLIST.append(ans_keypressSTR)

            # the Gap between each audio files
            #core.wait(5)
            print("Continue for the SoundFile{}".format(int(tape_numSTR)+1))
        # ask the participant to evaluate how well they understand the presented text
        if i == 1:
            display_ins(instructions_4, keypressLIST_space)  # End of experiment
        else:
            display_ins(instructions_3, keypressLIST_space)  # 1 miute break


    print("FINISHIED!")
    # close the window  at the end of the experiment
    win.close()

    '''
    ## LET IT SILDE RIGHT NOW
    # setting up what keypress would allow the experiment to proceed
    keys = event.waitKeys(keyList = keypressLIST_ans)
    event.getKeys(keyList = keypress)
    print(keys)
    print("audio ends")
    if keys == ["space"]:
        end_time = clock.getTime()
        time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
        print(time_duration)
        print(type(time_duration))
        clock.reset()
    else:
        pass  # we should use continue in here, right?
    '''

    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             'Date':dateLIST,
                             'Response':responseLIST
                             })

    '''
    # TRY TO OPEN THE CSV FILE COMMAND
    with open(result_data_path + "S%s_Listening_task.csv" %sub_id, "r", encoding="UTF-8", newline='') as csvfile:
        result_csv = csvfile.read.split("\n")
        print(cs)
    '''

    # Save the file
    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LTTC_Listening_practice_results.csv' %sub_id
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    """

    # close all the Psychopy application
    core.quit()
