#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

#import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
import json
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

"""
1. instructions >> press 'space'?? or other button?
2. Button press >> one for each side (choose wisely)
"""

# The EEG trigger port info
#port = serial.Serial("COM4", 115200)  # check the COM? every time we inpluge the trigger ; 115200 == how many bites were transmissed per second

if __name__ == "__main__":
    # key in number for notifying which subject it is
    sub_type = str(input("Group type: "))
    sub_id = str(input("Subject: "))
    sub_cond = str(input("Condition: "))

    # Set up the data path (For Win)
    #root_data_path = Path("D:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_preschool")
    #result_data_path = root_data_path / "LTTC_preschool_results"
    #result_data_path.mkdir(exist_ok=True)
    
    # the path for testing only (For Mac)
    root_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_preschool")
    target_w_stim_data_path = root_data_path / "LDT-8_target_words"
    result_data_path = root_data_path / Path("LTTC_preschool_results/%s_Sub%s" %(sub_type, sub_id))
    result_data_path.mkdir(exist_ok=True)
    
    # setting up usable dataLIST
    targetPseudoLIST = []
    pseudoLIST = []
    targetPseudoLIST = []

    # Set up the pws' data path, and Call out the pw's LIST by the audios' names
    pw_stimLIST = [path.name for path in target_w_stim_data_path.iterdir() if re.match(r'\D', path.name)]  #(both works)\D == any non-digits; \w == any characters(digits included)
    print(pw_stimLIST) # pw_stimLIST = ['bi4_ba2.wav', 'bo4_luo2.wav', 'chai2_fei1.wav', 'ge2_lu3.wav', 'ji3_an4.wav', 'pu2_zu2.wav', 'sheng1_chu4.wav', 'zhai1_tan2.wav']
    '''
    # This is just for testing the re commands
    for path in target_w_stim_data_path.iterdir():
        if re.match(r'\w', path.name):  # path.name == the name of the file in the specfic location
            print(path.suffix)  # path.suffix == the file type of the file in the specfic location
            print(type(path.suffix))
    '''
    # This the every pseudowords audio file name
    #pseudoLIST = pw_stimLIST.copy()
    #print(pseudoLIST)
    for f_nameSTR in pw_stimLIST:
        pseudoLIST.append(f_nameSTR[:-4])  # exclude the file extension
    print(pseudoLIST)
    
    # ALL target PWs
    targetPseudoLIST = ['bo4_luo2', 'ji3_an4', 'pu2_zu2', 'sheng1_chu4']   #[簸籮, 几案, 蹼足, 牲畜]
    # Paired target PWs
    pair_1pw_LIST = ['sheng1_chu4', 'ji3_an4']  #[牲畜, 几案] = Set_A's HCD / Set_B's LCD
    pair_2pw_LIST = ['bo4_luo2', 'pu2_zu2']  #[簸籮, 蹼足] = Set_A's LCD / Set_H's LCD
    
    # LDT Wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    sub_condLIST = []
    resultKeyLIST = []
    stimLIST = []
    CD_condLIST = []
    conditionLIST = []
    LDT_rtLIST = []
    correctnessLIST = []
    responseLIST = []
    correctLIST = []
    roundLIST = []

    # key in number for notifying which subject it is
    #sub_id = str(input("Subject: "))

    # Step_1: Show the instructions
    # Setting the presented window
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()
    #start_time = clock.getTime()  >>change position to make the calculation correct

    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到一連串的詞彙，\n請依照實驗指示進行按鍵反應，\n當你準備好的時候，\n實驗將準備開始"""
    instructions_2 = """將你的手指輕放在空白鍵\n\n聽過請按空白鍵，沒聽過請不要按\n\n當詞彙播放完畢時\n請盡快且正確的進行按鍵反應"""  # 按鍵號碼需要再修
    instructions_3 = """中場休息1分鐘"""
    instructions_4 = """本實驗結束，謝謝！"""
    keypressLIST_space = ['space']
    keypressLIST_enter = ["return"]
    #keypressLIST_ans = ['1', '6']  #'1' == Left_hand == unheard; '6' == Right_hand == heard

    #core.wait(3)

    #Display the instructions
    display_ins(instructions_1, keypressLIST_enter)
    display_ins(instructions_2, keypressLIST_enter)

    #core.wait(3)

    # 假詞all重新排列後依序送出，整個LIST重複送2次
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for round_ in range(1, 3):  # only 2 rounds
        print("Please ready for Round", round_)
        """
        ## To mark the round number  ##
        port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
        core.wait(.01); # Stay for 10 ms
        """        
        for i in range(1):  #need to loop 6 times for 48 trials in one round (96 trials in total)

            # randomly select the wanted pseudoword from the list
            random.shuffle(pseudoLIST)
            for stim_wordSTR in pseudoLIST:

                # To refresh the win before play out the stim pw
                win.flip()  # always add this after an item was presented
                core.wait(2)
                # start to record the time
                start_time = clock.getTime()

                # display fixation in the central of the screen
                display_fix()


                # Display the pw stimulus
                LTTC_pw_stm = target_w_stim_data_path / Path('{}.wav'.format(stim_wordSTR))
                pw_Sound = sound.Sound(LTTC_pw_stm)
                pw_Sound.play()

                """
                # TO MARK THE PSEUDOWORD APPEARED
                port.write(b'1') #This is the num_tag for opening the trigger
                core.wait(.01); # Stay for 10 ms
                """

                #setting up what keypress would allow the experiment to proceed
                keys = event.waitKeys(maxWait=5, keyList=keypressLIST_space) # only press "space" when you have heard this word
                event.getKeys(keyList=keypressLIST_space)
                print(keys)
                
                # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
                if keys == ["space"]:
                    conditionLIST = ["heard"]
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()

                else:
                    keys = ["None"]
                    conditionLIST = ["unheard"]
                    time_duration = 0
                    print(time_duration)
                    clock.reset()

                
                # calculate the correctness of the LDT response
                if stim_wordSTR in targetPseudoLIST:
                    #conditionLIST = ["heard"]
                    if keys == ["space"]:
                        correctLIST = ["True"]
                    #conditionLIST = ["unheard"]
                    elif keys == ["None"]:
                        correctLIST = ["False"]
                    else:
                        correctLIST = ["N/A"]

                elif stim_wordSTR not in targetPseudoLIST:
                    #conditionLIST = ["heard"]
                    if keys == ["space"]:
                        correctLIST = ["False"]
                    #conditionLIST = ["unheard"]
                    elif keys == ["None"]:
                        correctLIST = ["True"]
                    else:
                        correctLIST = ["N/A"]
                else:
                    pass
                
                # Collect the H/LCD of the words
                ## FOR Set A H/LCD
                if sub_cond == "A":
                    if stim_wordSTR in pair_1pw_LIST:
                        cdSTR = "H"
                    elif stim_wordSTR in pair_2pw_LIST:
                        cdSTR = "L"
                    else:
                        cdSTR = "C"
                
                ## FOR Set B H/LCD
                if sub_cond == "B":
                    if stim_wordSTR in pair_1pw_LIST:
                        cdSTR = "L"
                    elif stim_wordSTR in pair_2pw_LIST:
                        cdSTR = "H"
                    else:
                        cdSTR = "C"

                # making the wanted info into the List form for future use
                sub_idLIST.append(sub_id)
                dateLIST.append(day)
                sub_condLIST.append(sub_cond)
                roundLIST.append(round_)
                stimLIST.append(stim_wordSTR)
                CD_condLIST.append(cdSTR)
                resultKeyLIST.append(keys)
                responseLIST.append(conditionLIST)
                LDT_rtLIST.append(time_duration)
                correctnessLIST.append(correctLIST)
            
        #Display the instruction of the break in between Round 1 & Round 2
        print("Round", round_, "is over.")
        if round_ == 1:
            display_ins(instructions_3, keypressLIST_enter)
        else:
            display_ins(instructions_4, keypressLIST_enter)

            # close the window  at the end of the experiment
    win.close()


    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                           'Date':dateLIST,
                           'Sets':sub_condLIST,
                           'Round':roundLIST,
                           'Stimuli':stimLIST,
                           'CD_condition':CD_condLIST,
                           'Keypress':resultKeyLIST,
                           'Response':responseLIST,
                           'LDT_RT':LDT_rtLIST,
                           'Correctness':correctnessLIST
                           })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = '%s_S%s_LDT_preschool_testing_results.csv' %(sub_type, sub_id)
    save_path = result_data_path / Path(file_name)
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen
