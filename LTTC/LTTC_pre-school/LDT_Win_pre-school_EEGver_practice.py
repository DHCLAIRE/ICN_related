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
        instructions = visual.TextStim(win=win, text=t)
        instructions.draw()
        win.flip()
        event.waitKeys(keyList=keyPressLIST)
    win.flip()

def display_fix():
    '''
    呈現"+"於螢幕中央
    '''
    fixation = visual.TextStim(win=win, text="+")
    fixation.draw()
    win.flip()

# The EEG trigger port info
#port = serial.Serial("COM4", 115200)  # check the COM? every time we inpluge the trigger ; 115200 == how many bites were transmissed per second


if __name__ == "__main__":
    # key in number for notifying which subject it is
    sub_id = str(input("Subject_ID: "))

    # Set up the data path (For Win)
    #stim_data_path =  "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_LDT_practice_pw_audios/" #"/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_LDT_pw_audios/"
    #result_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id #"/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/"
    # the path for testing only (For Mac)
    stim_data_path =  "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_LDT_practice_pw_audios/"
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id
    
    # setting up usable dataLIST
    targetPseudoLIST = []
    pseudoLIST = []
    targetPseudoLIST = []
    """
    # Set up the pwDICT's data path
    DICT_name = 'S%s_pseudowordsDICT.json' %sub_id
    Dsave_path = result_data_path + DICT_name
    
    with open (Dsave_path, "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
        #print(pseudoDICT["High_CD condition pseudowords_3"])
        pseudoLIST.extend(pseudoDICT["The ControlPseudo group_6"])
        pseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])

        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])

        print(pseudoLIST)
    pass
    """
    pseudoLIST = ["daakaxl", "fayihng", "guwlihng", "kayfiy", "lowtaxst", "maasaxl"]

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

    # Step_1: Show the instructions
    # Setting the presented window
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()

    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到一連串的詞彙，\n請依照實驗指示進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵"""
    instructions_2 = """將你的手指輕放在空白鍵\n\n聽過請按空白鍵，沒聽過請不要按\n\n當詞彙播放完畢時\n請盡快且正確的進行按鍵反應"""  # 按鍵號碼需要再修
    keypressLIST_space = ['space']

    #Display the instructions
    display_ins(instructions_1, keypressLIST_space)
    display_ins(instructions_2, keypressLIST_space)


    # 假詞all重新排列後依序送出，整個LIST重複送10次
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for i in range(2):  #need to loop 10 times for a 120 total trials

        # randomly select the wanted pseudoword from the list
        random.shuffle(pseudoLIST)
        for stim_wordSTR in pseudoLIST:

            # To refresh the win before play out the stim pw
            win.flip()  # always add this after an item was presented
            core.wait(1)
            # start to record the time
            start_time = clock.getTime()

            # display fixation in the central of the screen
            display_fix()


            # Display the pw stimulus
            LTTC_pw_stm = stim_data_path + '{}.wav'.format(stim_wordSTR)
            pw_Sound = sound.Sound(LTTC_pw_stm)
            pw_Sound.play()

            """
            # TO MARK THE PSEUDOWORD APPEARED
            port.setData(8) #This is open the trigger  # MEG channel 195
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            """

            #setting up what keypress would allow the experiment to proceed
            keys = event.waitKeys(maxWait=2, keyList=keypressLIST_space) # only press "space" when you have heard this word
            event.getKeys(keyList=keypressLIST_space)
            print(keys)

            # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
            if keys == ["space"]:
                pass

            else:
                keys = ["None"]
                conditionLIST = ["N/A"]
                time_duration = 0
                print(time_duration)
                clock.reset()

            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            dateLIST.append(day)
            stimLIST.append(stim_wordSTR)
            resultKeyLIST.append(keys)

            # close the window  at the end of the experiment
    win.close()


    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             'Date':dateLIST,
                           'Stimuli':stimLIST,
                           'Keypress':resultKeyLIST
                           })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LDT_practice_results.csv' %sub_id
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen
