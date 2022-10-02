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

# The MEG trigger port info
port = parallel.ParallelPort('0x0378')

if __name__ == "__main__":
    
    ## The path needs to be modified ##
    
    #stim_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"
    stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"  # Testing
    #result_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-results_selfPRT_PLDT/"
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/"  # Testing
    #text_data_path = "C:/Users/user/Documents/DINGHSIN/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/"
    textSets_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets/"
    #C:/Users/user/Documents/DINGHSIN/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets
    
    instructions_1 = """接下來你會聽到幾段文章，\n每段文章結束後會需要請你評分，\n請依照剛剛聽到的內容進行理解度評分，\n中間會有休息時間，\n請按下空白鍵開始"""    # Need to think about it
    instructions_2 = """請問對於剛剛那一篇文章理解了多少？\n請以1～4分評分，\n1分為完全不理解，4分為非常理解\n評分完畢後，將會直接播放下一篇文章\n請評分"""

    keypressLIST_space = ["space"]
    keypressLIST_ans = ["1", "2", "3", "4"]

    # Answer wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    resultKeyLIST = []
    responseLIST = []

    # key in number for notifying which subject it is
    sub_id = str(input("Subject: "))

    # Full screen
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    # Testing small screen
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")

    # display instructions
    display_ins(instructions_1, keypressLIST_space)


    for i in range(2):    # should be 30

        # display "Start" to indicate the start of the audio
        display_start()
        core.wait(1)

        # display fixation for subject to look at when listening to the tape
        display_fix()

        # get the length of each audio files of every text
        sample_rate, data = wavfile.read(stim_data_path + 'S%s_textaudio_%d.wav' %(sub_id, i+1))
        len_data = len(data) # holds length of the numpy array
        t = len_data / sample_rate # returns duration but in floats
        print("SoundFile{} length = ".format(i+1), t)
        print("SoundFile{} length = ".format(i+1), int(t+1))

        # Play the audio files section by section
        LTTC_stm = stim_data_path + "S%s_textaudio_%d.wav" %(sub_id, i+1)
        Script_Sound = sound.Sound(LTTC_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        Script_Sound.play()
        
        """
        # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger
        """
        # set core wait time that match with the length of each audio files
        core.wait(int(t+1))
        """
        # TO MARK THE AUDIO FILE ENDS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger
        """

        print("SoundFile{}".format(i+1), "DONE")
        #print("Pause for 5 seconds.")
        core.wait(0.5)

        """
        # TO MARK THE QUESTION BEGINS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger
        """
        win.flip()

        # Display the quesitons for each tape
        ans_keypressSTR = display_ins(instructions_2, keypressLIST_ans)
        """
        # TO MARK THE QUESTION ENDS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger
        """
        # making the wanted info into the List form for future use
        sub_idLIST.append(sub_id)
        dateLIST.append(day)
        responseLIST.append(ans_keypressSTR)

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
                             'Response':responseLIST
                             })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = sub_id + '_LTTC_Listening_results.csv'
    save_path = results_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the Psychopy application
    core.quit()