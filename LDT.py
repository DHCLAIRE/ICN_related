#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psychopy
from psychopy import visual, core, event, clock
import json
import random

'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
'''

# need to add feedbacks of scaling and texts records

def display(STR, keyPressLIST = None):
    """
    設定欲呈現的字串及指定的反應鍵後，將會呈現字串，並需按下指定反應鍵才會進到下一個字串。
    若未指定反應鍵，則任意鍵皆可換下一張刺激
    i.e display("啦啦啦", ['space'])
    """
    instructionsLIST = STR.split("\\\\")
    keyPressLIST = keyPressLIST
        
    for t in instructionsLIST:
        instructions = instructions_0 = visual.TextStim(win = win, text = t)
        instructions.draw()
        win.flip()
        event.waitKeys(keyList = keyPressLIST)

#def reactionLIST(key, resultLIST):
    
    
    #return resultLIST
        


if __name__ == "__main__":
    
    # Step_0: load in all the stimuli
    # testing stimuli (realwordLIST & pseudowordLIST)
    realwordLIST = ["blue", "green", "yellow", "red", "orange"]
    pseudowordLIST = ["thorpt", "rairn", "coan", "flatch", "meeg"]
    
    resultKeyLIST = [] # what we want to collect
    resultLIST = []  # for containing the response resultLIST
    tmpLIST = []
    
    
    # Step_1: Show the instructions
    win = visual.Window(size = [500, 500],color = [-1, -1, -1], units ="pix")
    clock = core.Clock()
    start_time = clock.getTime()

    
    instructions_1 = "接下來你會看到一串數字\n，請依照實驗指示進行按鍵反應\n，當你準備好的時候\n，請按下空白鍵\n"
    instructions_2 = "真詞按z 假詞按/\n請按空白鍵繼續\\\\將你的左食指輕放在z鍵，右食指輕放在/鍵。\n請按空白鍵繼續\\\\當字詞出現時，請盡快且正確的進行按鍵反應。\n請按空白鍵繼續"
    keypress = ['space']
    
    #Display the instructions
    display(instructions_1, keypress)
    
    display(instructions_2, keypress)
    
    # Display fixations
    fixations = visual.TextStim(win = win, text = "+")   # do I need to modifiy this??
    

    #core.wait(2)
    
    # Step_3: filp to a blank screen
    win.flip()
    
    
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for i in range(10):
        testing_stimuli = visual.TextStim(win = win, text = random.choice(realwordLIST))  # how to control that every words only
        testing_stimuli.draw()
        #core.wait(1)
        win.flip()
        
        keys = event.waitKeys(maxWait = 2, keyList = ['z', 'slash'])
        event.getKeys(keyList = ['z', 'slash'])
        fixations.draw()
        
        print(keys)
        
        # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
        if keys == ["z"]:
            keys = ["real_word"]
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 4)*1000    # normally 以毫秒作為單位
            print(time_duration)
            clock.reset()
        
        elif keys == ["slash"]:
            keys = ["pseudoword"]
            end_time = clock.getTime()
            time_duration = round(end_time - start_time, 4)*1000    # normally 以毫秒作為單位
            print(time_duration)
            clock.reset()
            
        else:
            keys = ["Wrong!!"]
            time_duration = 0
            print(time_duration)
            clock.reset()
        

        resultKeyLIST.append(keys)


    with open('/Users/ting-hsin/Docs/Github/ICN_related/LDT-testing-resultLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        json.dump(resultKeyLIST, jsonfile, ensure_ascii=False)

    
    # Step_5: remove the stimuli, and then show the blank screen for 1500ms (waiting for the participants to react)
    
    # Step_6: if the participanst react, then record the answer and the reaction time that were given by the participant, if not, then record a blank in the results
    
    # Step_7: once the results are filled, then show a blank screen for 700-1000ms
    
    # Step_8: to close the LDT.py, and then save all the results into a file

    # close the window  at the end of the experiment
    win.close()
    
    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen


    """
    # NOTES:
    
    from psychopy.visual  # 主要用這個
    
    # 前面要先設定螢幕視窗
    # win = psychopy.visual.Window(size = [500, 500], units ="pix")
    
    # key = psychopy.event.waitKeys()  # 按任何按鍵都會跳到下一張
    # event.getKeys(keyList = ['space'])  # 指定按鍵才可以跳到下一張  
    # 若指定按鍵沒有收到作業，這裡同時紀錄時間的要歸零，不然system會卡住
    
    #需要在寫if else 決定她按鍵反應時要怎記錄時間，然後press到哪個才會做反應
    
    # 按鍵反應 + 按鍵時間（RT）+ (trigger_for 腦波) + 正確與否
    # basic info = trails數（的第幾題）,trai_list(第幾次trial), sub_num, date, duration
    
    # added these two
    # clock.getTime()
    # clock.reset()
    
    # probably need to use dataframe to save all the reaction 
    """