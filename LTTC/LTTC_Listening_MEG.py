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

# The MEG trigger port info
#port = parallel.ParallelPort('0x0378')

if __name__ == "__main__":

    ## The path needs to be modified ##
    # For key-in the id of the subject
    sub_id = str(input("Subject: "))

    stim_data_path = "E:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/" #"I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/" #%(sub_id, sub_id) #"/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/S%s_audios/" %(sub_id, sub_id)
    result_data_path = "E:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/" #"I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/" #%sub_id

    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到幾段文章，\n每段文章結束後，請依照剛剛聽到的內容進行理解度評分，\n請依照實驗指示進行按鍵反應，\n當你準備好的時候，\n實驗將會直接開始"""  #"""接下來你會聽到幾段文章，\n每段文章結束後會需要請你評分，\n請依照剛剛聽到的內容進行理解度評分，\n中間會有休息時間，\n請按下空白鍵開始"""
    instructions_2 = """請問對於剛剛那一篇文章理解了多少？\n請以1～4分評分，\n1分為完全不理解，4分為非常理解\n評分完畢後，將會直接播放下一篇文章\n請評分"""  #"""請問對於剛剛那一篇文章理解了多少？\n請以1～4分評分，\n1分為完全不理解，4分為非常理解\n評分完畢後，將會直接播放下一篇文章\n請評分"""
    instructions_3 = """現在為2分鐘的休息時間\n請稍作休息，\n您準備好後，將會開始播放下一階段的文章"""
    instructions_4 = """本實驗結束，謝謝您的參與"""

    # Set up the keypress types
    keypressLIST_space = ["space"]
    keypressLIST_ans = ["1", "2", "3", "4"]

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
    #"""
    for i in range(2):  # need to loop a total 3 times

        # display instructions for Reading Comprehension phase
        display_ins(instructions_1, keypressLIST_space)
        #win.flip()
        core.wait(0.5)

        for tapeINT in range(1): # need to loop a total 10 times

            # display "Start" to indicate the start of the audio
            display_start()
            core.wait(1)

            # display fixation for subject to look at when listening to the tape
            display_fix()

            # This is the tape num creation
            tape_numSTR = str(int("%d%d" %(i, tapeINT))+1)

            # get the length of each audio files of every text
            sample_rate, data = wavfile.read(stim_data_path + "S%s_modified_%s.wav" % (sub_id, tape_numSTR))   # the %s value in here will need to rewrite
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
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            # set core wait time that match with the length of each audio files
            core.wait(int(t+1))

            '''
            # TO MARK THE AUDIO FILE ENDS
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''

            print("SoundFile{}".format(i+1), "DONE")
            #print("Pause for 5 seconds.")
            core.wait(0.5)

            '''
            # TO MARK THE QUESTION BEGINS
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            win.flip()

            # Display the quesitons for each tape
            ans_keypressSTR = display_ins(instructions_2, keypressLIST_ans)
            '''
            # TO MARK THE QUESTION ENDS
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            '''
            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            dateLIST.append(day)
            responseLIST.append(ans_keypressSTR)

            # the Gap between each audio files
            #core.wait(5)
            print("Continue for the SoundFile{}".format(i+2))
        # ask the participant to evaluate how well they understand the presented text
        display_ins(instructions_3, keypressLIST_space)
    display_ins(instructions_4, keypressLIST_space)


    print("FINISHIED!")
    # close the window  at the end of the experiment
    win.close()

    '''
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

    # Save the file
    file_name = 'S%s_Listening_results.csv' %sub_id
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    '''
    # TRY TO OPEN THE CSV FILE COMMAND
    with open(result_data_path + "S%s_Listening_task.csv" %sub_id, "r", encoding="UTF-8", newline='') as csvfile:
        result_csv = csvfile.read.split("\n")
        print(cs)
    '''

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LTTC_Listening_results.csv' %sub_id
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    #"""

    # close all the Psychopy application
    core.quit()
