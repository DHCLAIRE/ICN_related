#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:50:02 2021

@author: neuroling
"""

from psychopy import visual #as psyv
from psychopy import core #as psyc

# something that is missing
'''
key press: need to be set (we'll use 2 bottons in here')
reaction time: need to be recorded
exclude other key press: don't  let the mispress botton to influence the  ongoing experiment 
'''



if __name__ == "__main__":
    
    # Step_1: load in all the stimuli to start the LDT.py, and show the instructions
    win = visual.Window(size = [500, 500], units ="pix")
    msg = visual.TextStim(win, text=u"Hellooooooooooooo")
            
    win.flip()
    msg.draw()
    core.wait(3)
    
    
    win.close()
    
    core.quit()
        
    # why does it can only produce once?? and it will be almost not possible to show for the second time
        
    # Step_2: show the cross in the central of the screen
        
    # Step_3: filp to a blank screen
        
        
    # Step_4: show the stimuli(real words or pseudowords), and remain the stimuli for 400ms
        
        
    # Step_5: remove the stimuli, and then show the blank screen for 1500ms (waiting for the participants to react)
        
    # Step_6: if the participanst react, then record the answer and the reaction time that were given by the participant, if not, then record a blank in the results 
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
        
    
    
    
    
    
    