#!/usr/bin/env python3
# -*- coding:utf-8 -*-

## To Change the backend setting to PTB
#from psychopy import prefs
##prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

##import psychtoolbox as ptb
#from psychopy import core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
##print(sound.Sound)

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
    fixation = visual.TextStim(win=win, text="+")
    fixation.draw()
    win.flip()
    
def display_Image(ImageSTR):  #, keyPressLIST=None):
    '''
    *Self deifined function*
    To present the pic in the central of the screen
    '''
    pic = visual.ImageStim(win=win, image=ImageSTR)
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
    #result_data_path = root_data_path / "data" / Path("Sub_%s_%s" %(sub_id, sub_cond))
    #result_data_path.mkdir(exist_ok=True) # if the folder wasn't created, this command will create the folder for you.
    
    ## Setting up usable dataLIST
    #targetPseudoLIST = []
    #pseudoLIST = []
    #targetPseudoLIST = []

    ### Set up the pws' data path, and Call out the pw's LIST by the audios' names
    #pw_stimLIST = [path.name for path in target_w_stim_data_path.iterdir() if re.match(r'\D', path.name)]  #(both works)\D == any non-digits; \w == any characters(digits included)
    #print(pw_stimLIST) # pw_stimLIST = ['bi4_ba2.wav', 'bo4_luo2.wav', 'chai2_fei1.wav', 'ge2_lu3.wav', 'ji3_an4.wav', 'pu2_zu2.wav', 'sheng1_chu4.wav', 'zhai1_tan2.wav']
    #'''
    ## This is just for testing the re commands
    #for path in target_w_stim_data_path.iterdir():
        #if re.match(r'\w', path.name):  # path.name == the name of the file in the specfic location
            #print(path.suffix)  # path.suffix == the file type of the file in the specfic location
            #print(type(path.suffix))
    #'''
    ### This the every pseudowords audio file name
    ##pseudoLIST = pw_stimLIST.copy()
    ##print(pseudoLIST)
    #for f_nameSTR in pw_stimLIST:
        #pseudoLIST.append(f_nameSTR[:-4])  # exclude the file extension
    #print(pseudoLIST)
    
    ## Presave the blank list for wanted results
    #day = date.today()
    #dateLIST = []
    #sub_idLIST = []
    #sub_condLIST = []
    #resultKeyLIST = []
    #stimLIST = []
    #CD_condLIST = []
    #conditionLIST = []
    #LDT_rtLIST = []
    #correctnessLIST = []
    #responseLIST = []
    #correctLIST = []
    #roundLIST = []

    # key in number for notifying which subject it is
    #sub_id = str(input("Subject: "))
    
    #### Experiment Begins ####
    ## Study Phase Start ###
    # Parameters Ssetting ##
    
    # Setting the presented window
    #win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    ##win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    #clock = core.Clock()
    ##start_time = clock.getTime()  >>change position to make the calculation correct

    # Setting the instructions
    instructions_welcome_Chi = """歡迎參與此實驗"""
    instructions_welcome_Eng = """Welcome to the experiment!"""
    
    instructions_study_Chi = """在第一階段裡，您將同時看到一張人臉及圖片背景。\n
    請以觀看整張圖片的方式來看，而非僅聚焦在人臉或背景圖片上。\n\n
    當看到人臉時，若為女性臉孔，請按下左邊的Alt鍵。\n
    若為男性臉孔，則請按下右邊的Alt鍵。\n如下方圖片所示：\n
    即便您已按下按鍵做反應，圖片將會在螢幕停留一下，\n
    故僅需按鍵回答一次即可。\n\n
    請按空格鍵開始！
    """
    instructions_study_Eng = """In this experiment, you will be presented with faces embedded in the background.\n
    Please see the picture hoslically without focus only on the faces or background.\n\n
    WKey Response:\n
    Press the left alt key if the face is a FEMALE\n
    and\n
    press the right alt key if the face is a MALE.\n
    Press the key as fast as you can.\n\n
    Picture would stay displayed on the screen even after key press.\n
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
    #keypressLIST_esc = ["escape"]
    
    # Step_1: Show the instructions
    # Welcome the participants
    #display_ins(instructions_welcome_Chi, keypressLIST_space)
    ## Display the instructions for experiment content and keypress
    #display_ins(instructions_study_Chi, keypressLIST_space)
    

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

    with open(root_data_path / Path('Sub%s_%s_study_Allstims.json'%(sub_id, sub_cond)), 'w', newline='') as jsonfile:
        json.dump(resultDICT, jsonfile, ensure_ascii=False)
    
    
    ## The presentation of study starts
    for i in range(30):
        """
        ## To mark the round number  ##
        port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
        core.wait(.01); # Stay for 10 ms
        """
        ## To refresh the win before play out the stim
        #win.flip()  # always add this after an item was presented
        #core.wait(0.5) # blank for 500 ms
        
        ## start to record the time
        #start_time = clock.getTime()

        # display fixation in the central of the screen
        #display_fix()
        #core.wait(0.5) # fixation for 500 ms

        # Display the pic stimulus
        face_imageSTR = face_stimLIST[i][0]
        bg_imageSTR = background_stimLIST[i][0]
        #display_Image(face_imageSTR)
        #display_Image(bg_imageSTR)
        
        #core.wait(3) # stim for 3000 ms

        """
        # TO MARK THE PSEUDOWORD APPEARED
        port.write(b'1') #This is the num_tag for opening the trigger
        core.wait(.01); # Stay for 10 ms
        """
        #win.flip()  # always add this after an item was presented
        #core.wait(0.5) # blank for 500 ms?


        ##setting up what keypress would allow the experiment to proceed
        keys = event.waitKeys(maxWait=5, keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
        event.getKeys(keyList=keypressLIST_alt)
        print(keys)
        
        
        # Add if-else condition to decide what to record in the results
                    #if keys == ["loption"]: #["lalt"]:
                        #conditionLIST = ["True"]
                        #end_time = clock.getTime()
                        #time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
                        #print(time_duration)
                        ##print(type(time_duration))
                        #clock.reset()
                        ## To determine whether the participants answers are correct or not
                        #if answerLIST == ["TRUE"]:
                            #correctLIST = 1 #["correct"]
                            #print(correctLIST)
                        #else:
                            #correctLIST = 0 #["incorrect"]
                    #elif keys == ["roption"]: #["ralt"]:
                        #conditionLIST = ["False"]
                        #end_time = clock.getTime()
                        #time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                        #print(time_duration)
                        ##print(type(time_duration))
                        #clock.reset()
                        #if answerLIST == ["TRUE"]:
                            #correctLIST = 0 #["incorrect"]
                            #print(correctLIST)
                        #else:
                            #correctLIST = 1 #["correct"]
                            
                    ##elif keys == ["escape"]:
                        ##win.close()
                        ##core.quit()
                    #else:
                        #keys = ["None"]
                        #conditionLIST = ["N/A"]
                        #time_duration = 0
                        #print(time_duration)
                        #clock.reset()        
        ## 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
        #if keys == ["loption"]: #["lalt"]:
            #conditionLIST = ["female"]
            #end_time = clock.getTime()
            #time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
            #print(time_duration)
            ##print(type(time_duration))
            #clock.reset()
        #elif keys == ["roption"]: #["ralt"]:
            #conditionLIST = ["male"]
            #end_time = clock.getTime()
            #time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
            #print(time_duration)
            ##print(type(time_duration))
            #clock.reset()

        #else:
            #keys = ["None"]
            #conditionLIST = ["N/A"]
            #time_duration = 0
            #print(time_duration)
            #clock.reset()

        
        ## calculate the correctness of the gender determination response
        #if gen_ans == ["female"]:  ## Rivise this command
            ## ans is "Correct"
            #if keys == ["lalt"]:
                #correctLIST = ["True"]
            ## ans is "Incorrect"
            #elif keys == ["ralt"]:
                #correctLIST = ["False"]
            #else:
                #correctLIST = ["N/A"]

        #elif gen_ans == ["male"]:
            ## ans is "Correct"
            #if keys == ["ralt"]:
                #correctLIST = ["True"]
            ## ans is "Incorrect"
            #elif keys == ["lalt"]:
                #correctLIST = ["False"]
            #else:
                #correctLIST = ["N/A"]
        #else:
            #pass
        
        ## Collect the H/LCD of the words
        ### FOR Set A H/LCD
        #if sub_cond == "A":
            #if stim_wordSTR in pair_1pw_LIST:
                #cdSTR = "H"
            #elif stim_wordSTR in pair_2pw_LIST:
                #cdSTR = "L"
            #else:
                #cdSTR = "C"
        
        ### FOR Set B H/LCD
        #if sub_cond == "B":
            #if stim_wordSTR in pair_1pw_LIST:
                #cdSTR = "L"
            #elif stim_wordSTR in pair_2pw_LIST:
                #cdSTR = "H"
            #else:
                #cdSTR = "C"
                
        ## making the wanted info into the List form for future use
        #sub_idLIST.append(sub_id)
        #dateLIST.append(day)
        #sub_condLIST.append(sub_cond)
        #roundLIST.append(round_)
        #stimLIST.append(stim_wordSTR)
        #CD_condLIST.append(cdSTR)
        #resultKeyLIST.append(keys)
        #responseLIST.append(conditionLIST)
        #LDT_rtLIST.append(time_duration)
        #correctnessLIST.append(correctLIST)
        
        ##Display the instruction of the break in between Round 1 & Round 2
        #print("Round", round_, "is over.")
        #if round_ == 1:
            #display_ins(instructions_3, keypressLIST_enter)
        #else:
            #display_ins(instructions_4, keypressLIST_enter)
    
    ## close the window  at the end of the experiment
    #win.close()
    
    
    
    ## Saving the self_paced_rt result into csv file
    #dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,         # subject number
                           #'Date':dateLIST,               # when did the experiment happen
                           #'Emo_Condition':sub_condLIST,  # emotion condition
                           #'Trial_num':trialLIST,         # which trial
                           #'RT':rtLIST,                   # the rt for memory reations
                           #'Keypress':resultKeyLIST,      # which key they press
                           #'Scale':scaleLIST,             # How confidence they thought themselves (=what does the keypress mean)
                           #'Emotion':faceEmoLIST,         # which emotion of the face pic
                           #'Gender':genderLIST,           # the gender of the face pic
                           #'Ethnic':ethnicLIST,           # the ethnic of the face pic
                           #'Pic_seq':pic_seqLIST,         # the sequence of the pic (no matter it is Bg or face)
                           #'Face_path':pathLIST,          # the datapath of the face pic
                           #'Bg_path':BgLIST,              # the datapath of the background pic
                           #'Pic_Condition':old_newLIST    # the seen or not condition
                           #})
    
    ##data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    #file_name = 'Sub%s_%s_studyPhase_results.csv' %(sub_id, sub_cond)
    #save_path = result_data_path / Path(file_name)
    #dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    
    ## close all the possible ongoing commands that could be running in the background
    #core.quit()  # normally we would add it, in case that anything happen
    
    ### Study Phase Ends ###
    
    
    #### Distractions Task Starts ###
    #try:
        #win = visual.Window(size=[500, 500], color=[1, 1, 1], units ="pix")
        ##win = visual.Window(color=[-1, -1, -1], units ="pix", fullscr = True)
        #clock = core.Clock()
        ##start_time = clock.getTime()  >>change position to make the calculation correct
    
        ## Setting the instructions
        #instructions_welcome_Chi = """歡迎參與此實驗"""
        #instructions_welcome_Eng = """Welcome to the experiment!"""
        
        #instructions_distraction_Chi = """在第二階段中，實驗流程如第一階段，\n
        #圖片則將替換成數學乘法問題。（例如：5*5=25）。\n\n
        #若答案正確，請按左邊的alt 鍵；\n
        #若答案錯誤，則請按右邊的 alt 鍵。\n\n
        #數學乘法問題將會在螢幕停留5秒，即便您已按下按鍵做反應，\n
        #故僅需按鍵回答一次即可。\n\n
        #請按空格鍵開始！
        #"""
        #instructions_distraction_Eng = """In this session of the experiment, \n
        #you will be presented with math multiplication problems. \n
        #(example:5*5=25).\n\n
        #Key Response:\n
        #Press the left alt key if the answer is TRUE\n
        #and\n
        #press the right alt key if the answer is FALSE.\n
        #Press the key as fast as you can.\n\n
        #Equation lasts 5 seconds on the screen even after key press.\n
        #Please press the key only once.\n\n
        #Please press “space” to proceed.
        #"""
    
        #instructions_end_Chi = """本實驗結束，謝謝！"""
        #instructions_end_Eng = """This is the End of the experiment.\nThank You!"""
    
        
        ### Set the response key
        #keypressLIST_space = ['space']
        #keypressLIST_enter = ["return"]
        #keypressLIST_alt = ["loption", "roption"] # In Mac == ["roption", "loptions"] # In win == ["lalt, ralt"]  # lalt = left Alt; ralt = right Alt
        ##keypressLIST_scale = ["space", "h", "j", "k", "l"]  # "space"==1, "h"==2, "j"==3, "k"==4, "l"==5  # use right hand for these keypress 
        #keypressLIST_esc = ["escape"]
    
        ## Show the instructions >> Welcome the participants
        #display_ins(instructions_welcome_Chi, keypressLIST_space)
        ## Display the instructions for experiment content and keypress
        #display_ins(instructions_distraction_Chi, keypressLIST_space)
        
        ## Load in the math problem for distraction task
        #with open(root_data_path / 'Distraction_task_materials.csv', 'r', encoding="utf-8") as csvf:
            #distr_fileLIST = csvf.read().split("\n")
            #pprint(distr_fileLIST)
            
            ## Extract the equation
            #mathLIST = []
            #for i in distr_fileLIST[1:]:
                ##print(i)
                #tmpLIST = i.split(",")
                ##print(itemLIST)
                #mathLIST.append(tmpLIST)
            #print(mathLIST)
    
        ### Show the stimuli(equations), randomly
        #"""
        ### To mark the round number  ##
        #port.write(b'2') #This is the num_tag for opening the trigger  #編號要用幾號再討論
        #core.wait(.01); # Stay for 10 ms
        #"""
        ## Randomly select the equation from the list
        #random.shuffle(mathLIST)
        #distr_mathLIST = sample(mathLIST, 20)
        #print(len(distr_mathLIST), distr_mathLIST)
    
        ### Presave the blank list for wanted results
        #day = date.today()
        #dateLIST = []
        #sub_idLIST = []
        #stimLIST = []
        #answerLIST =[]
        #resultKeyLIST = []
        #key_conditionLIST = []
        #distr_rtLIST = []
        #correctnessLIST = []
        #correctLIST = []
        #conditionLIST = []
        #sub_condLIST = []
        
        #for itemLIST in distr_mathLIST[:5]:
            ### To refresh the win before play out the stim pw
            #win.flip()  # always add this after an item was presented
            ##core.wait(2)
            ### Start to record the time
            #start_time = clock.getTime()
    
            ### Display the math formula stimulus
            #equationSTR = itemLIST[0]
            #answerSTR = itemLIST[1]
            #print(answerSTR)
            
            #equaStim = visual.TextStim(win=win, text=equationSTR, color=[-1, -1, -1])
            #equaStim.draw()
            #win.flip()
            #"""
            ## TO MARK THE PSEUDOWORD APPEARED
            #port.write(b'1') #This is the num_tag for opening the trigger
            #core.wait(.01); # Stay for 10 ms
            #"""
            
            ## Setting up what keypress would allow the experiment to proceed
            #keys = event.waitKeys(maxWait=5, keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
            #event.getKeys(keyList=keypressLIST_alt)
            #print(keys)
            
            ## Add if-else condition to decide what to record in the results
            #if keys == ["loption"]: #["lalt"]:
                #conditionLIST = ["True"]
                #end_time = clock.getTime()
                #time_duration = round(end_time - start_time, 3)*1000    # normally we use 以毫秒作為單位
                #print(time_duration)
                ##print(type(time_duration))
                #clock.reset()
                ## To determine whether the participants answers are correct or not
                #if answerLIST == ["TRUE"]:
                    #correctLIST = 1 #["correct"]
                    #print(correctLIST)
                #else:
                    #correctLIST = 0 #["incorrect"]
            #elif keys == ["roption"]: #["ralt"]:
                #conditionLIST = ["False"]
                #end_time = clock.getTime()
                #time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
                #print(time_duration)
                ##print(type(time_duration))
                #clock.reset()
                #if answerLIST == ["TRUE"]:
                    #correctLIST = 0 #["incorrect"]
                    #print(correctLIST)
                #else:
                    #correctLIST = 1 #["correct"]
                    
            ##elif keys == ["escape"]:
                ##win.close()
                ##core.quit()
            #else:
                #keys = ["None"]
                #conditionLIST = ["N/A"]
                #time_duration = 0
                #print(time_duration)
                #clock.reset()
                    
            ## making the wanted info into the List form for future use
            #sub_idLIST.append(sub_id)
            #sub_condLIST.append(sub_cond)
            #dateLIST.append(day)
            #stimLIST.append(equationSTR)
            #answerLIST.append(answerSTR)
            #resultKeyLIST.append(keys)
            #key_conditionLIST.append(conditionLIST)
            #distr_rtLIST.append(time_duration)
            #correctnessLIST.append(correctLIST)  # 1 == correct; 0 == incorrect
    
        ##Display the instruction of experiment ends
        #display_ins(instructions_end_Chi, keypressLIST_space)
    
        ## close the window  at the end of the experiment
        #win.close()
        
    
        ## Saving the self_paced_rt result into csv file
        #dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                                 #'Date':dateLIST,
                                 #'EmoGroup':sub_condLIST,
                                 #'Equation':stimLIST,
                                 #'Equa_Answers':answerLIST,
                                 #'Keypress':resultKeyLIST,
                                 #'Response':key_conditionLIST,
                                 #'RT':distr_rtLIST,
                                 #'Correctness':correctnessLIST
                                 #})
        
        ##data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
        #file_name = 'Sub%s_%s_distraction_results.csv' %(sub_id, sub_cond)
        #save_path = result_data_path / Path(file_name)
        #dataDICT.to_csv(save_path, sep="," ,index=False, header=True, encoding="UTF-8")
    
    #except:
        ##setting up what keypress would allow the experiment to proceed
        #keys = event.waitKeys() #keyList=keypressLIST_alt) # press "lalt" or "ralt" to determine the gender
        #event.getKeys()#keyList=keypressLIST_alt)
        ##print(keys)
        #if keys == ["escape"]:
            #win.close()
            #core.quit()
        
        
    #### Distractions Task Ends ###
    #### Test Phase Starts ###
    # Setting the presented window
    
    #win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    ##win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    #clock = core.Clock()
    ##start_time = clock.getTime()  >>change position to make the calculation correct

    ## Setting the instructions
    #instructions_welcome_Chi = """歡迎參與此實驗"""
    #instructions_welcome_Eng = """Welcome to the experiment!"""
    
    #instructions_study_Chi = """在第一階段裡，您將同時看到一張人臉及圖片背景。\n
    #請以觀看整張圖片的方式來看，而非僅聚焦在人臉或背景圖片上。\n\n
    #當看到人臉時，若為女性臉孔，請按下左邊的Alt鍵。\n
    #若為男性臉孔，則請按下右邊的Alt鍵。\n如下方圖片所示：\n
    #即便您已按下按鍵做反應，圖片將會在螢幕停留一下，\n
    #故僅需按鍵回答一次即可。\n\n
    #請按空格鍵開始！
    #"""
    #instructions_study_Eng = """In this experiment, you will be presented with faces embedded in the background.\n
    #Please see the picture hoslically without focus only on the faces or background.\n\n
    #WKey Response:\n
    #Press the left alt key if the face is a FEMALE\n
    #and\n
    #press the right alt key if the face is a MALE.\n
    #Press the key as fast as you can.\n\n
    #Picture would stay displayed on the screen even after key press.\n
    #Please press the key only once.\n\n
    #Please press “space” to proceed.
    #"""
    
    #instructions_distraction_Chi = """在第二階段中，實驗流程如第一階段，\n
    #圖片則將替換成數學乘法問題。（例如：5*5=25）。\n\n
    #若答案正確，請按左邊的alt 鍵；\n
    #若答案錯誤，則請按右邊的 alt 鍵。\n\n
    #數學乘法問題將會在螢幕停留5秒，即便您已按下按鍵做反應，\n
    #故僅需按鍵回答一次即可。\n\n
    #請按空格鍵開始！
    #"""
    #instructions_distraction_Eng = """In this session of the experiment, \n
    #you will be presented with math multiplication problems. \n
    #(example:5*5=25).\n\n
    #Key Response:\n
    #Press the left alt key if the answer is TRUE\n
    #and\n
    #press the right alt key if the answer is FALSE.\n
    #Press the key as fast as you can.\n\n
    #Equation lasts 5 seconds on the screen even after key press.\n
    #Please press the key only once.\n\n
    #Please press “space” to proceed.
    #"""
    
    #instructions_test_Chi = """在第三階段中，請根據之前看過的背景場景和人臉照片進行回答。\n
    #我們將先測試背景圖片或人臉的判斷，圖片會單獨出現。"""
    #instructions_test_Eng = """In this phase, please answer based on your best recollection \n
    #of the previously seen background and faces.\n
    #We would test the , and the picture will display on its own."""
    
    #instructions_end_Chi = """本實驗結束，謝謝！"""
    #instructions_end_Eng = """This is the End of the experiment.\nThank You!"""

    
    ### Set the response key
    #keypressLIST_space = ['space']
    #keypressLIST_enter = ["return"]
    #keypressLIST_alt = ["lalt, ralt"]  # lalt = left Alt; ralt = right Alt
    #keypressLIST_scale = ["space", "h", "j", "k", "l"]  # "space"==1, "h"==2, "j"==3, "k"==4, "l"==5  # use right hand for these keypress 

    ## Step_1: Show the instructions
    ## Welcome the participants
    #display_ins(instructions_welcome_Chi, keypressLIST_space)
    ## Display the instructions for experiment content and keypress
    #display_ins(instructions_study_Chi, keypressLIST_space)
    
    
    
    
    ## Saving the self_paced_rt result into csv file
    #dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,         # subject number
                           #'Date':dateLIST,               # when did the experiment happen
                           #'Emo_Condition':sub_condLIST,  # emotion condition
                           #'Trial_num':trialLIST,         # which trial
                           #'RT':rtLIST,                   # the rt for memory reations
                           #'Keypress':resultKeyLIST,      # which key they press
                           #'Scale':scaleLIST,             # How confidence they thought themselves (=what does the keypress mean)
                           #'Emotion':faceEmoLIST,         # which emotion of the face pic
                           #'Gender':genderLIST,           # the gender of the face pic
                           #'Ethnic':ethnicLIST,           # the ethnic of the face pic
                           #'Pic_seq':pic_seqLIST,         # the sequence of the pic (no matter it is Bg or face)
                           #'Face_path':pathLIST,          # the datapath of the face pic
                           #'Bg_path':BgLIST,              # the datapath of the background pic
                           #'Pic_Condition':old_newLIST    # the seen or not condition
                           #})
    
    ##data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    #file_name = 'Sub%s_%s_testPhase_results.csv' %(sub_id, sub_cond)
    #save_path = result_data_path / Path(file_name)
    #dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    
    #### Test Phase Ends ###

    ## close all the possible ongoing commands that could be running in the background
    #core.quit()  # normally we would add it, in case that anything happen