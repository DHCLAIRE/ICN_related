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
        raceSTR = race(inputLIST[i][race_colINT])
        genderSTR = gender(inputLIST[i][gen_colINT])
        # determine the race
        if genderSTR == "F":
            # Asian
            if raceSTR == "A":
                FA_LIST.append(inputLIST[i])
            # Black
            if raceSTR == "B":
                FB_LIST.append(inputLIST[i])
            # Caucasian
            if raceSTR == "W":
                FW_LIST.append(inputLIST[i])
            else:
                pass
        else:
            # Asian
            if raceSTR == "A":
                MA_LIST.append(inputLIST[i])
            # Black
            if raceSTR == "B":
                MB_LIST.append(inputLIST[i])
            # Caucasian
            if raceSTR == "W":
                MW_LIST.append(inputLIST[i])
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
        if sampleINT == 0:
            stimLIST.extend(value)
        else:
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
    #### Preparations for experiment variables ####
    
    ## key in number for notifying which subject it is
    #sub_type = str(input("Group type: "))
    sub_id = str(input("Subject: "))
    sub_cond = str(input("Condition: "))  # Angry--A/Fearful--F/Neutral--N

    ## Set up the data path (For Win)
    #root_data_path = Path("D:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_preschool")
    #result_data_path = root_data_path / "LTTC_preschool_results"
    #result_data_path.mkdir(exist_ok=True)
    
    # Set up the data path (For Mac)
    root_data_path = Path("/Users/ting-hsin/Downloads/MaterialsExp2")
    face_data_path = root_data_path / "faces"
    Bg_data_path = root_data_path / "Backgrounds"
    result_data_path = root_data_path / "data" / Path("Sub_%s_%s" %(sub_id, sub_cond))
    result_data_path.mkdir(exist_ok=True) # if the folder wasn't created, this command will create the folder for you.
    
    ## Presave the blank list for wanted results
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    sub_condLIST = []
    resultKeyLIST = []
    stimLIST = []
    conditionLIST = []
    correctnessLIST = []
    responseLIST = []
    correctLIST = []
    roundLIST = []
    
    face_stimLIST = []
    background_stimLIST = []
    picNameLIST = []
    picGenLIST = []
    picRaceLIST = []
    pic_seqLIST = []
    keyRepLIST = []
    stimConditionLIST = []
    scaleLIST = []
    stimPicTypeLIST = []
    
    pic_foundBOOL = True
    
    #### Experiment Begins ####
    # Parameters Ssetting ##
    
    # Setting the presented window
    win = visual.Window(size = [500, 500],color = [1, 1, 1], units ="pix")
    ##win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()
    #start_time = clock.getTime()  >>change position to make the calculation correct

    # Setting the instructions
    instructions_welcome_Chi = """歡迎參與此實驗"""
    instructions_welcome_Eng = """Welcome to the experiment!"""
    
    instructions_test_Chi = """在第三階段中，請根據之前看過的背景場景和人臉照片進行回答。\n
    我們將先測試背景圖片或人臉的判斷，圖片會單獨出現。"""
    instructions_test_Eng = """In this phase, please answer based on your best recollection \n
    of the previously seen background and faces.\n
    We would test the , and the picture will display on its own."""
    
    instructions_end_Chi = """本實驗結束，謝謝！"""
    instructions_end_Eng = """This is the End of the experiment.\nThank You!"""

    
    ## Set the response key
    keypressLIST_space = ['space']
    keypressLIST_enter = ["return"]
    #keypressLIST_alt = ["loption", "roption"] # In Mac == ["roption", "loptions"] # In win == ["lalt, ralt"]  # lalt = left Alt; ralt = right Alt
    keypressLIST_scale = ["space", "h", "j", "k", "l"]  # "space"==1, "h"==2, "j"==3, "k"==4, "l"==5  # use right hand for these keypress 
    #keypressLIST_esc = ["escape"]
    
    # Step_1: Show the instructions
    # Welcome the participants
    display_ins(instructions_welcome_Chi, keypressLIST_space)
    # Display the instructions for experiment content and keypress
    display_ins(instructions_test_Chi, keypressLIST_space)
    

    #core.wait(3)
    
    # Open the materials
    with open(root_data_path / 'n_material_files_faces_n_Bg.csv', 'r', encoding = "utf-8") as csvf:
        pic_fileLIST = csvf.read().split("\n")
        #pprint(pic_fileLIST)
        pic_fileLIST.pop(0)
    pic_infoLIST = []
    
    pic_angryLIST = []
    pic_fearfulLIST = []
    pic_neutralLIST = []
    pic_bgLIST = []
    
    for pic_info in pic_fileLIST:
        pic_infoLIST = pic_info.split(",")
        #print(pic_infoLIST, len(pic_infoLIST))
        
        # Extract the pic name out of the data path
        pic_nameSTR = str(pic_infoLIST[0])
        #print(pic_nameSTR)
        
        
        pic_typeSTR = str(pic_infoLIST[1])
        pic_seqINT = int(pic_infoLIST[2])
        #pic_genderSTR = gender(str(pic_infoLIST[3]))
        #pic_raceSTR = race(str(pic_infoLIST[4]))
        pic_emoSTR = emotion(str(pic_infoLIST[5]))
        
        #print(pic_typeSTR)
        #print(pic_seqINT)
        #print(pic_genderSTR)
        #print(pic_raceSTR)
        #print(pic_emoSTR)
        
        # Group into the new group based on emotions
        if pic_typeSTR == "face":
            # Angry group
            if pic_emoSTR == "angry":
                pic_angryLIST.append(pic_infoLIST)
            if pic_emoSTR == "fearful":
                pic_fearfulLIST.append(pic_infoLIST)
            if pic_emoSTR == "neutral":
                pic_neutralLIST.append(pic_infoLIST)
        if pic_typeSTR == "background":
            pic_bgLIST.append(pic_infoLIST)
        else:
            pass
    
    #pprint(pic_angryLIST)
    #pprint(pic_fearfulLIST)
    #pprint(pic_neutralLIST)
    #pprint(pic_bgLIST)
    #print(len(pic_angryLIST), len(pic_fearfulLIST))
    
    ## Randomly select the stims
    #background_stimLIST = random.sample(pic_bgLIST, 30)  >> No need to select 30 out of 60
    random.shuffle(pic_bgLIST)
    # Get the randomly selected stim out of the emotion pic database
    if sub_cond == "A":
        face_stimLIST = pic_angryLIST
        random.shuffle(face_stimLIST)
        #resultDICT = {"face":face_stimLIST,
                      #"background": pic_bgLIST}
    if sub_cond == "F":
        face_stimLIST = pic_fearfulLIST
        random.shuffle(face_stimLIST)
        #resultDICT = {"face":face_stimLIST,
                      #"background": pic_bgLIST}
    if sub_cond == "N":
        face_stimLIST = pic_neutralLIST
        random.shuffle(face_stimLIST)
        #resultDICT = {"face":face_stimLIST,
                      #"background": pic_bgLIST}
    else:
        pass
    #pprint(resultDICT)
    
    ## Open the saved stim csv file in study phase for future old/new item judgements
    with open(result_data_path / Path('Sub%s_%s_study_Allstims.json'%(sub_id, sub_cond)), 'r', newline='') as jsonfile:
        study_stimDICT = json.load(jsonfile) #, ensure_ascii=False) #no encode into ascii
        #pprint(study_stimDICT)
    seenFaceLIST = study_stimDICT["face"]
    seenBgLIST = study_stimDICT["background"]

    ## Decide whether the face or bg goes first
    # randomly choose one of it to decide which type of pics they are going see first
    face_or_bgLIST = [0,1]  # 1== face goes first, bg goes second; 0 == display in reverse (bg first and then face second)
    
    face_or_bg_INT = random.choice(face_or_bgLIST)
    print("face_or_bg_INT:", face_or_bg_INT)
    
    ### The presentation of test starts
    ## Present all faces or bgs based on the emo conditions
    ## face_or_bg_INT == 1: face goes first, Bg second; face_or_bg_INT == 0: Bg goes first, face second
    if face_or_bg_INT == 1:
        ## if face_or_bg_INT == 1, the face would be block 1 & Bg would be block 2
        stim_datapathLIST = [face_data_path, Bg_data_path]
        test_stimLIST = [face_stimLIST, pic_bgLIST]
        seenStimLIST = [seenFaceLIST, seenBgLIST]
        
        for block_INT in range(2):
            """
            ## To mark the round number  ##
            port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
            core.wait(.01); # Stay for 10 ms
            """
            for i in range(5):  # total stim display should be 60
                ## To refresh the win before play out the stim
                win.flip()  # always add this after an item was presented
                #core.wait(0.5) # blank for 500 ms
        
                # display fixation in the central of the screen
                display_fix()
                core.wait(0.5) # fixation for 500 ms
        
                # Display the pic stimulus
                stim_imageSTR = str(stim_datapathLIST[block_INT] / Path(test_stimLIST[block_INT][i][0]))
                stim_widthINT = int(test_stimLIST[block_INT][i][6])
                stim_heightINT = int(test_stimLIST[block_INT][i][7])
                
                ## start to record the time
                start_time = clock.getTime()
                ## Display the stim
                stim_pic = visual.ImageStim(win=win, image=stim_imageSTR, size=[stim_widthINT, stim_heightINT])
                stim_pic.draw()
    
                """
                # TO MARK THE PSEUDOWORD APPEARED
                port.write(b'1') #This is the num_tag for opening the trigger
                core.wait(.01); # Stay for 10 ms
                """
                win.flip()  # always add this after an item was presented
                #core.wait(0.5) # blank for 500 ms?
                
                ###setting up what keypress would allow the experiment to proceed
                keys = event.waitKeys(maxWait=5, keyList=keypressLIST_scale) # press the buttons of scales
                event.getKeys(keyList=keypressLIST_scale)
                print(keys)
                #core.wait(3) # stim for 3000 ms
                    
                ## Add if-else condition to decide what to record in the results
                if keys == ["space"]:  #"h", "j", "k", "l"
                    scaleINT = 1
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["h"]:
                    scaleINT = 2
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["j"]: #["ralt"]:
                    scaleINT = 3
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["k"]:
                    scaleINT = 4
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["l"]:
                    scaleINT = 5
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                else:
                    keys = ["None"]
                    scaleINT = ["N/A"]
                    time_duration = 0
                    print(time_duration)
                    clock.reset()
                    
                #print("Round_count:", block_INT)
                #print("==========================================")
                #print("Stim Num:", i)
                
                ## Decide what pic is seen(old) or unseen(new) to record in the results(look from both face & Bg list)
                pic_foundINT = 0
                for c in range(2):
                    #print("Seen Pic LIST:", c)
                    for seenPicInfoLIST in seenStimLIST[c]:
                        #print(seenPicInfoLIST[0])
                        ## Check the face path  (face == column[6])
                        if seenPicInfoLIST[0] in stim_imageSTR:
                            #print("Pic Found")
                            pic_foundINT += 1
                        else:
                            pass
                            #print("404 Not Found")
                    ## Use the accumulated pic_foundINT value to determine pic_found status (pic_foundBOOL)
                    if pic_foundINT > 0:
                        pic_foundBOOL = True
                    else:
                        pic_foundBOOL = False
                    #print("Database:",c ,"Seen status:", bool(pic_foundBOOL))
                
                # Check if the stim pic is seen(old) or unseen(new) using pic_foundBOOL
                if pic_foundBOOL == True:
                    stim_condtionSTR = "old"
                else:
                    stim_condtionSTR = "new"
                
                ## Assign the stored values of the stims for the result form
                stim_seqINT = int(test_stimLIST[block_INT][i][2])
                stim_genSTR = str(test_stimLIST[block_INT][i][3])
                stim_raceSTR = str(test_stimLIST[block_INT][i][4])
                
                # Determine the pic type based on the display order of the stim type (either face first or Bg first, change this when in different order)
                # face_or_bg_INT == 1 >> 1 == face goes first, bg second
                if block_INT == 0:
                    stim_typeSTR = "face"
                else:
                    stim_typeSTR = "background"
                
                ## making the wanted info into the List form for future use
                sub_idLIST.append(sub_id)
                sub_condLIST.append(sub_cond)   # the emo group of the participants
                dateLIST.append(day)
                picNameLIST.append(stim_imageSTR)  # include the data path of the stim picture
                picGenLIST.append(stim_genSTR)
                picRaceLIST.append(stim_raceSTR)
                pic_seqLIST.append(stim_seqINT)
                resultKeyLIST.append(keys)
                responseLIST.append(time_duration)
                scaleLIST.append(scaleINT)
                stimConditionLIST.append(stim_condtionSTR)
                stimPicTypeLIST.append(stim_typeSTR)   # whether it's the face or the Bg
                
        #Display the instruction of experiment ends
        display_ins(instructions_end_Chi, keypressLIST_space)
    
        # close the window  at the end of the experiment
        win.close()
            
            
            
        ### Saving the self_paced_rt result into csv file
        dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,              # subject number
                               'Date':dateLIST,                    # when did the experiment happen
                               'Emo_Condition':sub_condLIST,       # emotion condition
                               'Pic_seq':pic_seqLIST,              # the sequence of the pic (no matter it is Bg or face)
                               'Pic_type':stimPicTypeLIST,         # the type of the presented stim pic
                               'RT':responseLIST,                  # the rt for memory reactions
                               'Keypress':resultKeyLIST,           # which key they press
                               'Scale':scaleLIST,                  # what does the keypress means
                               'Pic_condition':stimConditionLIST,  # seen(old)/unseen(new) status of the stim pics
                               'Gender':picGenLIST,                # the gender of the face pic
                               'Ethnic':picRaceLIST,               # the ethnic of the face pic
                               'Path':picNameLIST,                 # the file name of the face pic
                               })
        
        #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
        file_name = 'Sub%s_%s_testPhase_results.csv' %(sub_id, sub_cond)
        save_path = result_data_path / Path(file_name)
        dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
        
        # close all the possible ongoing commands that could be running in the background
        core.quit()  # normally we would add it, in case that anything happen
            
    ## face_or_bg_INT == 1: face goes first, Bg second; face_or_bg_INT == 0: Bg goes first, face second
    ## if face_or_bg_INT == 0, the bg would be block 1 & face would be block 2
    elif face_or_bg_INT == 0:
        stim_datapathLIST = [Bg_data_path, face_data_path]
        test_stimLIST = [pic_bgLIST, face_stimLIST]
        seenStimLIST = [seenBgLIST, seenFaceLIST]
        
        #pprint(test_stimLIST[block_INT])
        #pprint(stim_datapathLIST[block_INT])
        #print(len(test_stimLIST[block_INT]))
        
        for block_INT in range(2):
            """
            ## To mark the round number  ##
            port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
            core.wait(.01); # Stay for 10 ms
            """
            # Display the stim
            for i in range(5):  # total stim display should be 60
                ## To refresh the win before play out the stim
                win.flip()  # always add this after an item was presented
                #core.wait(0.5) # blank for 500 ms
        
                # display fixation in the central of the screen
                display_fix()
                core.wait(0.5) # fixation for 500 ms
        
                # Display the pic stimulus
                stim_imageSTR = str(stim_datapathLIST[block_INT] / Path(test_stimLIST[block_INT][i][0]))
                stim_widthINT = int(test_stimLIST[block_INT][i][6])
                stim_heightINT = int(test_stimLIST[block_INT][i][7])
                
                ## start to record the time
                start_time = clock.getTime()
                ## Display the stim
                stim_pic = visual.ImageStim(win=win, image=stim_imageSTR, size=[stim_widthINT, stim_heightINT])
                stim_pic.draw()
    
                """
                # TO MARK THE PSEUDOWORD APPEARED
                port.write(b'1') #This is the num_tag for opening the trigger
                core.wait(.01); # Stay for 10 ms
                """
                win.flip()  # always add this after an item was presented
                #core.wait(0.5) # blank for 500 ms?
        
            
                ###setting up what keypress would allow the experiment to proceed
                keys = event.waitKeys(maxWait=5, keyList=keypressLIST_scale) # press the buttons of scales
                event.getKeys(keyList=keypressLIST_scale)
                print(keys)
                #core.wait(3) # stim for 3000 ms
                    
                ## Add if-else condition to decide what to record in the results
                if keys == ["space"]:  #"h", "j", "k", "l"
                    scaleINT = 1
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["h"]:
                    scaleINT = 2
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["j"]: #["ralt"]:
                    scaleINT = 3
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["k"]:
                    scaleINT = 4
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                if keys == ["l"]:
                    scaleINT = 5
                    end_time = clock.getTime()
                    time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                    print(time_duration)
                    #print(type(time_duration))
                    clock.reset()
                    
                else:
                    keys = ["None"]
                    scaleINT = ["N/A"]
                    time_duration = 0
                    print(time_duration)
                    clock.reset()
                    
                #print("Round_count:", block_INT)
                #print("==========================================")
                #print("Stim Num:", i)
                
                ## Decide what pic is seen(old) or unseen(new) to record in the results(look from both face & Bg list)
                pic_foundINT = 0
                for c in range(2):
                    #print("Seen Pic LIST:", c)
                    for seenPicInfoLIST in seenStimLIST[c]:
                        #print(seenPicInfoLIST[0])
                        ## Check the face path  (face == column[6])
                        if seenPicInfoLIST[0] in stim_imageSTR:
                            #print("Pic Found")
                            pic_foundINT += 1
                        else:
                            pass
                            #print("404 Not Found")
                    ## Use the accumulated pic_foundINT value to determine pic_found status (pic_foundBOOL)
                    if pic_foundINT > 0:
                        pic_foundBOOL = True
                    else:
                        pic_foundBOOL = False
                    #print("Database:",c ,"Seen status:", bool(pic_foundBOOL))
                
                # Check if the stim pic is seen(old) or unseen(new) using pic_foundBOOL
                if pic_foundBOOL == True:
                    stim_condtionSTR = "old"
                else:
                    stim_condtionSTR = "new"
                
                ## Assign the stored values of the stims for the result form
                stim_seqINT = int(test_stimLIST[block_INT][i][2])
                stim_genSTR = str(test_stimLIST[block_INT][i][3])
                stim_raceSTR = str(test_stimLIST[block_INT][i][4])
                
                # Determine the pic type based on the display order of the stim type (either face first or Bg first, change this when in different order)
                # face_or_bg_INT == 1 >> 1 == face goes first, bg second
                if block_INT == 0:
                    stim_typeSTR = "background"
                else:
                    stim_typeSTR = "face"
                
                ## making the wanted info into the List form for future use
                sub_idLIST.append(sub_id)
                sub_condLIST.append(sub_cond)   # the emo group of the participants
                dateLIST.append(day)
                picNameLIST.append(stim_imageSTR)  # include the data path of the stim picture
                picGenLIST.append(stim_genSTR)
                picRaceLIST.append(stim_raceSTR)
                pic_seqLIST.append(stim_seqINT)
                resultKeyLIST.append(keys)
                responseLIST.append(time_duration)
                scaleLIST.append(scaleINT)
                stimConditionLIST.append(stim_condtionSTR)
                stimPicTypeLIST.append(stim_typeSTR)   # whether it's the face or the Bg
                
        #Display the instruction of experiment ends
        display_ins(instructions_end_Chi, keypressLIST_space)
    
        # close the window  at the end of the experiment
        win.close()
            
            
            
        ### Saving the self_paced_rt result into csv file
        dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,              # subject number
                               'Date':dateLIST,                    # when did the experiment happen
                               'Emo_Condition':sub_condLIST,       # emotion condition
                               'Pic_seq':pic_seqLIST,              # the sequence of the pic (no matter it is Bg or face)
                               'Pic_type':stimPicTypeLIST,         # the type of the presented stim pic
                               'RT':responseLIST,                  # the rt for memory reactions
                               'Keypress':resultKeyLIST,           # which key they press
                               'Scale':scaleLIST,                  # what does the keypress means
                               'Pic_condition':stimConditionLIST,  # seen(old)/unseen(new) status of the stim pics
                               'Gender':picGenLIST,                # the gender of the face pic
                               'Ethnic':picRaceLIST,               # the ethnic of the face pic
                               'Path':picNameLIST,                 # the file name of the face pic
                               })
        
        #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
        file_name = 'Sub%s_%s_testPhase_results.csv' %(sub_id, sub_cond)
        save_path = result_data_path / Path(file_name)
        dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
        
        # close all the possible ongoing commands that could be running in the background
        core.quit()  # normally we would add it, in case that anything happen
    else:
        # close the window  at the end of the experiment
        win.close()
        # close all the possible ongoing commands that could be running in the background
        core.quit()