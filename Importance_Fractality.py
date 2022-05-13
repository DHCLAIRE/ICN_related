#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
Citation: Najafi, E., & Darooneh, A. H. (2017). Long range dependence in texts: A method for quantifying coherence of text. Knowledge-Based Systems, 133, 33-42.
COPIED CONTENT FROM THE ARTICLE:

The fractal dimension of words in this one-dimensional space is a number between 0 and 1.
The important words have dimensions that are significantly different from one, while the less important words are distributed 
uniformly and their dimensions are close to one [6].
Box counting is a practical method for computing the fractal dimension of words.
To perform this calculation, the text should be divided into boxes of size s.
It means that any box contains s successive words.
The number of such boxes that contains at least one occurrence of a given word w,

i.e. the number of filled boxes, is Nb(w, s) and the self-similarity
property is expressed as,

Nb(w, s) ∼ s−Dw . (1)

where Dw stands for the fractal dimension of word w.
It is obtained by finding the slope of log-log plot of Nb(w, s) versus s for large enough s.

"""

'''
The importance of Fractality:
Calculation process:
Box counting: t

Box = the length of the text

s = the size of the boxes = s words that contains in this box
w = the target word  (??) I guess

'''
'''
Steps:
1. split the text into different lengths = create s??
2. shuffle the texts??
3. calculate the texts
'''

from pprint import pprint
import csv
import json



def LISTblankEraser(rawLIST):
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    #print(len(newrawLIST))
    return newrawLIST

def Mean(resultLIST, i, typeSTR = None):
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    #print("{} Raw data:".format(typeSTR), contentLIST)
    old_count = len(contentLIST)
    #print(old_count)

    for RT_Int in contentLIST:
        if 0. in contentLIST:
            contentLIST.remove(0.0)
        else:
            pass
    #print("{} Exclude 0.0 data:".format(typeSTR), contentLIST)
    new_count = len(contentLIST)
    #print(new_count)
    
    exclude_countINT = old_count - new_count
    PLDTmean_subFLOAT = round(np.mean(np.array(contentLIST)),3) #ouput: H pwRT Mean : 783.167
    MeanDICT = {"{} count".format(typeSTR):len(contentLIST),"{} Mean".format(typeSTR):PLDTmean_subFLOAT, "Exclude 0.0 count": exclude_countINT}
    
    return MeanDICT


def correctness(resultLIST, typeSTR = None):
    correctnessLIST = []
    count_True = 0 
    count_False = 0
    count_NA = 0
    
    for row in resultLIST:
        #rawLIST = ListDetector(row)
        if type(row) == list:
            rawLIST = row
        else:
            rawLIST = row.split(",")
            
        if rawLIST[6] == "['True']":
            count_True += 1
            correctBOOL = 1
        elif rawLIST[6] == "['False']":
            count_False += 1
            correctBOOL = 0
        else:
            count_NA += 1
            
    total_correctFLOAT = round(count_True/(count_True + count_False)*100,2)
    correctnessDICT = {"{} Correctness".format(typeSTR): total_correctFLOAT, "{} True:".format(typeSTR): count_True, "{} False:".format(typeSTR): count_False, "{} N/A:".format(typeSTR): count_NA}
    #correctnessLIST = [count_True, count_False, count_NA, total_correctFLOAT]
    
    return correctnessDICT  #correctnessLIST,   ###count_True, count_False, count_NA, total_correctFLOAT



if __name__ == "__main__":
    
    """
    
    % directly from the paper>>
    
    Box counting is a practical method for computing the fractal dimension of words. 
    To perform this calculation, the text should be divided into boxes of size s. 
    It means that any box contains s successive words. 
    The number of such boxes that contains at least one occurrence of a given word w
    , i.e. the number of filled boxes, is N b ( w, s ) and the self-similarity property 
    is expressed as, N b (w, s ) ∼s −D w . (1) where D w stands for the fractal dimension of word w.
    It is obtained by finding the slope of log-log plot of N b ( w, s ) versus s for large enough s .
    
    
    =======
    Number of shuffled box count(Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    N = the number of word in a text
    s = the box size = how many words were count as one box
    
    =====
    THE STEPS:
    *For the values that based on SHUFFLED position*
    1. Segment the words: Cut the word into different box sizes
    2. Count the filled boxes: Count how many times of the target word that appeared in the divided boxes
    3. GET THE VALUE OF THE COUNTS
    
    *For the values that based on SHUFFLED position*
    1. Shuffle the orginal text: Shuffled the text by the unit of word(Randomly distributed)
    2. Segment the words: Cut the word into different box sizes
    3. Count the filled boxes: Count how many times of the target word that appeared in the divided boxes
    
    
    Calculate the Fractality: 
    
    
    
    
    """
    
    """
    String preprocessing (Things that need to do first)
    1. converting all letters to lower or upper case
    2. converting numbers into words or removing numbers
    3. removing punctuations, accent marks and other diacritics
    4. removing white spaces
    5. expanding abbreviations
    6. removing stop words, sparse terms, and particular words
    7. text canonicalization
    """
    
    """
    What is the base of the calculation?? >> the whole chapter?  Or each sentence?? 
    """
    
    tmpLIST = []
    
    
    testing_text = """The marathon COVID-19 lockdown in Sydney, Australia, ended Monday for vaccinated residents. Stay-at-home orders imposed on June 26 have been lifted. Government advertisements have promised that freedoms would return when vaccination rates passed certain milestones. The message has been getting through to the community. Lockdown in the New South Wales state capital, Sydney, was lifted Monday because inoculation rates have passed 70% for people above aged 16. Shops have reopened for the first time since June. Small gatherings at home are permitted, and larger groups are allowed to meet at parks and beaches. However, the above apply only to fully vaccinated people. All residents still face restrictions on travel beyond Sydney. The rules will be eased when vaccination rates in New South Wales reach 80%. At that point international travel will resume. Still, New South Wales state premier Dominic Perrottet stated that a cautious stages approach to reopening is needed."""
    #print(type(testing_text))
    #print(testing_text)
    
    tmpLIST = testing_text.lower().split(" ")
    
    #pprint(tmpLIST)
    #print(len(tmpLIST))
    
    #for strROW in tmpLIST:
        #print(strROW)
        #print(type(strROW))
        
    result_data_path = "/Users/ting-hsin/Downloads/"
    
    
    resultLIST = []
    tmpLIST = []

    #剩把pseudoDICT的值叫出來
    pseudoLIST = []
    targetPseudoLIST = []
    High_CDpwLIST = []
    Low_CDpwLIST = []

    with open (result_data_path + "003_pseudowordsDICT.json", "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
    
        #print(sub_num)
    
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
    
        print(sub_num, "Target pw : ", targetPseudoLIST)
        print(sub_num, "High-CD pw : ", High_CDpwLIST)
        print(sub_num, "Low-CD pw : ", Low_CDpwLIST) # output: 003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']    
    
    
    with open (result_data_path + "003_Reading_task.csv", "r", encoding= 'unicode_escape') as csvfile_reading:  #, "r", encoding = "utf-8")
        readingLIST = csvfile_reading.read().split("\n")
        #pprint(readingLIST)
        #print(type(readingLIST))
        #print(len(readingLIST))
        readingLIST.pop(0)   # exclude the headers
        #print(len(readingLIST))
        
        # exclude the blank row
        readingLIST = LISTblankEraser(readingLIST)
        #print(len(readingLIST))
        #print(readingLIST[0])
        count = 0
        cleaned_LIST = []
        textLIST = []
        
        for row in readingLIST:
            #print(row)
            if ',"[""' in row:
                rawLIST = row.split(',"[""')
            elif ',"[\'' in row:
                rawLIST = row.split(',"[\'')
            else:
                print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
                print("Wrong_count >>>>>", len(rawLIST))
                
            if len(rawLIST) ==2:
                count +=1
            else:
                print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
                print("Wrong_count >>>>>", len(rawLIST))
            cleaned_LIST.append(rawLIST)

        print(count)
        pprint(cleaned_LIST)
        print(len(cleaned_LIST))
        
        for row in cleaned_LIST:
            textLIST = row[1].lower().split(" ")
            print(textLIST)
            print(len(textLIST))
            for word in textLIST:
                print(word)
                
        #print(len(readingLIST[0]))