#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pprint import pprint
#from CwnGraph import CwnBase
from CwnGraph import CwnImage  # pip3 install CwnGraph >> then you could start using it

if __name__ == "__main__":
    # Import the latest corpus
    cwn = CwnImage.latest()
    
    lemmasList = []
    sensesLIST = []
    rawLIST = []
    
    #"""
    #TESTING SECTION#
    """
    # Find out the target word
    lemmasList = cwn.find_lemma("")
    print(lemmasList)
    pprint(len(lemmasList))
    pprint(type(lemmasList))
    
    
    # Get the info of the target word
    sensesLIST = lemmasList[0].senses
    pprint(sensesLIST)
    print(type(sensesLIST))
    print(len(sensesLIST))
    
    # Get the relations of the target word?
    
    computer = sensesLIST[0]
    pprint(computer.relations)
    print(type(computer.relations))
    print(len(computer.relations))
    """
    # Setting up the data_path
    data_path = "/Users/neuroling/Downloads/ICN_ExpMaterials/"
    
     
    # Load in the data
    with open(data_path + "雙字詞_3-2聲Noun.csv","r", encoding = "utf-8") as csvfile:  #2-3/3-3/3-1 沒啥東西
        rawLIST = csvfile.read().split("\n")
        print(len(rawLIST))  # 34692 in total >> should minus one for the headline
        #print(tmpLIST)
        
        for row in rawLIST:
            testLIST = row.split(",")
            print(testLIST[:2])
            
            # combine the 2 characters together into one string
            input2wordSTR = ''.join(testLIST[:2])
            print(input2wordSTR)
                
            # for the users to moniter the prograss >> command written by Peter wolf of Droidtown's CEO
            print("{}%".format(round(rawLIST.index(row)/len(rawLIST), 3)*100))   #, w[0])
            
            lemmasList = cwn.find_lemma(input2wordSTR)
            print(lemmasList)