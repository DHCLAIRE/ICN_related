#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
from psychopy.hardware import keyboard
import json

# something that is missing
'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
'''


if __name__ == "__main__":
    
    
    # testing stimuli (realwordLIST & pseudowordLIST)
    realwordLIST = ["blue", "green", "yellow", "red", "orange"]
    pseudowordLIST = ["thorpt", "rairn", "coan", "flatch", "meeg"]    
    resultKeyLIST = [] # what we want to collect
    tmpLIST = []
    # Step_1: load in all the stimuli to start the LDT.py, and show the instructions
    
    win = visual.Window(size = [500, 500], units ="pix")
    instructions_0 = visual.TextStim(win = win, text = "接下來你會看到一串數字\n，請依照實驗指示進行按鍵反應\n，當你準備好的時候\n，請按下空白鍵\n")  # 這裡中文字顯現的有點奇怪
    fixations = visual.TextStim(win = win, text = "+")
    
    resultLIST = []  # for contain the response resultLIST
    
    # for showing the instructions, and instruct them to press key to continue
    instructions_0.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])  # 沒有keylist的話，按任何按鍵都會跳到下一張  # 指定按鍵才可以跳到下一張，在這裡指的就是空白鍵
    
    instructions_1 = visual.TextStim(win = win, text = "真詞按z 假詞按/\n請按任意鍵繼續")  # 這裡中文字顯現的有點奇怪
    instructions_1.draw()
    win.flip()
    event.waitKeys()
    
    
    instructions_2 = visual.TextStim(win = win, text = "將你的左食指輕放在z鍵，右食指輕放在/鍵。\n請按任意鍵繼續")  # 這裡中文字顯現的有點奇怪
    instructions_2.draw()
    win.flip()
    event.waitKeys()       
    
    instructions_3 = visual.TextStim(win = win, text = "當字詞出現時，請盡快且正確的進行按鍵反應。\n請按任意鍵繼續")  # 這裡中文字顯現的有點奇怪
    instructions_3.draw()
    win.flip()
    event.waitKeys()  #keyList = ['z', '/']
    
    # Step_2: show the cross in the central of the screen
    # for showing the fixation ["+"]
    fixations.draw()
    win.flip()
    core.wait(2)
    
    # Step_3: filp to a blank screen
    win.flip()    
    
    #"""
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms  # randomly display would also be crucial!!
    for i in realwordLIST:
        testing_stimuli = visual.TextStim(win = win, text = i)
        testing_stimuli.draw()
        win.flip()
        #core.wait(2) #DON'T NEED THIS IN HERE! #the waiting time need to rethink about it, cause something is not right
        event.waitKeys(keyList = ["z", "slash"])
        keys = event.getKeys(keyList = ["z", "slash"], modifiers = True, timeStamped = False) # 再加上if else的判斷決定是否要收或是要怎麼紀錄這反應
        """
        # 按鍵反應 + 按鍵時間（RT）+ (trigger_for 腦波) + 正確與否
        # basic info = trails數（的第幾題）,trai_list(第幾次trial), sub_num, date, duration
        # added these two
        # clock.getTime()
        # clock.reset()
        """
        
        tmpLIST.append(keys)
    resultKeyLIST = tmpLIST
    #keys = event.getKeys(keyList = ['z', '/'], modifiers = False, timeStamped = False)
    
    #event.waitKeys(keyList = ['space'])
    
    
    #resultLIST = event.getKeys(keyList = [], modifiers = True, timeStamped = True)
    
    with open('/Users/ting-hsin/Docs/Github/ICN_related/LDT-testing-resultLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        json.dump(resultKeyLIST, jsonfile, ensure_ascii=False)
        
    
    
    
    # Step_5: remove the stimuli, and then show the blank screen for 1500ms (waiting for the participants to react)
    
    # Step_6: if the participanst react, then record the answer and the reaction time that were given by the participant, if not, then record a blank in the results 
    # event.getKeys() # this will give you the result of which key is being press
    
    
        
    """
        from psychopy.visual  # 主要用這個
    
        # 前面要先設定螢幕視窗
        win = psychopy.visual.Window(size = [500, 500], units ="pix")
        
        
        key = psychopy.event.waitKeys()  # 按任何按鍵都會跳到下一張
        event.getKeys(keyList = ['space'])  # 指定按鍵才可以跳到下一張  
        #若指定按鍵沒有收到作業，這裡同時紀錄時間的要歸零，不然system會卡住
        
        
        #需要在寫if else 決定她按鍵反應時要怎記錄時間，然後press到哪個才會做反應
        
    """
        
    # Step_7: once the results are filled, then show a blank screen for 700-1000ms
        
    
    # Step_8: to close the LDT.py, and then save all the results into a file

    # close the window
    win.close()
    
    # close all the possible ongoing commands that could be running in the background
    core.quit()  # normally we would add it, in case that anything happen
