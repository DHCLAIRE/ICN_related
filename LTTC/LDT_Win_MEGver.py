#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
print(sound.Sound)

#import psychopy
#from psychopy import visual, core, event, clock, parallel
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
from pprint import pprint

'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
'''

# need to add feedbacks of scaling and texts records

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
1. instructions >> press 'space'?? or other button?
2. Button press >> one for each side (choose wisely)
"""

# The MEG trigger port info
#port = parallel.ParallelPort('0x0378')

if __name__ == "__main__":

    stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_LDT_pw_audios/" #"I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/"
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/"#"I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-results_selfPRT_PLDT/"

    # setting up usable dataLIST
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    words_high_CD_setLIST = []
    words_low_CD_setLIST = []
    PLDT_LIST = []

    # key in number for notifying which subject it is
    sub_id = str(input("Subject: "))

    #把pseudoDICT的值叫出來
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    words_high_CD_setLIST = []
    words_low_CD_setLIST = []


    DICT_name = 'S%s_pseudowordsDICT.json' %sub_id
    Dsave_path = result_data_path + DICT_name

    with open (Dsave_path, "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
        #print(pseudoDICT["High_CD condition pseudowords_3"])
        pseudoLIST.extend(pseudoDICT["The ControlPseudo group_6"])
        pseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])

        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        
        #print(pseudoLIST)
    pass


    # LDT Wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    resultKeyLIST = []
    stimLIST = []
    conditionLIST = []
    LDT_rtLIST = []
    correctnessLIST = []
    responseLIST = []
    correctLIST = []

    # key in number for notifying which subject it is
    #sub_id = str(input("Subject: "))

    # Step_1: Show the instructions
    # Setting the presented window
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()
    #start_time = clock.getTime()  >>change position to make the calculation correct

    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到一連串的詞彙，\n請依照實驗指示進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵"""
    instructions_2 = """將你的左食指輕放在1鍵，右食指輕放在2鍵。\n聽過請按1 沒聽過請按2\n當詞彙播放完畢時，請盡快且正確的進行按鍵反應。"""  # 按鍵號碼需要再修
    keypress = ['space']

    core.wait(3)

    #Display the instructions
    display_ins(instructions_1, keypress)
    display_ins(instructions_2, keypress)

    core.wait(3)

    # 假詞all重新排列後依序送出，整個LIST重複送10次
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for i in range(1):

        # randomly select the wanted pseudoword from the list
        random.shuffle(pseudoLIST)
        for stim_wordSTR in pseudoLIST:
            
            start_time = clock.getTime()
            
            """
            sample_rate, data = wavfile.read(stim_data_path + '{}.wav'.format(stim_wordSTR))
            len_data = len(data) # holds length of the numpy array
            t = len_data / sample_rate # returns duration but in floats
            print("SoundFile{} length = ".format(i+1), t)
            print("SoundFile{} length = ".format(i+1), int(t+1))
            """
            # display fixation in the central of the screen
            display_fix()
            #core.wait(1)
            
            # Display the pw stimulus
            LTTC_pw_stm = stim_data_path + '{}.wav'.format(stim_wordSTR)
            pw_Sound = sound.Sound(LTTC_pw_stm)
            pw_Sound.play()
            
            
            """
            # TO MARK THE PSEUDOWORD APPEARED
            port.setData(8) #This is open the trigger
            #core.wait(0.01) # Stay for 10 ms
            #port.setData(0) #This is close the trigger
            """
            win.flip()  # always add this after an item was presented

            #setting up what keypress would allow the experiment to proceed
            keys = event.waitKeys(maxWait = 3, keyList = ['1', '2'])
            event.getKeys(keyList = ['1', '2'])
            print(keys)

            # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
            if keys == ["1"]:
                conditionLIST = ["heard"]
                end_time = clock.getTime()
                time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                print(time_duration)
                #print(type(time_duration))
                clock.reset()

            elif keys == ["2"]:
                conditionLIST = ["unheard"]
                end_time = clock.getTime()
                time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                print(time_duration)
                #print(type(time_duration))
                clock.reset()

            else:
                keys = ["Wrong!!"]
                conditionLIST = ["N/A"]
                time_duration = 0
                print(time_duration)
                clock.reset()
            """
            # TO MARK THE PSEUDOWORD GONE
            #port.setData(8) #This is open the trigger
            #core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            """
            # calculate the correctness of the LDT response
            if stim_wordSTR in targetPseudoLIST:
                #conditionLIST = ["seen"]
                if keys == ["1"]:
                    correctLIST = ["True"]
                #conditionLIST = ["unseen"]
                elif keys == ["2"]:
                    correctLIST = ["False"]
                else:
                    correctLIST = ["N/A"]

            elif stim_wordSTR not in targetPseudoLIST:
                #conditionLIST = ["seen"]
                if keys == ["1"]:
                    correctLIST = ["False"]
                #conditionLIST = ["unseen"]
                elif keys == ["2"]:
                    correctLIST = ["True"]
                else:
                    correctLIST = ["N/A"]
            else:
                pass


            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            dateLIST.append(day)
            stimLIST.append(stim_wordSTR)
            resultKeyLIST.append(keys)
            responseLIST.append(conditionLIST)
            LDT_rtLIST.append(time_duration)
            correctnessLIST.append(correctLIST)

            #core.wait(0.5)

            # close the window  at the end of the experiment
    win.close()


    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                           'Date':dateLIST,
                           'Stimuli':stimLIST,
                           'Keypress':resultKeyLIST,
                           'Response':responseLIST,
                           'LDT_RT':LDT_rtLIST,
                           'Correctness':correctnessLIST
                           })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LDT_results.csv' %sub_id
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen