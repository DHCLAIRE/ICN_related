#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
For stimuli formation and selection

Steps:
1. (DONE)create a list that only have 12 pseudowords
2. (DONE)import the pseudoword list
3. (DONE)randomly select 6 out of the list of 12 pseudowords as the target words
4. (DONE)select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
5. (DONE)import all the pre-selected bunch of texts
6. divided all the pre-selected texts into the High-CD and Low-CD sets
7. randomly selelct a pair set of High-CD and Low-CD texts
8. insert the assigned pseudowords into the pair set of High-CD and Low-CD texts
# The pseudowords need to be inseted in the texts first, and then randomly choose from the texts set??

'''

# for stimuli
from pprint import pprint
import csv
import json
import random
from random import sample

# for LDT and Reading Comprehension Task
import psychopy
from psychopy import visual, core, event, clock, parallel   #from psychopy import visual, core, event, gui, prefs, sound, monitors, clock,parallel
#import json
#import random
import numpy as np
from datetime import datetime,date
import pandas as pd

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
    
def display_start():
    '''
    呈現"Start"於螢幕中央，暗示音檔即將要播出了。
    '''
    fixation = visual.TextStim(win = win, text = "Start")
    fixation.draw()
    win.flip()


# The MEG trigger port info
#port = parallel.ParallelPort('0x0378')

# Parts that Need to modify
"""
1. Scaling part >> change it to the new way of keeping them awake??
2. instructions >> press 'space'?? or other button?
3. Button press >> for continue the audio??? or 3 parts, 10/10/10
"""
# 

if __name__ == "__main__":
    # For key-in the id of the subject
    sub_id = str(input("Subject: "))
    
    stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/S%s_audios/" %(sub_id, sub_id)
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id
    #text_data_path = "C:/Users/user/Documents/DINGHSIN/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/"
    textSets_data_path = "I:/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets/"
    #C:/Users/user/Documents/DINGHSIN/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets

    # Stimuli Section
    # insert the stim-forming code?? >> or just present the selected texts per paragraphs??

    # Wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    self_paced_rtLIST=[]
    text_noLIST = []
    resultKeyLIST = []

    # setting up the display win conditions
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)
    clock = core.Clock()
    #start_time = clock.getTime()

    # Setting the instructions and the response key
    instructions_1 = """接下來你會聽到幾篇文章，\n請依照實驗指示進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵"""  #"""接下來你會聽到幾段文章，\n每段文章結束後會需要請你評分，\n請依照剛剛聽到的內容進行理解度評分，\n中間會有休息時間，\n請按下空白鍵開始"""
    instructions_2 = """請問對於剛剛那一篇文章理解了多少？\n請評分，評分完畢後\n將會準備進到下一篇"""  #"""請問對於剛剛那一篇文章理解了多少？\n請以1～4分評分，\n1分為完全不理解，4分為非常理解\n評分完畢後，將會直接播放下一篇文章\n請評分"""
    instructions_3 = """現在為2分鐘的休息時間\n請稍作休息，\n準備好後將會開始播放下一階段的文章"""
    keypressLIST_space = ["space"]
    keypressLIST_ans = ["1", "2", "3", "4"]

    # for pseudoword data
    tmpLIST = []
    tmpLIST_2 = []
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    words_high_CD_setLIST = []
    words_low_CD_setLIST = []
    texts_high_CD_setLIST = []
    texts_low_CD_setLIST = []

    """
    # 2_Import the pseudoword list (in json file form)
    with open (stim_data_path + "LTTC-pseudowordLIST.json", "r", encoding = "utf-8") as jfile:
        pseudoLIST = json.load(jfile)
        print("12 pseudowords = ", pseudoLIST)

    # 3_Randomly select 6 out of the list of 12 pseudowords as the target words
        # randomly select 6 target pseudowords from the list
        targetPseudoLIST = sample(pseudoLIST, 6)

        # collect other 6 pseudowords as the control group
        for t in pseudoLIST:
            if t not in targetPseudoLIST:
                controlPseudoLIST.extend([t])
            else:
                pass

        print("The TargetPseudo words = ", targetPseudoLIST)
        print("The ControlPseudo words = ", controlPseudoLIST)

    # 4_Select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
        words_high_CD_setLIST = sample(targetPseudoLIST, 3)

        for w in targetPseudoLIST:
            if w not in words_high_CD_setLIST:
                words_low_CD_setLIST.extend([w])
            else:
                pass

        print("High-CD_set = ", words_high_CD_setLIST)
        print("Low-CD_set = ", words_low_CD_setLIST)

        """
    """
    # Load in the stim_texts
    # for the stim_texts data
    textSetsLIST_High = []
    textSetsLIST_Low = []
    new_High_textSetsLIST = []
    new_Low_textSetsLIST = []
    High_stimLIST = []
    High_stim_SetLIST = []
    Low_stimLIST = []
    Low_stim_SetLIST = []
    total_stimSetLIST = []
    shuffledTotalT_LIST = []
    rating_LIST = []


    # for calling out the sets individually
    HightSetsLIST = []
    LowtSetsLIST = []
    Setsinfo_LIST = []

    # High_CD Set TEXTS
    # texts_high_CD_setLIST = [345, 456, 567, 367, 347]
    HighCD_CallingLIST = [["3", "4", "5"], ["4", "5", "6"], ["5", "6", "7"], ["3", "6", "7"], ["3", "4", "7"]]
    LowCD_CallingLIST = [["1", "2", "8"], ["2", "8", "9"], ["8", "9", "10"], ["1", "9", "10"], ["1", "2", "10"]]
    HightSetsLIST = random.sample(HighCD_CallingLIST, 1)
    LowtSetsLIST = random.sample(LowCD_CallingLIST, 1)
    print(HightSetsLIST)
    print(HightSetsLIST[0][0])
    print(LowtSetsLIST)
    print(LowtSetsLIST[0][0])

    Setsinfo_LIST.extend(HightSetsLIST)
    Setsinfo_LIST.extend(LowtSetsLIST)
    """

    #for sets in range(3):
    """
        # High_CD Set TEXTS
        with open (textSets_data_path + "sets_{}_LIST.json".format(HightSetsLIST[0][sets]), "r", encoding = "utf-8") as jfile_3:
            textSetsLIST_High = json.load(jfile_3)

            # randomly select 5 texts from the json file
            High_stimLIST = random.sample(textSetsLIST_High, 5)
            #pprint(High_stimLIST)
            #print(len(High_stimLIST))

            # replace {} to the assigned pseudowords by different condition
            for tSTR in High_stimLIST:
                new_tSTR = tSTR.replace("{}", words_high_CD_setLIST[sets])
                #pprint(new_tSTR)
                new_High_textSetsLIST.extend([new_tSTR])

        # Low_CD Set TEXTS
        # texts_low_CD_setLIST = [128, 289, 890, 190, 120]
        with open (textSets_data_path + "sets_{}_LIST.json".format(LowtSetsLIST[0][sets]), "r", encoding = "utf-8") as jfile_4:
            textSetsLIST_Low = json.load(jfile_4)

            # randomly select 5 texts from the json file
            Low_stimLIST = random.sample(textSetsLIST_Low, 5)
            #pprint(Low_stimLIST)
            #print(len(Low_stimLIST))

            # replace {} to the assigned pseudowords by different condition
            for tSTR in Low_stimLIST:
                new_tSTR = tSTR.replace("{}", words_low_CD_setLIST[sets])
                #pprint(new_tSTR)
                new_Low_textSetsLIST.extend([new_tSTR])

    #pprint(new_High_textSetsLIST)
    #print(len(new_High_textSetsLIST))
    #pprint(new_Low_textSetsLIST)
    #print(len(new_Low_textSetsLIST))

    # Combine the High & Low texts into one LIST
    total_stimSetLIST.extend(new_High_textSetsLIST)
    total_stimSetLIST.extend(new_Low_textSetsLIST)

    # Shuffle the texts so that the texts would be randomized
    random.shuffle(total_stimSetLIST)
    """

    # Experiment section
    # Reading Comprehension Task STARTS
    for i in range(2):  # need to loop a total 3 times
        
        # display instructions for Reading Comprehension phase
        display_ins(instructions_1, keypressLIST_space)
        #win.flip()
        core.wait(0.5)
        
        for tapeINT in range(3): # need to loop a total 10 times
            
            # display "Start" to indicate the start of the audio
            display_start()
            core.wait(1)
    
            # display fixation for subject to look at when listening to the tape
            display_fix()
    
            # get the length of each audio files of every text
            sample_rate, data = wavfile.read(stim_data_path + "S%s_textaudio_modified_%02d.wav" %(sub_id, tapeINT+1))   # the %s value in here will need to rewrite
            len_data = len(data) # holds length of the numpy array
            t = len_data / sample_rate # returns duration but in floats
            print("SoundFile{} length = ".format(tapeINT+1), t)
            print("SoundFile{} length = ".format(tapeINT+1), int(tapeINT+1))
    
            # Play the audio files section by section
            LTTC_audio_stm = stim_data_path + "S%s_textaudio_modified_%02d.wav" %(sub_id, tapeINT+1)
            Script_Sound = sound.Sound(LTTC_audio_stm)   #value=str(Alice_stm), secs = 60)
            #now = ptb.GetSecs()
            Script_Sound.play()
            
            """
            # TO MARK THE AUDIO FILE BEGINS
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            """            
            
            # display instructions for Listening Comprehension rating
            display_ins(instructions_2, keypressLIST_ans)
            #win.flip()
            core.wait(0.5)
            
            
            """
            # display instructions for Reading Comprehension phase
            display_ins(instructions_1, keypress)
            #win.flip()
            core.wait(0.5)

            # display fixation in the central of the screen
            display_fix()
            core.wait(1)

            start_time = clock.getTime()
            # display the stimuli, which would be a series of short texts
            testing_text = i
            text = visual.TextStim(win = win, text = testing_text)
            print("text starts")
            text.draw()
            """

            win.flip()

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
            
            """
            # TO MARK THE AUDIO FILE ENDS
            port.setData(2) #This is open the trigger
            core.wait(0.01) # Stay for 10 ms
            port.setData(0) #This is close the trigger
            """
            # making the wanted info into the List form for future use
            text_noLIST.append(int(total_stimSetLIST.index(i))+1)
            dateLIST.append(day)
            sub_idLIST.append(sub_id)
            resultKeyLIST.append(keys)
            self_paced_rtLIST.append(time_duration)
            shuffledTotalT_LIST.append([i])
            rating_LIST.append([""])

            core.wait(0.5)

        # ask the participant to evaluate how well they understand the presented text
        display_ins(instructions_3, keypressLIST_space)


    # close the window  at the end of the experiment
    win.close()

    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                       'Date':dateLIST,
                       'Texts_no':text_noLIST,
                       'Self-paced RT':self_paced_rtLIST,
                       'Rating Scale': rating_LIST,
                       'Text content': shuffledTotalT_LIST
                       })

    pseudoDICT = {"The TargetPseudo group_6":targetPseudoLIST,
                  "The ControlPseudo group_6": controlPseudoLIST,
                  "High_CD condition pseudowords_3":words_high_CD_setLIST,
                  "Low_CD condition pseudowords_3":words_low_CD_setLIST}

    textsDICT = {"The High-Low Set Group": Setsinfo_LIST,
                 "High_textSetsLIST": new_High_textSetsLIST,
                 "Low_textSetsLIST":new_Low_textSetsLIST,
                 "Total_stimSetLIST":total_stimSetLIST}


    #print(type(dataDICT))

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related"
    file_name = sub_id + '_Reading_task.csv'
    fsave_path = result_data_path + file_name
    dataDICT.to_csv(fsave_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    DICT_name = sub_id + '_pseudowordsDICT.json'
    Dsave_path = result_data_path + DICT_name
    with open(Dsave_path, "w", newline='', encoding="UTF-8") as jsfile:
        json.dump(pseudoDICT, jsfile, ensure_ascii=False)

    Text_name = sub_id + '_textsDICT.json'
    Tsave_path = result_data_path + Text_name
    with open(Tsave_path, "w", newline='', encoding="UTF-8") as jsfile_2:
        json.dump(textsDICT, jsfile_2, ensure_ascii=False)


    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen
