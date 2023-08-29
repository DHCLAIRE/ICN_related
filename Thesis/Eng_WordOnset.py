#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""This tutorial shows how to align transcript to speech with torchaudio, 
using CTC segmentation algorithm described in CTC-Segmentation of Large Corpora for German End-to-end Speech Recognition.
>> https://pytorch.org/audio/stable/tutorials/forced_alignment_tutorial.html
"""
import torch
import torchaudio


if __name__ == "__main__":
    print(torch.__version__)
    print(torchaudio.__version__)
    
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)