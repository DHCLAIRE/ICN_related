#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
import time
#from datetime import datetime,date
import pandas as pd

if __name__ == "__main__":
    
    # Setting up the data_path
    data_path = "/Users/neuroling/Downloads/ICN_ExpMaterials/"
    
    # for collecting the Tone combination set of words
    rawLIST = []
    testLIST = []
    resultLIST = []
    Tone_2_3LIST  = []
    Tone_3_3LIST  = []
    Tone_3_2LIST  = []
    Tone_3_1LIST  = []
    
    # for articut parser
    input2wordLIST = []
    resultDICT_lv1 = {}
    resultDICT_lv2 = {}
    pos2wordLIST = []
    totalposLIST = []
    rawLIST_2 = []
    word_posLIST = []
    CKIPposLIST = []
    CKIPwLIST = []
    ArticutposLIST = []
    wantedCKIPposLIST = []
    
    
    with open(data_path + "雙字詞_23-33-3231.csv","r", encoding = "utf-8") as csvfile:
        rawLIST = csvfile.read().split("\n")
        print(len(rawLIST))  # 34692 in total >> should minus one for the headline
        #print(tmpLIST)
        
        for row in rawLIST :
            testLIST = row.split(",")
            #print(testLIST[:4])
            
            # 23聲雙字詞
            if "2" in testLIST[2] and "3" in testLIST[3]:
                #print("這有2-3聲雙字詞 : ", testLIST[:4])
                Tone_2_3LIST.append(testLIST)
            
            # 33聲雙字詞
            if "3" in testLIST[2] and "3" in testLIST[3]:
                #print("這有3-3聲雙字詞 : ", testLIST[:4])
                Tone_3_3LIST.append(testLIST)
                
            # 32聲雙字詞
            if "3" in testLIST[2] and "2" in testLIST[3]:
                #print("這有3-2聲雙字詞 : ", testLIST[:4])
                Tone_3_2LIST.append(testLIST)
            
            # 31聲雙字詞
            if "3" in testLIST[2] and "1" in testLIST[3]:
                #print("這有3-1聲雙字詞 : ", testLIST[:4])
                Tone_3_1LIST.append(testLIST)
                
            else:
                pass
        
        # present part
        #pprint(Tone_2_3LIST)
        print("2-3聲雙字詞LIST長度 : ", len(Tone_2_3LIST))   # 1395 組
        #pprint(Tone_3_3LIST)
        print("3-3聲雙字詞LIST長度 : ", len(Tone_3_3LIST))   # 1132 組
        #pprint(Tone_3_2LIST)
        print("3-2聲雙字詞LIST長度 : ", len(Tone_3_2LIST))   # 1484 組
        #pprint(Tone_3_1LIST)
        print("3-1聲雙字詞LIST長度 : ", len(Tone_3_1LIST))   # 1096 組
        
        
        """
        # write all the list into the csv file
        headerLIST =["first_char", "sec_char", "P1","P2","P1,3->2","first_code", "sec_code", "first_freq", "first_frating", "first_stroke", "sec_freq", "sec_frating", "sec_stroke"
                     ,"word_freq", "NB", "NB1", "NB2", "rel_HF", "rel_HF_nb1", "rel_HF_nb2", "rel_HF%", "rel_HF%_nb1", "rel_HF%_nb2", "first_mno.(rating)", "sec_mno.(rating)"]
                     
        with open(data_path + '雙字詞_3-1聲.csv', 'w', encoding = "utf-8-sig") as f:   #encoding = "utf-8-sig" >> if 中文字用"utf-8" encode會有亂碼，就用"utf-8-sig", 應該就會沒事了
            # using csv.writer method from CSV package
            write = csv.writer(f)
      
            write.writerow(headerLIST)   #(fields)
            write.writerows(Tone_3_1LIST)  #(rows)
            """
        
        # load in the Articut package
        with open("account.info") as accountFILE:   # meanging to load the account info file, the you won't risk the chance of exposing your APIkey
            accountDICT = json.loads(accountFILE.read())   # which also means that you have to put the account info file together with every script that  have this line.
        
            username = accountDICT["username"] #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
            apikey   = accountDICT["apikey"]   #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
            articut = Articut(username, apikey)
        
        
        # load in the CKIP's POS and also the Articut POS
        with open(data_path + "out2.csv","r", encoding = "utf-8") as csvfile_2:
            rawLIST_2 = csvfile_2.read().split("\n")

        for word_posSTR in rawLIST_2:
            word_posLIST = word_posSTR.split(",")
            #pprint(word_posLIST)
            CKIPposLIST.append(word_posLIST)
        #pprint(CKIPposLIST)
        #print(CKIPposLIST[0][0])
        
        
        # combine the 2 characters together into one string to do Articut Pasrer
        for w in Tone_3_2LIST:
            # combining the seperate characters into an item
            input2wordLIST = w[:2]
            input2wordSTR = ''.join(input2wordLIST)
            #print(input2wordSTR)
            
            # for the users to moniter the prograss >> command written by Peter wolf of Droidtown's CEO
            print("{}%".format(round(Tone_3_2LIST.index(w)/len(Tone_3_2LIST), 4)*100))   #, w[0])
            
            # Use Articut Parser to get the pos of the target word
            inputSTR = input2wordSTR
            #resultDICT_lv1 = articut.parse(inputSTR, level = "lv1")   #msg': 'Each account can only issue 80 requests per minute'
            resultDICT_lv2 = articut.parse(inputSTR, level = "lv2")
            time.sleep(1.4)
            
            '''
             # Notes for how manu time sleep you need for having another round of Articut Parser
             # let the machine(ArticutAPI) rest for 2.6 sec 
             # >> came from command line 81 >>>how to calculate 2.6 sec ? 
             # >> 80 requests per minutes >> 80/60 = 1.34  >> but we need to requests for 2 level at the same time
             # hence >> (80*2)/60 = 2.67 >>resulted in resting for 2.6 sec
            '''
            #print(resultDICT_lv2["result_obj"][0][0]["pos"])   # this is how us get the pos information from the resultDICT of Articut Parser
            #print(type(resultDICT_lv2["result_obj"][0][0]["pos"]))
            
            # setting the wanted form of string and its pos that tag by Articut Parser
            pos2wordLIST = [input2wordSTR, resultDICT_lv2["result_obj"][0][0]["pos"]]
            #print(pos2wordLIST)
            ArticutposLIST.append(pos2wordLIST)
        
            
            # Matching the out2.txt, which is the CKIP pos info, which the Tone word set to get more pos, and then save all kinds of different POS at one time
            for CKIPwLIST in CKIPposLIST:
                # excluding the one that pos == "#--"
                if input2wordSTR == CKIPwLIST[0] and "#--" != CKIPwLIST[1]:
                    #print("It's a Match!", input2wordSTR)
                    wantedCKIPposLIST.append(CKIPwLIST)
                else:
                    pass
        #pprint(wantedCKIPposLIST)
        #print(type(wantedCKIPposLIST))
        #pprint(ArticutposLIST)
        #print(type(ArticutposLIST))
        
        """
        # save all the list into the csv file
        ArticutheaderLIST = ["word", "Articutpos"]
        CKIPheaderLIST = ["word", "CKIPpos", "text_num"]
                     
        with open(data_path + 'ArticutPOS_3-2聲.csv', 'w', encoding = "utf-8-sig") as f_2:   #encoding = "utf-8-sig" >> if 中文字用"utf-8" encode會有亂碼，就用"utf-8-sig", 應該就會沒事了
            # using csv.writer method from CSV package
            write = csv.writer(f_2)
      
            write.writerow(ArticutheaderLIST)   #(fields)
            write.writerows(ArticutposLIST)  #(rows)
        
        with open(data_path + 'CKIPpos_3-2聲.csv', 'w', encoding = "utf-8-sig") as f_3:   #encoding = "utf-8-sig" >> if 中文字用"utf-8" encode會有亂碼，就用"utf-8-sig", 應該就會沒事了
            # using csv.writer method from CSV package
            write = csv.writer(f_3)
            
            write.writerow(CKIPheaderLIST)   #(fields)
            write.writerows(wantedCKIPposLIST)  #(rows)
"""