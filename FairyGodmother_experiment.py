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
    faceNameLIST = []
    faceGenLIST = []
    faceRaceLIST = []
    bgstimLIST = []
    pic_seqLIST = []
    keyRepLIST = []

    # key in number for notifying which subject it is
    #sub_id = str(input("Subject: "))
    
    #### Experiment Begins ####
    ## Study Phase Start ###
    # Parameters Ssetting ##
    
    # Setting the presented window
    win = visual.Window(size = [500, 500],color = [1, 1, 1], units ="pix")
    ##win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()
    ##start_time = clock.getTime()  >>change position to make the calculation correct

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
    keypressLIST_alt = ["loption", "roption"] # In Mac == ["roption", "loptions"] # In win == ["lalt, ralt"]  # lalt = left Alt; ralt = right Alt
    keypressLIST_scale = ["space", "h", "j", "k", "l"]  # "space"==1, "h"==2, "j"==3, "k"==4, "l"==5  # use right hand for these keypress 
    #keypressLIST_esc = ["escape"]
    
    # Step_1: Show the instructions
    # Welcome the participants
    display_ins(instructions_welcome_Chi, keypressLIST_space)
    # Display the instructions for experiment content and keypress
    display_ins(instructions_study_Chi, keypressLIST_space)
    

    #core.wait(3)
    
    
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
    
    # Separate the race & gender
    angryDICT = raceNgender(pic_angryLIST, 4, 3)
    fearfulDICT = raceNgender(pic_fearfulLIST, 4, 3)
    neutralDICT = raceNgender(pic_neutralLIST, 4, 3)
    
    ## Randomly select the stims
    background_stimLIST = random.sample(pic_bgLIST, 30)
    random.shuffle(background_stimLIST)
    # Get the randomly selected stim out of the emotion pic database
    if sub_cond == "A":
        face_stimLIST = stim_collection(angryDICT, 5)
        random.shuffle(face_stimLIST)
        resultDICT = {"face":face_stimLIST,
                      "background": background_stimLIST}
    if sub_cond == "F":
        face_stimLIST = stim_collection(fearfulDICT, 5)
        random.shuffle(face_stimLIST)
        resultDICT = {"face":face_stimLIST,
                      "background": background_stimLIST}
    if sub_cond == "N":
        face_stimLIST = stim_collection(neutralDICT, 5)
        random.shuffle(face_stimLIST)
        resultDICT = {"face":face_stimLIST,
                      "background": background_stimLIST}
    else:
        pass

    with open(result_data_path / Path('Sub%s_%s_study_Allstims.json'%(sub_id, sub_cond)), 'w', newline='') as jsonfile:
        json.dump(resultDICT, jsonfile, ensure_ascii=False)
    
    
    ## The presentation of study starts
    for i in range(5):  # total is 30 round
        """
        ## To mark the round number  ##
        port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
        core.wait(.01); # Stay for 10 ms
        """
        ## To refresh the win before play out the stim
        win.flip()  # always add this after an item was presented
        #core.wait(0.5) # blank for 500 ms
        
        # start to record the time
        start_time = clock.getTime()

        # display fixation in the central of the screen
        display_fix()
        core.wait(0.5) # fixation for 500 ms

        # Display the pic stimulus
        face_imageSTR = str(face_data_path / Path(face_stimLIST[i][0]))
        bg_imageSTR = str(Bg_data_path / Path(background_stimLIST[i][0]))
        face_widthINT = int(face_stimLIST[i][6])
        face_heightINT = int(face_stimLIST[i][7])
        bg_widthINT = int(face_stimLIST[i][6])
        bg_heightINT = int(face_stimLIST[i][7])
        #print(widthINT)
        #print(heightINT)
        #print(face_imageSTR)
        #print(bg_imageSTR)
        bg_pic = visual.ImageStim(win=win, image=bg_imageSTR, size=[bg_widthINT, bg_heightINT])
        face_pic = visual.ImageStim(win=win, image=face_imageSTR, size=[face_widthINT, face_heightINT])
        bg_pic.overlaps = True
        bg_pic.draw()
        face_pic.overlaps = True
        face_pic.draw()
        

        
        core.wait(3) # stim for 3000 ms

        """
        # TO MARK THE PSEUDOWORD APPEARED
        port.write(b'1') #This is the num_tag for opening the trigger
        core.wait(.01); # Stay for 10 ms
        """
        win.flip()  # always add this after an item was presented
        core.wait(0.5) # blank for 500 ms?


        ##setting up what keypress would allow the experiment to proceed
        keys = event.waitKeys(maxWait=5, keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
        event.getKeys(keyList=keypressLIST_alt)
        print(keys)
        
        
        # Add if-else condition to decide what to record in the results
        if keys == ["loption"]: #["lalt"]:
            conditionLIST = ["female"]
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
            print(time_duration)
            #print(type(time_duration))
            clock.reset()
        elif keys == ["roption"]: #["ralt"]:
            conditionLIST = ["male"]
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
            print(time_duration)
            #print(type(time_duration))
            clock.reset()

        else:
            keys = ["None"]
            conditionLIST = ["N/A"]
            time_duration = 0
            print(time_duration)
            clock.reset()
        
        
        face_pic_seqINT = int(face_stimLIST[i][2])
        face_genSTR = str(face_stimLIST[i][3])
        face_raceSTR = str(face_stimLIST[i][4])
        bg_pic_seqINT = int(background_stimLIST[i][2])
        
        ## making the wanted info into the List form for future use
        sub_idLIST.append(sub_id)
        sub_condLIST.append(sub_cond)
        dateLIST.append(day)
        faceNameLIST.append(face_imageSTR)
        faceGenLIST.append(face_genSTR)
        faceRaceLIST.append(face_raceSTR)
        bgstimLIST.append(bg_imageSTR)
        pic_seqLIST.append([face_pic_seqINT, bg_pic_seqINT])
        resultKeyLIST.append(keys)
        responseLIST.append(time_duration)
        
        
    #Display the instruction of experiment ends
    display_ins(instructions_end_Chi, keypressLIST_space)

    # close the window  at the end of the experiment
    win.close()
    
    
    
    ## Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,         # subject number
                           'Date':dateLIST,               # when did the experiment happen
                           'Emo_Condition':sub_condLIST,  # emotion condition
                           'RT':responseLIST,             # the rt for memory reactions
                           'Keypress':resultKeyLIST,      # which key they press
                           'Key_rep':keyRepLIST,          # what does the keypress means
                           'Face_path':faceNameLIST,      # the file name of the face pic
                           'Bg_path':bgstimLIST,          # the file name of the bg pic
                           'Gender':faceGenLIST,          # the gender of the face pic
                           'Ethnic':faceRaceLIST,         # the ethnic of the face pic
                           'Pic_seq':pic_seqLIST          # the sequence of the pic (no matter it is Bg or face)
                           })
    
    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'Sub%s_%s_studyPhase_results.csv' %(sub_id, sub_cond)
    save_path = result_data_path / Path(file_name)
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    
    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen