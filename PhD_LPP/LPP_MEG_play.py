#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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

# 2. Assign the exact device name
# Note: Ensure you are using the correct characters (喇叭)
#prefs.hardware['audioDevice'] = '喇叭 (Realtek(R) Audio)' 

# 3. Now you can import the sound module
#from psychopy import sound 

# Example: play a sound
# tone = sound.Sound(440, secs=0.5) 
# tone.play()


# To Change the backend setting to PTB
#from psychopy import prefs
#prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']
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

class ExitProcedureException(Exception):
    """Custom exception raised to cleanly exit the listening procedure."""
    pass


def play_language_tape_slice(sub_id, order_type, port, lang, tape_range, 
                             writer, data_path="audio/"):
    """
    Plays a specific slice of tapes for a single language, sends MEG triggers,
    and logs each trial to an open CSV writer.
    
    Parameters:
        sub_id (str): Subject ID
        order_type (str): e.g., 'Type A'
        port: Initialized PsychoPy parallel port object
        lang (str): Language code to play (e.g., 'CHT')
        tape_range (range or list): Sequence of tape numbers (e.g., range(1, 4))
        writer: Python csv.writer object for logging
        data_path (str): Directory where wav files are stored
    """
    for tape_num in tape_range:
        file_name = f"LPP_{lang}_tape_{tape_num}.wav"
        full_path = os.path.join(data_path, file_name)
        
        # 1. Read exact audio duration
        sample_rate, data = wavfile.read(full_path)
        duration_sec = len(data) / sample_rate
        print(f"\n--- Playing: {file_name} (Duration: {duration_sec:.2f}s) ---")
        
        # 2. Load audio
        script_sound = sound.Sound(full_path)
        
        # --- 3. START PLAYBACK & SEND ONSET TRIGGER ---
        script_sound.play()
        
        port.setData(2)
        core.wait(0.01)  # 10 ms pulse width
        port.setData(0)
        
        # 4. Active listening loop (allows ESC or Click to abort cleanly)
        timer = core.Clock()
        while timer.getTime() < duration_sec:
            keys = event.getKeys(keyList=['escape'])
            if 'escape' in keys:
                script_sound.stop()
                port.setData(99)  # Optional: Send an "aborted" trigger code to MEG
                core.wait(0.01)
                port.setData(0)
                raise ExitProcedureException("Experiment aborted by user via ESC key.")
            
            core.wait(0.01)  # Small yield to prevent CPU hogging
        
        # --- 5. SEND OFFSET TRIGGER ---
        port.setData(4)
        core.wait(0.01)
        port.setData(0)
        
        print(f"{file_name} DONE.")
        
        # 6. Log completion
        writer.writerow([lang, tape_num, file_name, round(duration_sec, 4), "DONE"])
        
        # Inter-Trial Interval (1 second between tapes)
        core.wait(1.0)


"""
def run_meg_experiment(sub_id, order_type, port, languages=["CHT", "ENG", "FRN"], 
                       data_path="audio/"):
    """
    Master controller: Sets up logging, determines language order, and executes 
    tape slices (1-3, 4-6, 7-9) by calling play_language_tape_slice three times.
    
    languages: A list where index 0 = L1, index 1 = L2, index 2 = L3.
    """
    # 1. Map order types to language presentation sequences
    order_map = {
        "Type A": [languages[0], languages[1], languages[2]],  # L1-L2-L3
        "Type B": [languages[0], languages[2], languages[1]],  # L1-L3-L2
        "Type C": [languages[1], languages[0], languages[2]],  # L2-L1-L3
        "Type D": [languages[1], languages[2], languages[0]],  # L2-L3-L1
        "Type E": [languages[2], languages[0], languages[1]],  # L3-L1-L2
        "Type F": [languages[2], languages[1], languages[0]]   # L3-L2-L1
    }
    
    if order_type not in order_map:
        raise ValueError(f"Invalid order_type '{order_type}'. Must be one of: {list(order_map.keys())}")
        
    selected_langs = order_map[order_type]
    
    # 2. Prepare behavioral data logging file
    clean_type = order_type.replace(" ", "")
    log_filename = f"LPP_S{sub_id}{clean_type}_{selected_langs[0]}_{selected_langs[1]}_{selected_langs[2]}.csv"
    
    try:
        with open(log_filename, mode='w', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(["language", "tape_num", "filename", "duration_sec", "status"])
            
            # --- CALL 1: First Language (Tapes 1 to 3) ---
            print(f"\n=== STARTING BLOCK 1: {selected_langs[0]} (Tapes 1-3) ===")
            play_language_tape_slice(
                sub_id, order_type, port, 
                lang=selected_langs[0], 
                tape_range=range(1, 4),  # Plays tapes 1, 2, 3
                writer=writer, 
                data_path=data_path
            )
            
            # --- CALL 2: Second Language (Tapes 4 to 6) ---
            print(f"\n=== STARTING BLOCK 2: {selected_langs[1]} (Tapes 4-6) ===")
            play_language_tape_slice(
                sub_id, order_type, port, 
                lang=selected_langs[1], 
                tape_range=range(4, 7),  # Plays tapes 4, 5, 6
                writer=writer, 
                data_path=data_path
            )
            
            # --- CALL 3: Third Language (Tapes 7 to 9) ---
            print(f"\n=== STARTING BLOCK 3: {selected_langs[2]} (Tapes 7-9) ===")
            play_language_tape_slice(
                sub_id, order_type, port, 
                lang=selected_langs[2], 
                tape_range=range(7, 10), # Plays tapes 7, 8, 9
                writer=writer, 
                data_path=data_path
            )
            
        print(f"\nAll 9 tapes completed successfully! Log saved to: {log_filename}")
        
    except ExitProcedureException as e:
        print(f"\n[ABORTED]: {e}")
        print(f"Partial data up to the abort point was saved to: {log_filename}")
"""


    from psychopy import visual, event, core
    
def display_ins(STR, keyPressLIST=None):
    """
    Displays instruction text on the screen and waits for a specific key press 
    to proceed to the next text screen.
    
    If 'STR' contains the delimiter '\\\\', it splits the string into multiple 
    sequential screens. If 'keyPressLIST' is None, pressing any key will advance 
    to the next screen.
    
    Example usage:
        display_ins("Welcome to the experiment!\\\\Press SPACE to start.", ['space'])
    """
    instructionsLIST = STR.split("\\\\")
    
    for t in instructionsLIST:
        instructions = visual.TextStim(win=win, text=t)
        instructions.draw()
        win.flip()
        event.waitKeys(keyList=keyPressLIST)
        win.flip()  # Clears the screen after the key is pressed

def display_fix(duration=None):
    """
    Displays a white fixation cross ('+') at the center of the screen.
    
    Parameters:
        duration (float, optional): Time in seconds to hold the fixation cross 
                                    on screen. If None, it just draws and flips 
                                    without pausing execution.
    """
    fixation = visual.TextStim(win=win, text="+")
    fixation.draw()
    win.flip()
    
    if duration is not None:
        core.wait(duration)
        win.flip()  # Clears the screen after the duration expires

"""
1. instructions >> press 'space'?? or other button?
2. Button press >> one for each side (choose wisely)
"""

# The AS-MEG trigger port info
#port = parallel.ParallelPort('0x0378')

##============== MEG 或 筆電 轉換 ==========================
#### MEG 正式跑： USE_TRIGGER = True、USE_KEYPORT = True
#### 筆電測試： USE_TRIGGER = False、USE_KEYPORT = False
##==========================================================

# The NTU-MEG trigger port info
USE_TRIGGER = True  # 是否啟用平行埠 trigger（筆電測試可 False）
LPT_ADDRESS = 0x4FF8  # 平行埠位址（依 MEG 系統設定）
DEBUG_TRIGGER = False  # port 不可用時是否印 trigger（正式收資料建議 False）


REFRESH_HZ = 60  # 螢幕刷新率（你已確認為 60Hz）
WORD_ON_FRAMES = int(round(0.5 * REFRESH_HZ))  # Stage1 語詞呈現：0.5 秒 = 30 frames
ITI_FRAMES = int(round(0.2 * REFRESH_HZ))  # Trial 間隔：0.2 秒 = 12 frames


START_KEY = 'space'  # 開始鍵：空白鍵
BREAK_KEY = 'return'  # 休息鍵：Enter（鍵名 return）
END_KEY = 'return'  # 結束鍵：Enter（避免空白鍵誤觸）


RESPONSE_MAP = {'1': '合理', '2': '不合理', '6': '合理', '7': '不合理'}  # 反應鍵對照（可只用 1/2）
ALLOWED_KEYS = list(RESPONSE_MAP.keys()) + ['escape']  # 允許按鍵（加 escape 緊急中止）


# -------------------- 反應設定：鍵盤（筆電）/ keyport（MEG 反應盒） --------------------
USE_KEYPORT = True  # MEG 室：True（用 keyport 讀 pin）；筆電測試：False（用鍵盤 1/2）
KEYPORT_ADDR = 0x5FF8  # MEG 反應盒 keyport 位址（讀 pin）
PIN_REASONABLE = 6     # 合理（紅色）
PIN_UNREASONABLE = 7   # 不合理（黃色）


if __name__ == "__main__":
    # Set Data path
    data_root_path = "/Volumes/DH_4GB/"
    results_data_path = "/Volumes/DH_4GB/LPP_Materials/"

    # sample_rate holds the sample rate of the wav file
    # in (sample/sec) format
    # data is the numpy array that consists
    # of actual data read from the wav file

    # display fixation
    #display_fix()
    instructions = """接下來你會聽到幾段故事，\n每段故事結束後會有一題單選題，\n請依照剛剛聽到的內容進行按鍵反應，\n當你準備好的時候，\n請按下空白鍵開始"""
    questionsLIST = [
        "When Alice peeked into her sister's book on the bank, what did it NOT* have?\n1. No sign of her sister’s name.\n2. No pictures or conversations.\n3. No pages at all.\n4. No interesting story.",
        "What two things are immediately most striking to Alice about the rabbit?\n1. It is talking and won't respond to her.\n2. It has a waistcoast-pocket and a watch.\n3. It is running late and yelling loudly.\n4. It walks and talks just as a human.",
        "When Alice fell down the well, she took down a jar from one of the shelves as she passed. What was it labeled?\n1. Orange Marmalade\n2. Strawberry Marmalade\n3. Blueberry Jam\n4. Apricot Jam",
        "When Alice thinks she might have fallen right through the earth and come out among people that walk backwards, what countries does she think they are from?\n1. Argentina\n2. United States and Canada\n3. India\n4. Australia and New Zealand",
        "What is the name of Alice's cat?\n1. Selima\n2. Chester\n3. Dinah\n4. Felix",
        "What does Alice land on at the bottom of the well?\n1. The hard stone floor\n2. An overstuffed armchair\n3. A heap of sticks and dry leaves\n4. A large, purple couch",
        "What material is the key which Alice finds made of?\n1. Brass\n2. Silver\n3. Bronze\n4. Gold",
        "What device does Alice 'shut up like'?\n1. A telescope\n2. A clam\n3. A bite\n4. A lantern",
        "Drinking from the bottle has a variety of tastes. What does it NOT* taste like?\n1. Cherry tart\n2. Pineapple\n3. Tea\n4. Roast turkey",
        "What are the effects of drinking from the bottle and eating the cake?\n1. Drinking makes Alice smaller and eating makes her larger.\n2. Drinking makes Alice larger and eating makes her smaller.\n3. Both drinking and eating make her smaller.\n4. Both drinking and eating make her larger.",
        "Why did Alice box her own ears once?\n1. For checking out her new boxing gloves.\n2. For cheating herself in a game of croquet.\n3. For not knowing the capital of Bulgaria.\n4. For forgetting to give Dina her milk at tea-time.",
        "Where did Alice find the cake?\n1. Floating in the pond of her tears.\n2. In a little wooden box that was lying on the table.\n3. In a little glass box that was lying under the table.\n4. She did not find it -- the rabbit gave it to her."
    ]

    keypressLIST_space = ["space"]
    keypressLIST_ans = ["1", "2", "3", "4"]

    # Answer 12Qs wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    Ques_textLIST = []
    resultKeyLIST = []
    #correctnessLIST = []
    responseLIST = []
    Q_numLIST = []
    
    

    # key in number for notifying which subject it is
    sub_id = str(input("Subject ID: "))
    lang_typesSTR = str(input("Lang Type: "))
    tape_numSTR = str(input("Tape Num: "))
    

    # Full screen
    #win = visual.Window(color = [-1, -1, -1], units ="pix", fullscr = True)   # Present screen_Full
    # Testing small screen
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")

    # display instructions
    display_ins(instructions, keypressLIST_space)


    for i in range(2):

        # display "Start" to indicate the start of the audio
        display_start()
        core.wait(1)

        # display fixation for subject to look at when listening to the tape
        display_fix()

        # get the length of each audio files of Alice in the Wonderland Chapter one
        sample_rate, data = wavfile.read(data_path + 'DownTheRabbitHoleFinal_SoundFile{}.wav'.format(i+1))
        len_data = len(data) # holds length of the numpy array
        t = len_data / sample_rate # returns duration but in floats
        print("SoundFile{} length = ".format(i+1), t)
        print("SoundFile{} length = ".format(i+1), int(t+1))

        # Play the audio files section by section
        Alice_stm = data_path + "DownTheRabbitHoleFinal_SoundFile{}.wav".format(i+1)
        Script_Sound = sound.Sound(Alice_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        Script_Sound.play()

        # TO MARK THE AUDIO FILE BEGINS  # This is the trigger_marker for marking the start of the audio file
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger

        # set core wait time that match with the length of each audio files
        core.wait(int(t+1))

        # TO MARK THE AUDIO FILE ENDS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger


        print("SoundFile{}".format(i+1), "DONE")
        #print("Pause for 5 seconds.")
        core.wait(0.5)


        # TO MARK THE QUESTION BEGINS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger

        win.flip()

        # Display the quesitons for each tape
        ans_keypressSTR = display_ins(questionsLIST[i], keypressLIST_ans)

        # TO MARK THE QUESTION ENDS
        port.setData(2) #This is open the trigger
        core.wait(0.01) # Stay for 10 ms
        port.setData(0) #This is close the trigger

        # making the wanted info into the List form for future use
        sub_idLIST.append(sub_id)
        dateLIST.append(day)
        Ques_textLIST.append(questionsLIST[i])
        responseLIST.append(ans_keypressSTR)
        Q_numLIST.append(int(i+1))
        #correctnessLIST.append(correctLIST)

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
                             'Q_num':Q_numLIST,
                             'Stimuli':Ques_textLIST,
                             'Response':responseLIST,
                             #'LDT_RT':LDT_rtLIST,
                             #'Correctness':correctnessLIST
                             })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = sub_id + '_12Qs_results.csv'
    save_path = results_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the Psychopy application
    core.quit()
