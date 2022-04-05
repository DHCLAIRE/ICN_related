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

# for LDT
import psychopy
from psychopy import visual, core, event, clock   #from psychopy import visual, core, event, gui, prefs, sound, monitors, clock,parallel
#import json
#import random
import numpy as np
from datetime import datetime,date
import pandas as pd


# Self-paced reading
# 


def display(STR, keyPressLIST = None):
    """
    設定欲呈現的字串及指定的反應鍵後，將會呈現字串，並需按下指定反應鍵才會進到下一個字串。
    若未指定反應鍵，則任意鍵皆可換下一張刺激
    i.e display("啦啦啦", ['space'])
    """
    instructionsLIST = STR.split("\\\\")
    keyPressLIST = keyPressLIST
        
    for t in instructionsLIST:
        instructions = visual.TextStim(win = win, text = t)
        instructions.draw()
        win.flip()
        event.waitKeys(keyList = keyPressLIST)
        


if __name__ == "__main__":
    
    # Stimuli Section
    # insert the stim-forming code?? >> or just present the selected texts per paragraphs??
    
    
    # Wanted data
    day = date.today()
    date = []
    sub_id = []
    self_paced_rtLIST=[]
    tmpResultLIST = []
    resultKeyLIST = []
    """
    response=[]
    response_time=[]
    trial_no=[]
    clock=psychopy.core.Clock()
    keys=[]
    ran_dur=[]
    interval=[]
    """
    sub_id = str(input("Subject: "))
    
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    clock = core.Clock()
    start_time = clock.getTime()

    
    instructions_1 = "接下來你會看到一串數字\n，請依照實驗指示進行按鍵反應\n，當你準備好的時候\n，請按下空白鍵\n"
    instructions_2 = "真詞按z 假詞按/\n請按空白鍵繼續\\\\將你的左食指輕放在z鍵，右食指輕放在/鍵。\n請按空白鍵繼續\\\\當字詞出現時，請盡快且正確的進行按鍵反應。\n請按空白鍵繼續"
    keypress = ['space']
    
    #Display the instructions
    #display(instructions_1, keypress)
    
    #display(instructions_2, keypress)
    
    # Step_3: filp to a blank screen
    #win.flip()
    
    
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for i in range(5):
        #display(instructions_1, keypress)
        
        #testing_stim = 
        display(instructions_1, keypress)  # how to control that every words only
        win.flip()
        
        
        # adding rating scale in here!!!!
        
        
        keys = event.waitKeys(keyList = keypress)
        event.getKeys(keyList = keypress)
        
        print(keys)
        
        # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
        if keys == ["space"]:
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 4)*1000    # normally 以毫秒作為單位
            print(time_duration)
            print(type(time_duration))
            clock.reset()
        else:
            pass

        resultKeyLIST.append(keys)
        self_paced_rtLIST.append(time_duration)
    tmpResultLIST.append(resultKeyLIST)
    tmpResultLIST.append(self_paced_rtLIST)

    with open('/Users/ting-hsin/Docs/Github/ICN_related/LTTC-testing-resultLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        json.dump(tmpResultLIST, jsonfile, ensure_ascii=False)
    
    
    # close the window  at the end of the experiment
    win.close()
    
    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen

    
    # Experiment section  # Two parts >> Comprehension(Learning phase) + LDT(Testing Phase)