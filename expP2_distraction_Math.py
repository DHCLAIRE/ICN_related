#!/usr/bin/env python3
# -*- coding:utf-8 -*-

## To Change the backend setting to PTB
from psychopy import prefs
#prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

##import psychtoolbox as ptb
from psychopy import core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
#print(sound.Sound)

import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
from pprint import pprint
import random
from random import sample
import re
from pathlib import Path
import serial


def display_ins(STR, keyPressLIST=None):
    '''
    *Self deifined function*
    To display the required strings and its appointed keypress.
    When the appointed strings and keypress were set, this function will display the strings.
    Only the pre-arranged keypress will allow the string display to proceed onto the next string.
    If no keypress was assigned, any keypress will continue the string display.
    e.g display_ins("lalala", ['space'])
    '''
    instructionsLIST = STR.split("\\\\")
    keyPressLIST = keyPressLIST

    for t in instructionsLIST:
        instructions = visual.TextStim(win=win, text=t, color=[-1, -1, -1])
        instructions.draw()
        win.flip()
        event.waitKeys(keyList=keyPressLIST)
    win.flip()

def display_fix():
    '''
    *Self deifined function*
    Display fixation in the central of the screen.
    e.g. display_fix()
    '''
    fixation = visual.TextStim(win=win, text="+", color=[-1, -1, -1])
    fixation.draw()
    win.flip()
    
def display_Image(ImageSTR, widthINT=None, heightINT=None):  #, keyPressLIST=None):
    '''
    *Self deifined function*
    To present the pic in the central of the screen
    '''
    pic = visual.ImageStim(win=win, image=ImageSTR, size=[widthINT, heightINT])
    pic.draw()
    win.flip()
    #event.waitKeys(keyList=keyPressLIST)
    #win.flip()
    
def gender(inputSTR):
    '''
    Determine the gender category
    '''
    sub_genderSTR = str()
    if inputSTR == "female":
        sub_genderSTR = "F"
    if inputSTR == "male":
        sub_genderSTR = "M"
    else:
        pass #print("No gender")
    
    return sub_genderSTR

def race(inputSTR):
    '''
    Determine the race category
    '''
    sub_raceSTR = str()
    if inputSTR == "black":
        sub_raceSTR = "B"
    if inputSTR == "caucasian":
        sub_raceSTR = "W"
    if inputSTR == "asian":
        sub_raceSTR = "A"
    else:
        pass #print("No race")
    
    return sub_raceSTR

def emotion(inputSTR):
    '''
    Determine the emotion category
    '''
    sub_emoSTR = str()
    if inputSTR == "angry":
        sub_emoSTR = "angry"
    if inputSTR == "fearful":
        sub_emoSTR = "fearful"
    if inputSTR == "neutral":
        sub_emoSTR = "neutral"
    else:
        pass #print("No emotion")
    
    return sub_emoSTR


def raceNgender(inputLIST, race_colINT, gen_colINT):
    '''
    Separate the group based on gender and race
    '''
    FB_LIST  = []
    FW_LIST = []
    FA_LIST = []
    MB_LIST = []
    MW_LIST = []
    MA_LIST = []
    for i in range(len(inputLIST)):
        raceSTR = race(pic_angryLIST[i][race_colINT])
        genderSTR = gender(pic_angryLIST[i][gen_colINT])
        # determine the race
        if genderSTR == "F":
            # Asian
            if raceSTR == "A":
                FA_LIST.append(pic_angryLIST[i])
            # Black
            if raceSTR == "B":
                FB_LIST.append(pic_angryLIST[i])
            # Caucasian
            if raceSTR == "W":
                FW_LIST.append(pic_angryLIST[i])
            else:
                pass
        else:
            # Asian
            if raceSTR == "A":
                MA_LIST.append(pic_angryLIST[i])
            # Black
            if raceSTR == "B":
                MB_LIST.append(pic_angryLIST[i])
            # Caucasian
            if raceSTR == "W":
                MW_LIST.append(pic_angryLIST[i])
            else:
                pass
    resultDICT = {"Female_Asian": FA_LIST,
                 "Female_Black": FB_LIST,
                 "Female_Caucasian": FW_LIST,
                 "Male_Asian": MA_LIST,
                 "Male_Black": MB_LIST,
                 "Male_Caucasian": MW_LIST
                 }
    
    return resultDICT

def stim_collection(inputDICT, sampleINT):
    '''
    # Randomly select the stimuli from files
    '''
    allstimLIST = []
    stimLIST = []
    for key, value in inputDICT.items():
        stimLIST = random.sample(value, sampleINT)
        allstimLIST.extend(stimLIST)
    
    return allstimLIST

# The EEG trigger port info
# For setting up the Trigger in NCU ICN Room608 EEG
# (Unnote the codes will activate the trigger port, thus to deactivate is to note the codes)
"""
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
    ### Distractions Task Starts ###
    try:
        win = visual.Window(size=[500, 500], color=[1, 1, 1], units ="pix")
        #win = visual.Window(color=[-1, -1, -1], units ="pix", fullscr = True)
        clock = core.Clock()
        #start_time = clock.getTime()  >>change position to make the calculation correct
    
        # Setting the instructions
        instructions_welcome_Chi = """歡迎參與此實驗"""
        instructions_welcome_Eng = """Welcome to the experiment!"""
        
        instructions_distraction_Chi = """在第二階段中，實驗流程如第一階段，\n
        圖片則將替換成數學乘法問題。（例如：5*5=25）。\n\n
        若答案正確，請按左邊的alt 鍵；\n
        若答案錯誤，則請按右邊的 alt 鍵。\n\n
        數學乘法問題將會在螢幕停留5秒，即便您已按下按鍵做反應，\n
        故僅需按鍵回答一次即可。\n\n
        請按空格鍵開始！
        """
        instructions_distraction_Eng = """In this session of the experiment, \n
        you will be presented with math multiplication problems. \n
        (example:5*5=25).\n\n
        Key Response:\n
        Press the left alt key if the answer is TRUE\n
        and\n
        press the right alt key if the answer is FALSE.\n
        Press the key as fast as you can.\n\n
        Equation lasts 5 seconds on the screen even after key press.\n
        Please press the key only once.\n\n
        Please press “space” to proceed.
        """
    
        instructions_end_Chi = """本實驗結束，謝謝！"""
        instructions_end_Eng = """This is the End of the experiment.\nThank You!"""
    
        
        ## Set the response key
        keypressLIST_space = ['space']
        keypressLIST_enter = ["return"]
        keypressLIST_alt = ["loption", "roption"] # In Mac == ["roption", "loptions"] # In win == ["lalt, ralt"]  # lalt = left Alt; ralt = right Alt
        #keypressLIST_scale = ["space", "h", "j", "k", "l"]  # "space"==1, "h"==2, "j"==3, "k"==4, "l"==5  # use right hand for these keypress 
        keypressLIST_esc = ["escape"]
    
        # Show the instructions >> Welcome the participants
        display_ins(instructions_welcome_Chi, keypressLIST_space)
        # Display the instructions for experiment content and keypress
        display_ins(instructions_distraction_Chi, keypressLIST_space)
        
        # Load in the math problem for distraction task
        with open(root_data_path / 'Distraction_task_materials.csv', 'r', encoding="utf-8") as csvf:
            distr_fileLIST = csvf.read().split("\n")
            pprint(distr_fileLIST)
            
            # Extract the equation
            mathLIST = []
            for i in distr_fileLIST[1:]:
                #print(i)
                tmpLIST = i.split(",")
                #print(itemLIST)
                mathLIST.append(tmpLIST)
            print(mathLIST)
    
        ## Show the stimuli(equations), randomly
        """
        ## To mark the round number  ##
        port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
        core.wait(.01); # Stay for 10 ms
        """
        # Randomly select the equation from the list
        random.shuffle(mathLIST)
        distr_mathLIST = sample(mathLIST, 20)
        print(len(distr_mathLIST), distr_mathLIST)
    
        ## Presave the blank list for wanted results
        day = date.today()
        dateLIST = []
        sub_idLIST = []
        stimLIST = []
        answerLIST =[]
        resultKeyLIST = []
        key_conditionLIST = []
        distr_rtLIST = []
        correctnessLIST = []
        correctLIST = []
        conditionLIST = []
        sub_condLIST = []
        
        for itemLIST in distr_mathLIST[:5]:
            ## To refresh the win before play out the stim pw
            win.flip()  # always add this after an item was presented
            #core.wait(2)
            ## Start to record the time
            start_time = clock.getTime()
    
            ## Display the math formula stimulus
            equationSTR = itemLIST[0]
            answerSTR = itemLIST[1]
            print(answerSTR)
            
            equaStim = visual.TextStim(win=win, text=equationSTR, color=[-1, -1, -1])
            equaStim.draw()
            win.flip()
            """
            # TO MARK THE PSEUDOWORD APPEARED
            port.write(b'1') #This is the num_tag for opening the trigger
            core.wait(.01); # Stay for 10 ms
            """
            
            # Setting up what keypress would allow the experiment to proceed
            keys = event.waitKeys(maxWait=5, keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
            event.getKeys(keyList=keypressLIST_alt)
            print(keys)
            
            # Add if-else condition to decide what to record in the results
            if keys == ["loption"]: #["lalt"]:
                conditionLIST = ["True"]
                end_time = clock.getTime()
                time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
                print(time_duration)
                #print(type(time_duration))
                clock.reset()
                # To determine whether the participants answers are correct or not
                if answerLIST == ["TRUE"]:
                    correctLIST = 1 #["correct"]
                    print(correctLIST)
                else:
                    correctLIST = 0 #["incorrect"]
            elif keys == ["roption"]: #["ralt"]:
                conditionLIST = ["False"]
                end_time = clock.getTime()
                time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                print(time_duration)
                #print(type(time_duration))
                clock.reset()
                if answerLIST == ["TRUE"]:
                    correctLIST = 0 #["incorrect"]
                    print(correctLIST)
                else:
                    correctLIST = 1 #["correct"]
                    
            #elif keys == ["escape"]:
                #win.close()
                #core.quit()
            else:
                keys = ["None"]
                conditionLIST = ["N/A"]
                time_duration = 0
                print(time_duration)
                clock.reset()
                    
            # making the wanted info into the List form for future use
            sub_idLIST.append(sub_id)
            sub_condLIST.append(sub_cond)
            dateLIST.append(day)
            stimLIST.append(equationSTR)
            answerLIST.append(answerSTR)
            resultKeyLIST.append(keys)
            key_conditionLIST.append(conditionLIST)
            distr_rtLIST.append(time_duration)
            correctnessLIST.append(correctLIST)  # 1 == correct; 0 == incorrect
    
        #Display the instruction of experiment ends
        display_ins(instructions_end_Chi, keypressLIST_space)
    
        # close the window  at the end of the experiment
        win.close()
        
    
        # Saving the self_paced_rt result into csv file
        dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                                 'Date':dateLIST,
                                 'EmoGroup':sub_condLIST,
                                 'Equation':stimLIST,
                                 'Equa_Answers':answerLIST,
                                 'Keypress':resultKeyLIST,
                                 'Response':key_conditionLIST,
                                 'RT':distr_rtLIST,
                                 'Correctness':correctnessLIST
                                 })
        
        #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
        file_name = 'Sub%s_%s_distraction_results.csv' %(sub_id, sub_cond)
        save_path = result_data_path / Path(file_name)
        dataDICT.to_csv(save_path, sep="," ,index=False, header=True, encoding="UTF-8")
    
    except:
        #setting up what keypress would allow the experiment to proceed
        keys = event.waitKeys() #keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
        event.getKeys()#keyList=keypressLIST_alt)
        #print(keys)
        if keys == ["escape"]:
            win.close()
            core.quit()
        
        
    ### Distractions Task Ends ###