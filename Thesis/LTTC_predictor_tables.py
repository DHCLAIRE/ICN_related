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
#from nltk import sent_tokenize
#from nltk import tokenize

"""
## Predictor ItemS
Word: the current word
Segment: per tape
Onset: word onset
Offset: word offset
Order: word order
LogFreq: the Log frequency of the current word
LogFreq_Prev: the Log frequency of the previous word, hence the first word is always 0
LogFreq_Next: the Log frequency of the next word
SndPower: word SndPower
Length: Offset minus Onset
Position: word position per sentence
Sentence:sentence position per text
IsLexical: 1=Content word; 0=Function word
NGRAM: the POS surprisal calculated from Tri-Gram model
CFG: the POS surprisal calculated from CFG model
Fractality: the POS surprisal calculated from Fractality model
"""

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
    LTTCroot_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG")
    Thesisroot_data_path = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")
    
    # The predictor items
    Word_LIST = []
    SegmentLIST = []
    OnsetLIST = []
    OffsetLIST = []
    OrderLIST = []
    LogFreqLIST = []
    LogFreq_PrevLIST = []
    LogFreq_NextLIST = []
    SndPowerLIST = []
    LengthLIST = []
    PositionLIST = []
    SentenceLIST = []
    IsLexicalLIST = []
    NGRAM_LIST = []
    CFG_LIST = []
    Fractality_LIST = []
    
    
    for sub_id in range(1):
        sub_idINT = sub_id+1
        text_data_path = LTTCroot_data_path / ("LTTC_MEG_S%.3d" %sub_idINT)
        
        # Open the csv fule
        with open (text_data_path / Path("S%.3d_Reading_task.csv" %sub_idINT), "r", encoding = "utf-8") as csvfile:
            fileLIST = csvfile.read().split("\n")
            fileLIST = LISTblankEraser(fileLIST)
            fileLIST.pop(0)
            #print(len(fileLIST)) # length Should be 30 
            #print(fileLIST)
            
            # Call out every text per subject
            for row in fileLIST[:1]:
                #print(row)
                per_textLIST = row.split(',"[')
                pprint(per_textLIST)
                # Find the segment sequence
                segmentINT = fileLIST.index(row)+1
                print(segmentINT)
                print(len(per_textLIST))
                
                # Sentence Segmentation by nltk
                textSTR = per_textLIST[1]
                sentenceLIST = nltk.sent_tokenize(textSTR)
                pprint(sentenceLIST)
                print(len(sentenceLIST))
                
                # Tokenization by nltk
                AllwordLIST = []
                Allword_seqLIST = []
                for sentence in sentenceLIST:
                    # Use re to filter out the punctuations
                    sentence = re.sub(r'[^\w\s]', '', sentence) #a_string
                    # Tokenize the cleaned text into a LIST form
                    wordLIST = nltk.word_tokenize(sentence)
                    print(len(wordLIST))
                    AllwordLIST.append(wordLIST)
                    word_seqLIST = []
                    for word in wordLIST:
                        word_seqINT = wordLIST.index(word)
                        word_seqLIST.append(word_seqINT)
                    Allword_seqLIST.append(word_seqLIST)
                print(AllwordLIST)
                print(Allword_seqLIST)

                """
                
                # making the wanted info into the List form for future use
                sub_idLIST.append(sub_id)
                dateLIST.append(day)
                sub_condLIST.append(sub_cond)
                roundLIST.append(round_)
                stimLIST.append(stim_wordSTR)
                CD_condLIST.append(cdSTR)
                resultKeyLIST.append(keys)
                responseLIST.append(conditionLIST)
                LDT_rtLIST.append(time_duration)
                correctnessLIST.append(correctLIST)

    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Word':Word_LIST,
                           'Segment':SegmentLIST,
                           'Onset':OnsetLIST,
                           'Offset':OffsetLIST,
                           'Order':OrderLIST,
                           'LogFreq':LogFreqLIST,
                           'LogFreq_Prev':LogFreq_PrevLIST,
                           'LogFreq_Next':LogFreq_NextLIST,
                           'SndPower':SndPowerLIST,
                           'Position':PositionLIST,
                           'Sentence':SentenceLIST,
                           'IsLexical':IsLexicalLIST,
                           'NGRAM':NGRAM_LIST,
                           'CFG':CFG_LIST,
                           'Fractality':Fractality_LIST
                           })
                           
            #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
            file_name = 'S%.3d_TRF_predictor_tables.csv' %sub_idINT
            save_path = Thesisroot_data_path / Path(file_name)
            dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

"""