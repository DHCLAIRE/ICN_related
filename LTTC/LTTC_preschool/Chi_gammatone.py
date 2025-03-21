#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path

from eelbrain import *
import eelbrain
from trftools import gammatone_bank
import numpy as np
from trftools.neural import edge_detector

# Source Github repo: https://github.com/Eelbrain/Alice

if __name__ == "__main__":
    DATA_ROOT = Path("/Users/neuroling/Downloads")  #Path("~").expanduser() / 'Data' / 'Alice'
    STIMULUS_DIR = DATA_ROOT / "Chi_Demo"
    
    #print(STIMULUS_DIR)
    
    ## THE FIRST STEP ## #from Alice/predictors/make_gammatone.py
    # Make Gammatone from audio file
    for i in range(1):# , 13):
        audio_gammatone = STIMULUS_DIR / f'SillyBilly-gammatone.pickle' #存起來的gammatone檔名："SillyBilly"
        if audio_gammatone.exists():
            continue
        wav = load.wav(STIMULUS_DIR / f'傻比傻利_final_1.wav')  # 改檔名：『傻比傻利_final_1』= 讀進去的音檔
        gt = gammatone_bank(wav, 20, 5000, 256, location='left', pad=False, tstep=0.001)
        save.pickle(gt, audio_gammatone)
    
    
    ## THE SECOND STEP ##  # from Alice/predictors/make_gammatone_predictors.py
    # Make predictors from gammatone

    #DATA_ROOT = Path("~").expanduser() / 'Data' / 'Alice'
    #STIMULUS_DIR = DATA_ROOT / 'stimuli'
    PREDICTOR_DIR = STIMULUS_DIR / 'Chi_audio_predictors'  # This command could automatically create a new folder
    #print(PREDICTOR_DIR)

    PREDICTOR_DIR.mkdir(exist_ok=True)
    for i in range(1):  #, 13):
        gt = load.unpickle(STIMULUS_DIR / f'SillyBilly-gammatone.pickle') #存起來的gammatone檔名："SillyBilly"

        # Remove resampling artifacts
        gt = gt.clip(0, out=gt)
        # apply log transform
        gt = (gt + 1).log()
        # generate onset detector model
        gt_on = edge_detector(gt, c=30)

        # 1 band predictors
        save.pickle(gt.sum('frequency'), PREDICTOR_DIR / f'SillyBilly~gammatone-1.pickle') #存起來的gammatone檔名："SillyBilly"
        save.pickle(gt_on.sum('frequency'), PREDICTOR_DIR / f'SillyBilly~gammatone-on-1.pickle')#存起來的gammatone檔名："SillyBilly"

        # 8 band predictors
        x = gt.bin(nbins=8, func=np.sum, dim='frequency')
        save.pickle(x, PREDICTOR_DIR / f'SillyBilly~gammatone-8.pickle') #存起來的gammatone檔名："SillyBilly"
        x = gt_on.bin(nbins=8, func=np.sum, dim='frequency')
        save.pickle(x, PREDICTOR_DIR / f'SillyBilly~gammatone-on-8.pickle')# 存起來的gammatone檔名："SillyBilly"

    #"""