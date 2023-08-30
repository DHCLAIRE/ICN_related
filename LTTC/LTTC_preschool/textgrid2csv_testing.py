#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""#!/usr/bin/python
# textgrid2csv.py
# D. Gibbon
# 2016-03-15
# 2016-03-15 (V02, includes filename in CSV records)
"""
#-------------------------------------------------
# Import modules

import sys, re

from pprint import pprint
import csv
import json
import random
from random import sample
import os
#from gtts import gTTS
import pandas as pd
import time
from pathlib import Path
#import nltk
#import re
#from nltk import sent_tokenize
#from nltk import tokenize
#-------------------------------------------------
# Text file input / output

def inputtextlines(filename):
    handle = open(filename,'r')
    print(handle)
    linelist = handle.readlines()
    handle.close()
    return linelist

def outputtext(filename, text):
    handle = open(filename,'w')  #, encoding="utf-8"
    handle.write(text)
    handle.close()

#-------------------------------------------------
# Conversion routines

def converttextgrid2csv(textgridlines,textgridname):

    csvtext = '# TextGrid to CSV (D. Gibbon, 2008-11-23)\n# Open the file with OpenOffice.org Calc or MS-Excel.\nFileName\tTierType\tTierName\tLabel\tStart\tEnd\tDuration\n'

    newtier = False
    for line in textgridlines[9:]:
        line = re.sub('\n','',line)
        line = re.sub('^ *','',line)
        linepair = line.split(' = ')
        if len(linepair) == 2:
            if linepair[0] == 'class':
                classname = linepair[1]
            if linepair[0] == 'name':
                tiername = linepair[1]
            if linepair[0] == 'xmin':
                xmin = linepair[1]
            if linepair[0] == 'xmax':
                xmax = linepair[1]
            if linepair[0] == 'text':
                text = linepair[1]
                diff = str(float(xmax)-float(xmin))
                csvtext += textgridname + '\t' + classname + '\t' + tiername + '\t' + text + '\t' + xmin + '\t' + xmax + '\t' + diff + '\n'
    return csvtext

#-------------------------------------------------
# Main caller
"""
def main():

    if len(sys.argv) < 2:
        print("Usage: textgrid2csv.py <textgridfilename>")
        exit()
    textgridname = sys.argv[1]
    csvname = textgridname + '.csv'

    textgrid = inputtextlines(textgridname)

    textcsv = converttextgrid2csv(textgrid,textgridname)

    outputtext(csvname,textcsv)

    print("Output file: " + csvname)

    return
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
    
    textgrid_path = "/Users/ting-hsin/Downloads/Sound/"
    
    textgridname = textgrid_path + "story1.TextGrid"
    csvname = textgridname + '.csv'

    textgrid = inputtextlines(textgridname)

    textcsv = converttextgrid2csv(textgrid,textgridname)

    outputtext(csvname,textcsv)

    print("Output file: " + csvname)
    
    
    # The predictor items
    Word_LIST = []     #  = textgrid.csv_word
    SegmentLIST = []   #  = the sequence of the story
    OnsetLIST = []     #  = textgrid.csv_start
    OffsetLIST = []    #  = textgrid.csv_end
    OrderLIST = []     #  = count by the index of the word
    #LogFreqLIST = []
    #LogFreq_PrevLIST = []
    #LogFreq_NextLIST = []
    #SndPowerLIST = []
    LengthLIST = []    #  = textgrid.csv_duration
    PositionLIST = []  #  = count from the raw txt file (office word file)
    SentenceLIST = []  #  = count from the raw txt file (office word file)
    IsLexicalLIST = [] #  = textgrid.csv_POS (or universal pos)
    #NGRAM_LIST = []
    #CFG_LIST = []
    #Fractality_LIST = []
    
    # Open the csv fule
    with open (csvname, "r", encoding = "utf-8") as csvfile:
        fileLIST = csvfile.read().split("\n")
        fileLIST = LISTblankEraser(fileLIST)
        #fileLIST.pop(0)
        print(len(fileLIST)) # length Should be 30 
        pprint(fileLIST)    