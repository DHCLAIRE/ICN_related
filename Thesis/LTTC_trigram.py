#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json
import random
from random import sample
import os
from gtts import gTTS
import pandas as pd
import time
from pathlib import Path
import nltk
import re
from nltk import sent_tokenize
from nltk import tokenize

# Using Reuters as the corpus to train a trigram model
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict


def LISTblankEraser(rawLIST):
    '''
    Remove the blank that inside the list
    '''
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    #print(len(newrawLIST))
    return newrawLIST

if __name__ == "__main__":

    
    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))
    
    # Count frequency of co-occurance  
    for sentence in reuters.sents():
        for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1
    
    # Let's transform the counts to probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count    