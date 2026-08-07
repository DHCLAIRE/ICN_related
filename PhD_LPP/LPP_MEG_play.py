#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Get a dictionary of all playback devices >> do this everytime we run the audio experiments
from psychopy.tools.systemtools import getAudioPlaybackDevices
from pprint import pprint 
device_list = getAudioPlaybackDevices()

print("\n--- Available Audio Playback Devices (via systemtools) ---")
pprint(device_list)
print("----------------------------------------------------------\n")

# For NTU-MEG audio experiment setting
from psychopy import prefs

# 1. Set the preferred audio library to PTB (or the one you want to use)
prefs.hardware['audioLib'] = ['PTB'] 
prefs.hardware['audioLatencyMode'] = 3
"""
# 2. Assign the exact device name
# Note: Ensure you are using the correct characters (喇叭)
#prefs.hardware['audioDevice'] = '喇叭 (Realtek(R) Audio)' 

# 3. Now you can import the sound module
#from psychopy import sound 

# Example: play a sound
# tone = sound.Sound(440, secs=0.5) 
# tone.play()


# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']
# Set other python packages
import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
#import json
print(sound.Sound)

import os
import csv
import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
#from pprint import pprint
import random

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

'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
'''

# =============================================================================
# 1. CUSTOM EXCEPTION & HELPER FUNCTIONS
# =============================================================================

class ExitProcedureException(Exception):
    """Custom exception raised to cleanly exit the listening procedure."""
    pass


def display_ins(win, text_str, key_list=None):
    """Displays instructions and waits for a keypress."""
    screens = text_str.split("\\\\")
    for t in screens:
        stim = visual.TextStim(win=win, text=t, height=0.08, wrapWidth=1.5)
        stim.draw()
        win.flip()
        event.waitKeys(keyList=key_list)
        win.flip()


def display_fix(win, duration=None):
    """Displays a central fixation cross."""
    fixation = visual.TextStim(win=win, text="+", height=0.15)
    fixation.draw()
    win.flip()
    if duration is not None:
        core.wait(duration)
        win.flip()


def play_audio_trial(file_name, port, writer=None, trial_info=None, 
                     onset_code=2, offset_code=4, data_path="audio/"):
    """
    Universal audio player: Plays ANY .wav file, sends MEG TTL triggers,
    checks for ESC to abort, and logs data to CSV.
    """
    full_path = os.path.join(data_path, file_name)
    
    # 1. Read exact duration
    sample_rate, data = wavfile.read(full_path)
    duration_sec = len(data) / sample_rate
    print(f"\n--- Playing: {file_name} (Duration: {duration_sec:.2f}s) ---")
    
    # 2. Load sound
    script_sound = sound.Sound(full_path)
    
    # 3. Onset Trigger & Playback
    script_sound.play()
    #port.setData(onset_code)
    core.wait(0.01)  # 10 ms TTL pulse
    #port.setData(0)
    
    # 4. Active listening loop (checks ESC key every 10 ms)
    timer = core.Clock()
    while timer.getTime() < duration_sec:
        keys = event.getKeys(keyList=['escape'])
        if 'escape' in keys:
            script_sound.stop()
            #port.setData(99)  # Abort trigger code
            core.wait(0.01)
            #port.setData(0)
            raise ExitProcedureException(f"Experiment aborted by user during {file_name}")
        
        core.wait(0.01)
    
    # 5. Offset Trigger
    #port.setData(offset_code)
    core.wait(0.01)
    #port.setData(0)
    
    print(f"{file_name} DONE.")
    
    # 6. Log to CSV
    if writer and trial_info is not None:
        writer.writerow(trial_info + [file_name, round(duration_sec, 4), "DONE"])
    
    core.wait(0.5)  # Brief delay before next event


# =============================================================================
# 2. MASTER EXPERIMENT CONTROLLER
# =============================================================================

def run_meg_experiment(sub_id, order_type, win, port, 
                       languages=["CHT", "ENG", "FRN"], data_path="audio/"):
    """
    Executes the full MEG experiment: displays instructions, plays tapes 
    followed by comprehension questions, and logs all events to one CSV file.
    """
    # Map counterbalanced orders (L1, L2, L3)
    order_map = {
        "Type A": [languages[0], languages[1], languages[2]],  # L1-L2-L3
        "Type B": [languages[0], languages[2], languages[1]],  # L1-L3-L2
        "Type C": [languages[1], languages[0], languages[2]],  # L2-L1-L3
        "Type D": [languages[1], languages[2], languages[0]],  # L2-L3-L1
        "Type E": [languages[2], languages[0], languages[1]],  # L3-L1-L2
        "Type F": [languages[2], languages[1], languages[0]]   # L3-L2-L1
    }
    
    if order_type not in order_map:
        raise ValueError(f"Invalid order_type '{order_type}'. Must be: {list(order_map.keys())}")
        
    selected_langs = order_map[order_type]
    
    # Assign Language Blocks -> (Language, Tape_Range)
    blocks = [
        (selected_langs[0], range(1, 4)),   # Block 1: Tapes 1 to 3
        (selected_langs[1], range(4, 7)),   # Block 2: Tapes 4 to 6
        (selected_langs[2], range(7, 10))   # Block 3: Tapes 7 to 9
    ]
    
    # Prepare single CSV log file
    clean_type = order_type.replace(" ", "")
    log_filename = f"LPP_S{sub_id}{clean_type}_{selected_langs[0]}_{selected_langs[1]}_{selected_langs[2]}.csv"
    
    try:
        with open(log_filename, mode='w', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            # Unified CSV Headers for both Story Tapes & Comprehension Qs
            writer.writerow(["sub_id", "order_type", "language", "stim_type", "item_num", 
                             "filename", "duration_sec", "status"])
            
            # Initial Experiment Welcome Screen
            display_ins(win, "Welcome to the Listening Experiment.\\\\Press SPACE to begin.", ['space'])
            
            # --- MAIN EXPERIMENT LOOP ---
            for block_idx, (lang, tape_range) in enumerate(blocks, start=1):
                
                # Display block instructions before switching languages
                display_ins(
                    win, 
                    f"Block {block_idx} of 3 ({lang}).\\\\Listen carefully to the story.\\\\Press SPACE when ready.", 
                    ['space']
                )
                
                for tape_num in tape_range:
                    # Show Fixation cross before story starts (1 second)
                    display_fix(win, duration=1.0)
                    
                    # ---------------------------------------------------------
                    # A. PLAY STORY TAPE
                    # ---------------------------------------------------------
                    tape_file = f"LPP_{lang}_tape_{tape_num}.wav"
                    play_audio_trial(
                        file_name=tape_file,
                        #port=port,
                        writer=writer,
                        trial_info=[sub_id, order_type, lang, "StoryTape", tape_num],
                        onset_code=10 + tape_num,   # Unique trigger per tape
                        offset_code=50 + tape_num,
                        data_path=data_path
                    )
                    
                    # ---------------------------------------------------------
                    # B. PLAY COMPREHENSION QUESTION
                    # ---------------------------------------------------------
                    question_file = f"LPP_{lang}_question_{tape_num}.wav"
                    play_audio_trial(
                        file_name=question_file,
                        #port=port,
                        writer=writer,
                        trial_info=[sub_id, order_type, lang, "ComprehensionQ", tape_num],
                        onset_code=100 + tape_num,  # Unique trigger per question
                        offset_code=150 + tape_num,
                        data_path=data_path
                    )
                    
                    # (Optional) Add your participant button-response recording here!
                    # e.g., record_participant_answer(win, port, writer, ...)
                    
                    # Short pause between trials
                    core.wait(1.0)
                    
            # Completion Screen
            display_ins(win, "You have completed the experiment!\\\\Thank you for your participation.", ['space'])
            print(f"\nAll 9 tapes completed successfully! Log saved to: {log_filename}")
            
    except ExitProcedureException as e:
        print(f"\n[ABORTED]: {e}")
        print(f"Data saved up to abort point in: {log_filename}")
        display_ins(win, "Experiment aborted by user.", ['space'])


# =============================================================================
# 3. RUNNER EXECUTION
# =============================================================================

if __name__ == "__main__":
    
    # Set Data path
    data_root_path = "/Volumes/DH_4GB/"
    results_data_path = "/Volumes/DH_4GB/LPP_Materials/"
    
    # Initialize PsychoPy Window & Hardware
    win = visual.Window(size=[500, 500], units="norm", fullscr=False)
    #meg_port = parallel.ParallelPort(address=0x0378)
    languages_typesLIST = ["CHT", "ENG", "FRN"]
    # Run Experiment (e.g., Sub '01', Type A order: CHT 1-3 -> ENG 4-6 -> FRN 7-9)
    run_meg_experiment(
        sub_id="01",
        order_type="Type A",
        win=win,
        #port=meg_port,
        languages=languages_typesLIST,
        data_path= data_root_path #"audio/"
    )
    
    win.close()
    core.quit()

##======OLD script BLOCK================================================================================================


#"""
#1. instructions >> press 'space'?? or other button?
#2. Button press >> one for each side (choose wisely)
#"""

## The AS-MEG trigger port info
##port = parallel.ParallelPort('0x0378')

###============== MEG 或 筆電 轉換 ==========================
##### MEG 正式跑： USE_TRIGGER = True、USE_KEYPORT = True
##### 筆電測試： USE_TRIGGER = False、USE_KEYPORT = False
###==========================================================

## The NTU-MEG trigger port info
#USE_TRIGGER = True  # 是否啟用平行埠 trigger（筆電測試可 False）
#LPT_ADDRESS = 0x4FF8  # 平行埠位址（依 MEG 系統設定）
#DEBUG_TRIGGER = False  # port 不可用時是否印 trigger（正式收資料建議 False）


#REFRESH_HZ = 60  # 螢幕刷新率（你已確認為 60Hz）
#WORD_ON_FRAMES = int(round(0.5 * REFRESH_HZ))  # Stage1 語詞呈現：0.5 秒 = 30 frames
#ITI_FRAMES = int(round(0.2 * REFRESH_HZ))  # Trial 間隔：0.2 秒 = 12 frames


#START_KEY = 'space'  # 開始鍵：空白鍵
#BREAK_KEY = 'return'  # 休息鍵：Enter（鍵名 return）
#END_KEY = 'return'  # 結束鍵：Enter（避免空白鍵誤觸）


#RESPONSE_MAP = {'1': '合理', '2': '不合理', '6': '合理', '7': '不合理'}  # 反應鍵對照（可只用 1/2）
#ALLOWED_KEYS = list(RESPONSE_MAP.keys()) + ['escape']  # 允許按鍵（加 escape 緊急中止）


## -------------------- 反應設定：鍵盤（筆電）/ keyport（MEG 反應盒） --------------------
#USE_KEYPORT = True  # MEG 室：True（用 keyport 讀 pin）；筆電測試：False（用鍵盤 1/2）
#KEYPORT_ADDR = 0x5FF8  # MEG 反應盒 keyport 位址（讀 pin）
#PIN_REASONABLE = 6     # 合理（紅色）
#PIN_UNREASONABLE = 7   # 不合理（黃色）


#if __name__ == "__main__":
    ## Set Data path
    #data_root_path = "/Volumes/DH_4GB/"
    #results_data_path = "/Volumes/DH_4GB/LPP_Materials/"

    ## sample_rate holds the sample rate of the wav file
    ## in (sample/sec) format
    ## data is the numpy array that consists
    ## of actual data read from the wav file

    ## display fixation
    ##display_fix()
    #instructions = """接下來你會聽到幾段故事，\n每段故事結束後會有一題單選題，\n請依照剛剛聽到的內容進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵開始"""
    #questionsLIST = [
        #"When Alice peeked into her sister's book on the bank, what did it NOT* have?\n1. No sign of her sister’s name.\n2. No pictures or conversations.\n3. No pages at all.\n4. No interesting story.",
        #"What two things are immediately most striking to Alice about the rabbit?\n1. It is talking and won't respond to her.\n2. It has a waistcoast-pocket and a watch.\n3. It is running late and yelling loudly.\n4. It walks and talks just as a human.",
        #"When Alice fell down the well, she took down a jar from one of the shelves as she passed. What was it labeled?\n1. Orange Marmalade\n2. Strawberry Marmalade\n3. Blueberry Jam\n4. Apricot Jam",
        #"When Alice thinks she might have fallen right through the earth and come out among people that walk backwards, what countries does she think they are from?\n1. Argentina\n2. United States and Canada\n3. India\n4. Australia and New Zealand",
        #"What is the name of Alice's cat?\n1. Selima\n2. Chester\n3. Dinah\n4. Felix",
        #"What does Alice land on at the bottom of the well?\n1. The hard stone floor\n2. An overstuffed armchair\n3. A heap of sticks and dry leaves\n4. A large, purple couch",
        #"What material is the key which Alice finds made of?\n1. Brass\n2. Silver\n3. Bronze\n4. Gold",
        #"What device does Alice 'shut up like'?\n1. A telescope\n2. A clam\n3. A bite\n4. A lantern",
        #"Drinking from the bottle has a variety of tastes. What does it NOT* taste like?\n1. Cherry tart\n2. Pineapple\n3. Tea\n4. Roast turkey",
        #"What are the effects of drinking from the bottle and eating the cake?\n1. Drinking makes Alice smaller and eating makes her larger.\n2. Drinking makes Alice larger and eating makes her smaller.\n3. Both drinking and eating make her smaller.\n4. Both drinking and eating make her larger.",
        #"Why did Alice box her own ears once?\n1. For checking out her new boxing gloves.\n2. For cheating herself in a game of croquet.\n3. For not knowing the capital of Bulgaria.\n4. For forgetting to give Dina her milk at tea-time.",
        #"Where did Alice find the cake?\n1. Floating in the pond of her tears.\n2. In a little wooden box that was lying on the table.\n3. In a little glass box that was lying under the table.\n4. She did not find it -- the rabbit gave it to her."
    #]

    #keypressLIST_space = ["space"]
    #keypressLIST_ans = ["1", "2", "3", "4"]

    ## Answer 12Qs wanted data
    #day = date.today()
    #dateLIST = []
    #sub_idLIST = []
    #Ques_textLIST = []
    #resultKeyLIST = []
    ##correctnessLIST = []
    #responseLIST = []
    #Q_numLIST = []
    
    

    ## key in number for notifying which subject it is
    #sub_id = str(input("Subject ID: "))
    #lang_typesSTR = str(input("Lang Type: "))
    #tape_numSTR = str(input("Tape Num: "))
    

    ## Full screen
    ##win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    ## Testing small screen
    #win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")

    ## display instructions
    #display_ins(instructions, keypressLIST_space)


    #for i in range(2):

        ## display "Start" to indicate the start of the audio
        #display_start()
        #core.wait(1)

        ## display fixation for subject to look at when listening to the tape
        #display_fix()

        ## get the length of each audio files of Alice in the Wonderland Chapter one
        #sample_rate, data = wavfile.read(data_path + 'DownTheRabbitHoleFinal_SoundFile{}.wav'.format(i+1))
        #len_data = len(data) # holds length of the numpy array
        #t = len_data / sample_rate # returns duration but in floats
        #print("SoundFile{} length = ".format(i+1), t)
        #print("SoundFile{} length = ".format(i+1), int(t+1))

        ## Play the audio files section by section
        #Alice_stm = data_path + "DownTheRabbitHoleFinal_SoundFile{}.wav".format(i+1)
        #Script_Sound = sound.Sound(Alice_stm)   #value=str(Alice_stm), secs = 60)
        ##now = ptb.GetSecs()
        #Script_Sound.play()

        ## TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        #port.setData(2) #This is open the trigger
        #core.wait(0.01) # Stay for 10 ms
        #port.setData(0) #This is close the trigger

        ## set core wait time that match with the length of each audio files
        #core.wait(int(t+1))

        ## TO MARK THE AUDIO FILE ENDS
        #port.setData(2) #This is open the trigger
        #core.wait(0.01) # Stay for 10 ms
        #port.setData(0) #This is close the trigger


        #print("SoundFile{}".format(i+1), "DONE")
        ##print("Pause for 5 seconds.")
        #core.wait(0.5)


        ## TO MARK THE QUESTION BEGINS
        #port.setData(2) #This is open the trigger
        #core.wait(0.01) # Stay for 10 ms
        #port.setData(0) #This is close the trigger

        #win.flip()

        ## Display the quesitons for each tape
        #ans_keypressSTR = display_ins(questionsLIST[i], keypressLIST_ans)

        ## TO MARK THE QUESTION ENDS
        #port.setData(2) #This is open the trigger
        #core.wait(0.01) # Stay for 10 ms
        #port.setData(0) #This is close the trigger

        ## making the wanted info into the List form for future use
        #sub_idLIST.append(sub_id)
        #dateLIST.append(day)
        #Ques_textLIST.append(questionsLIST[i])
        #responseLIST.append(ans_keypressSTR)
        #Q_numLIST.append(int(i+1))
        ##correctnessLIST.append(correctLIST)

        ## the Gap between each audio files
        ##core.wait(5)
        #print("Continue for the SoundFile{}".format(i+2))

        ## Add ESC could core.quit() function in the middle of the experiments process

    #print("FINISHIED!")
    ## close the window  at the end of the experiment
    #win.close()


    ## Saving the self_paced_rt result into csv file
    #dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             #'Date':dateLIST,
                             #'Q_num':Q_numLIST,
                             #'Stimuli':Ques_textLIST,
                             #'Response':responseLIST,
                             ##'LDT_RT':LDT_rtLIST,
                             ##'Correctness':correctnessLIST
                             #})

    ##data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    #file_name = sub_id + '_12Qs_results.csv'
    #save_path = results_data_path + file_name
    #dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    ## close all the Psychopy application
    #core.quit()
