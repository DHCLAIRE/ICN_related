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
from psychopy import visual, core, event, clock   #from psychopy import visual, core, event, gui, prefs, sound, monitors, clock,parallel
#import json
#import random
import numpy as np
from datetime import datetime,date
import pandas as pd


def display_ins(STR, keyPressLIST = None):
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
    win.flip()

def display_fix():
    """
    呈現"+"於螢幕中央
    """
    fixation = visual.TextStim(win = win, text = "+")
    fixation.draw()
    win.flip()


if __name__ == "__main__":
    
    # Stimuli Section
    # insert the stim-forming code?? >> or just present the selected texts per paragraphs??
    
    
    # Wanted data
    day = date.today()
    dateLIST = []
    sub_idLIST = []
    self_paced_rtLIST=[]
    text_noLIST = []
    resultKeyLIST = []
    
    # For key-in the id of the subject
    sub_id = str(input("Subject: "))
    
    # setting up the display win conditions
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    clock = core.Clock()
    start_time = clock.getTime()

    # Setting the instructions and the response key
    instructions_1 = """接下來你會看到一篇文章\n，請依照實驗指示進行按鍵反應\n，當你準備好的時候\n，請按下空白鍵\n"""
    instructions_2 = """請在紙上評分\n，評分完畢後請按下空白鍵繼續"""
    keypress = ['space']
    
    # Experiment section  # Two parts >> Comprehension(Learning phase) + LDT(Testing Phase)
    # Reading Comprehension Task STARTS
    for i in range(5):
        # display instructions for Reading Comprehension phase
        display_ins(instructions_1, keypress)
        #win.flip()
        core.wait(0.5)
        
        # display fixation in the central of the screen
        display_fix()
        core.wait(1)
        
        # display the stimuli, which would be a series of short texts
        testing_text = "LALALALLALALALALALALALLLAL"
        text = visual.TextStim(win = win, text = testing_text)
        print("text starts")
        text.draw()
        win.flip()
        
        # adding rating scale in here!!!!
        
        # setting up what keypress would allow the experiment to proceed
        keys = event.waitKeys(keyList = keypress)
        event.getKeys(keyList = keypress)
        print(keys)
        print("text ends")
        if keys == ["space"]:
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 3)*1000    # normally 以毫秒作為單位
            print(time_duration)
            print(type(time_duration))
            clock.reset()
        else:
            pass
        
        # making the wanted info into the List form for future use
        text_noLIST.append(i+1)
        dateLIST.append(day)
        sub_idLIST.append(sub_id)
        resultKeyLIST.append(keys)
        self_paced_rtLIST.append(time_duration)
        
        core.wait(0.5)
        
        # ask the participant to evaluate how well they understand the presented text
        display_ins(instructions_2, keypress)
        
        
    # close the window  at the end of the experiment
    win.close()
    
    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                       'Date':dateLIST,
                       'Self-paced RT':self_paced_rtLIST,
                       'Texts':text_noLIST})
    print(type(dataDICT))
    
    data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = sub_id + '_Reading_task.csv'
    save_path = data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen
    
    
    #### Should I seperate the Comprehension and the LDT task, or should I combine these two tasks together??
