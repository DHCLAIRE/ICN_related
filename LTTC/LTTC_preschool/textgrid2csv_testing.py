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

#-------------------------------------------------
# Text file input / output

def inputtextlines(filename):
    handle = open(filename,'r')
    print(handle)
    linelist = handle.readlines()
    handle.close()
    return linelist

def outputtext(filename, text):
    handle = open(filename,'w')
    handle.write(text)
    handle.close()
    
    
if __name__ == "__main__":
    
    textgrid_path = "/Users/ting-hsin/Downloads/"
    
    textgridname = textgrid_path + "f051p003-10.TextGrid"
    textgrid = inputtextlines(textgridname)
    #pprint(textgrid)