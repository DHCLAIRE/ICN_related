#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import psychtoolbox as ptb
from psychopy import sound, core   # if you change the setting, this command must be put after the prefs's command
#import json
print(sound.Sound)

if __name__ == "__main__":
    #data_path = "/Volumes/Neurolang_1/Master Program/新碩論主題/Alice(EEG dataset and stimuli)/audio/"
    Alice_stm = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset and stimuli)/audio/DownTheRabbitHoleFinal_SoundFile{}.wav".format()
    
    
    for i in range(12):
        mySound = sound.Sound(Alice_stm)   #value=str(Alice_stm), secs = 60)
        #now = ptb.GetSecs()
        mySound.play()#when = now + 0.5)  # play in EXACTLY 0.5s
        core.wait(60)
        pass
    #"""