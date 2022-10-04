#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path

from eelbrain import *
from trftools import gammatone_bank
import numpy as np
from trftools.neural import edge_detector


if __name__ == "__main__":
    #DATA_ROOT = Path("~").expanduser() / 'Data' / 'Alice'
    #STIMULUS_DIR = DATA_ROOT / 'stimuli'
    
    # stim_data_path = "ALICE's audio file"
    
    # Make Gammatone from audio file
    for i in range(1, 13):
        dst = STIMULUS_DIR / f'{i}-gammatone.pickle'
        if dst.exists():
            continue
        wav = load.wav(STIMULUS_DIR / f'{i}.wav')
        gt = gammatone_bank(wav, 20, 5000, 256, location='left', pad=False, tstep=0.001)
        save.pickle(gt, dst)
    
    
    # Make predictors from gammatone
    """
    DATA_ROOT = Path("~").expanduser() / 'Data' / 'Alice'
    STIMULUS_DIR = DATA_ROOT / 'stimuli'
    PREDICTOR_DIR = DATA_ROOT / 'predictors'
    """
    PREDICTOR_DIR.mkdir(exist_ok=True)
    for i in range(1, 13):
        gt = load.unpickle(STIMULUS_DIR / f'{i}-gammatone.pickle')
    
        # Remove resampling artifacts
        gt = gt.clip(0, out=gt)
        # apply log transform
        gt = (gt + 1).log()
        # generate onset detector model
        gt_on = edge_detector(gt, c=30)
    
        # 1 band predictors
        save.pickle(gt.sum('frequency'), PREDICTOR_DIR / f'{i}~gammatone-1.pickle')
        save.pickle(gt_on.sum('frequency'), PREDICTOR_DIR / f'{i}~gammatone-on-1.pickle')
        # 8 band predictors
        x = gt.bin(nbins=8, func=np.sum, dim='frequency')
        save.pickle(x, PREDICTOR_DIR / f'{i}~gammatone-8.pickle')
        x = gt_on.bin(nbins=8, func=np.sum, dim='frequency')
        save.pickle(x, PREDICTOR_DIR / f'{i}~gammatone-on-8.pickle')    
    
    