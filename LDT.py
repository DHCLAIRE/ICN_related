#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import json

# something that is missing
'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
exclude other key press: don't  let the mispress botton to influence the  ongoing experiment 
'''

if __name__ == "__main__":
    
    # Step_1: load in all the stimuli to start the LDT.py, and show the instructions
    
    win = visual.Window(size = [500, 500], units ="pix")
    instructions = visual.TextStim(win = win, text = "接下來你會看到一串數字\n，請依照實驗指示進行按鍵反應\n，當你準備好的時候\n，請按下空白鍵\n")  # 這裡中文字顯現的有點奇怪
    fixations = visual.TextStim(win = win, text = "+")
    testing_stimuli = visual.TextStim(win = win, text = "word")
    resultLIST = []  # for contain the response resultLIST
    
    # for showing the instructions, and instruct them to press key to continue
    instructions.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])  # 沒有keylist的話，按任何按鍵都會跳到下一張  # 指定按鍵才可以跳到下一張，在這裡指的就是空白鍵
    
    # Step_2: show the cross in the central of the screen
    # for showing the fixation ["+"]
    fixations.draw()
    win.flip()
    core.wait(5)
    
    # Step_3: filp to a blank screen
    win.flip()
    
    
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms
    testing_stimuli.draw()
    win.flip()
    event.waitKeys()
    resultLIST = event.getKeys(keyList = None, modifiers = True, timeStamped = True)
    
    with open('/Users/ting-hsin/Downloads/LDT-testing-resultLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        json.dump(resultLIST, jsonfile, ensure_ascii=False)
        
    
    core.wait(3)
    
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
    
    
    
        
    
    
    
    
    
    