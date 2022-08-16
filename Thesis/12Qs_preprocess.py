#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import re


if __name__ == "__main__":
    data_path = "/Users/neuroling/Downloads/新碩論主題/Ding-Thesis_ExpMaterials/"
    txtFile = data_path + '(MRI)code_comprehension_questions.txt'
    text = open(txtFile, 'r')
    #print(text.read())
    print(type(text))
    
    textLIST = [] 
    
    for row in text:
        print(row)
        print(type(row))
        print(len(row))
        re.sub("\t", " ")#.replace("\n", "")
        if len(row) > 1:
             
            textLIST.append(row)
        else:
            pass
    print(textLIST)
    
    
    #.close()
