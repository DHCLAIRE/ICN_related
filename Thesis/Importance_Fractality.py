#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pprint import pprint
import re
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
from collections import Counter
import string   # import string library function
#from string import maketrans # for text preprocessing


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

def word_frequncy(text):
    '''
    Count the word appearance based on its text content
    '''
    count_wordDICT = dict()
    text_wordLIST = text.lower().split()
    
    for wordSTR in text_wordLIST:
        if wordSTR in count_wordDICT:
            count_wordDICT[wordSTR] += 1
        else:
            count_wordDICT[wordSTR] = 1
    return count_wordDICT


def shuffle_text(targetLIST):
    '''
    shuffle the test multiple times based on how long the text is 
    '''
    shuffle_textLIST = targetLIST.copy()
    for i in range(len(shuffle_textLIST)):
        random.shuffle(shuffle_textLIST)
    return shuffle_textLIST

def box2count(target_boxedLIST):
    '''
    count the target word appearance in the boxed text
    '''
    word_boxDICT = {}
    
    # Count the appearance of the target word in the box_wordLIST after the disecction was done
    # According to the sequence of the splited raw text = every segmented word in the text
    for wordSTR in raw_textLIST:
        #print(wordSTR)
        
        # Access every elements inside the stored All_boxed_textLIST & All_shuffled_boxed_textLIST, which are the boxed results of every box size
        for boxedLIST in target_boxedLIST: #All_boxed_textLIST:
            #print(wordSTR)
            #print(boxedLIST)
            #print(type(boxedLIST))
            t_wordcountINT = 0
            
            # Access the elements of boxed list based on the box size
            for small_box_wordLIST in boxedLIST:
                #print("small_box_wordLIST = ", small_box_wordLIST)  # The model only catchs the last small_box_wordLIST, there for the word count might be wrong
                
                # Count the existence of the target word
                if wordSTR in small_box_wordLIST:
                    t_wordcountINT +=1
                    #print(wordSTR)
            #print("The word count of", "[", wordSTR, "]", "in box size = ", "[", len(boxedLIST[0]), "]", "is", t_wordcountINT)
            #print(type(t_wordcountINT))
            # The count in this section would need to be DICTed by the box size
            #word_boxDICT = {"marathon":{{"Box_size_1": 7},
                                      #  {"Box_size_2": 7},.....},
                        #    "the":{{"Box_size_1": 7},
                        #           {"Box_size_2": 7},...}, 
                        #    .....}
            
            #box_countDICT = {"Box_size_%d" %len(boxedLIST[0]):t_wordcountINT}
            #print(box_countDICT)
            
            # Store everything into a DICT
            # The old version
            word_boxDICT["%s_%d" %(wordSTR, len(boxedLIST[0]))] = {"Box_size_%d" %len(boxedLIST[0]):t_wordcountINT}
            #word_boxDICT = {"%s_%d" %(wordSTR, len(boxedLIST[0])): t_wordcountINT}
            
    #print(word_boxDICT)
    #print(len(word_boxDICT))
    return word_boxDICT


if __name__ == "__main__":
    
    """
    Citation: Najafi, E., & Darooneh, A. H. (2017). Long range dependence in texts: A method for quantifying coherence of text. Knowledge-Based Systems, 133, 33-42.
    COPIED CONTENT FROM THE ARTICLE:
    
    ========Formula__1 <--> Section__1========
    The fractal dimension of words in this one-dimensional space is a number between 0 and 1.
    The important words have dimensions that are significantly different from one, while the less important words are distributed 
    uniformly and their dimensions are close to one [6].
    Box counting is a practical method for computing the fractal dimension of words.
    To perform this calculation, the text should be divided into boxes of size s.
    It means that any box contains s successive words.
    The number of such boxes that contains at least one occurrence of a given word w,
    
    i.e. the number of filled boxes, is Nb(w, s) and the self-similarity property is expressed as,
    
    Nb(w, s) ∼ s−Dw . (1)
    
    where Dw stands for the fractal dimension of word w.
    It is obtained by finding the slope of log-log plot of Nb(w, s) versus s for large enough s.
    
    =======
    # NOTES_Section__1
    =======
    Number of shuffled box count (Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    N = the number of word in a text
    s = the box size = how many words were count as one box
    
    ========Formula__2 <--> Section__2========
    The shuffling process cannot change the pattern of the words that are uniformly distributed throughout the text
    , although meaning of the text gets lost.
    Therefore, such words have less importance in the semantic structure of the text.
    The distributions of the more important words change remarkably in the shuffled text.
    Accordingly, for an important word, the number of filled boxes in an original text differs from the case of the shuffled text.
    Difference between the number of filled boxes for a given word in the orig- inal and shuffled text could be considered as
    a measure of word importance [6] .
    To measure these differences the degree of fractal- ity is defined as:
    
    d f (w ) =   s log ( N sh. b (w, s ) N b (w, s ) ) (2)
    >>> df(w) = the degree of fractality of a target word = sum(log(Nsh(w,s)/Nb(w,s)))
    
    where d f ( w ) is the degree of fractality (or simply fractality) and N sh. b (w, s ) is the number of filled boxes with size s for the particular word w , in the shuffled text.
    To take into account the frequency of each word in a text, the fractality could be multiplied by log ( M ), where M is word frequency, as is explained in the reference [6] .
    
    =======
    # NOTES_Section__2
    =======
    
    
    
    ========Formula__3 <--> Section__3========
    To calculate the number of filled boxes in a shuffled text, we have to perform one shuffling process for each particular word.
    It means that we need to perform a large number of shuffling processes (equal to the number of word-types in a text) 
    to rank the words due to their importance.
    To overcome this difficulty we use our conjecture about the number of filled boxes in a shuffled text [6] :
    
    N sh. b (s, ω) = M 1 + ( M−1 N−1 )(s −1)
    >>> Number of shuffled box count (Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    
    where M is frequency of the word ω. This equation shows good conformity with the number of filled boxes in a shuffled text [6] .
    Higher value of degree of fractality means that the distribution pattern of the word is more different from the uniform distribution
    ; So the word is more important.
    
    =======
    # NOTES_Section__3
    =======
    Number of shuffled box count (Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    N = the number of word in a text = Shuffle counts  >>  = the length of the text >> DONE
    M = the word frequency >> count the appearance of the target word in the text  >> UNDONE
    s = the box size = how many words were count as one box >> from 1 to the maximum length of the text  >> DONE
    w = the target word  >> DONE
    
    
    ================================================================================================================
    ================================================================================================================
    Formulas
    
    1. Nb(w, s) ∼ s−Dw . (1)
    2. d f (w ) =   s log ( N sh. b (w, s ) N b (w, s ) ) (2)
       >>> df(w) = the degree of fractality of a target word = sum(log(Nsh(w,s)/Nb(w,s)))
    3. N sh. b (s, ω) = M 1 + ( M−1 N−1 )(s −1)
       >>> Number of shuffled box count (Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    
    We've got 3 formula
    1. Unshuffled box count >> Vary in box sizes
    2. Shuffled box count >> Vary in box sizes and (shuffling count??)
    3. Fractality: sum of [log(Shuffled box count/Unshuffled box count)>> vary in box sizes]
    
    ================================================================================================================
    ================================================================================================================
    
    
    #=====
    THE STEPS:
    *For the values that based on *UNSHUFFLED* position*
    1. Segment the words: Cut the word into different box sizes
    2. Count the filled boxes: Count how many times of the target word that appeared in the divided boxes
    3. GET THE VALUE OF THE COUNTS
    4. Do it all over again and again(what is the scale of the box sizes???)  

    
    *For the values that based on SHUFFLED position*
    1. Shuffle the orginal text: Shuffled the text by the unit of word(Randomly distributed)
    2. Segment the words: Cut the word into different box sizes
    3. Count the filled boxes: Count how many times of the target word that appeared in the divided boxes
    
    
    ======Questions======
    Q1: What is the base of the calculation?? >> the whole chapter?  Or each sentence??  >> I think is the whole text(would the length affect the importance value??)
    Q2: How to construct the command of spliting in different nox sizes???
    
    
    '''
    # There's no need to add this first, cause we all ready got the file in word unit

    String preprocessing (Things that need to do first)
    1. converting all letters to lower or upper case
    2. converting numbers into words or removing numbers
    3. removing punctuations, accent marks and other diacritics
    4. removing white spaces
    5. expanding abbreviations
    6. removing stop words, sparse terms, and particular words
    7. text canonicalization
    '''
    
    ======
    Method
    ======
    1. calculate the importance values for all word types in our sample texts
       >> : To calculate the fractality values, text should be divided into 
            non-overlapping boxes of size s and the number of filled boxes ( N b ) should be counted.
    2. constructing the important time series
       >> : an array which is directed from beginning word of text to the last one is considered.
            The importance time series of the text is simply constructed by replacing each word with its importance value. 
            and then normalizated the 
    
    
    
    """
    
    raw_textLIST = []
    
    
    testing_text = """The marathon COVID-19 lockdown in Sydney, Australia, ended Monday for vaccinated residents. Stay-at-home orders imposed on June 26 have been lifted. Government advertisements have promised that freedoms would return when vaccination rates passed certain milestones. The message has been getting through to the community. Lockdown in the New South Wales state capital, Sydney, was lifted Monday because inoculation rates have passed 70% for people above aged 16. Shops have reopened for the first time since June. Small gatherings at home are permitted, and larger groups are allowed to meet at parks and beaches. However, the above apply only to fully vaccinated people. All residents still face restrictions on travel beyond Sydney. The rules will be eased when vaccination rates in New South Wales reach 80%. At that point international travel will resume. Still, New South Wales state premier Dominic Perrottet stated that a cautious stages approach to reopening is needed."""
    #print(type(testing_text))
    #print(testing_text)
    
    # Using re to remove the punctuations
    #a_string = '!hi. wh?at is the weat[h]er lik?e.'
    cleaned_text = re.sub(r'[^\w\s]', '', testing_text) #a_string
    #print(cleaned_text)
    
    # segment the text word by word
    raw_textLIST = cleaned_text.lower().split()
    print(raw_textLIST)
    #print(len(raw_textLIST))  # = 150
    """
    ### APPLY LATER ###
    # set the value of N (N = "The length of the text")
    N = float(len(raw_textLIST))
    print("N (The length of the text) = ", N)
    #print(type(N))
    #pprint(raw_textLIST)
    print(len(raw_textLIST))
    
    ##NOT THIS WAY## # word frequency count  # M >> needs to call out the word(key) for its count(value)
    # method 1
    word_frequncyDICT = word_frequncy(testing_text)
    print("Func:", word_frequncyDICT) # Follow the word sequence of text
    print(len(word_frequncyDICT))
    
    # method 2
    word_frequncyDICT_2 = Counter(raw_textLIST)
    print("Counter:", word_frequncyDICT_2) # Listed in the rank of frequency
    print(len(word_frequncyDICT_2))
    
    """
    
    ## THIS IS BOX COUNTING ##
    #Number of the box count >> M >> I guess??
    #make a box size list for segment the text according to the box size
    lengthLIST = list(range(1,len(raw_textLIST)+1))
    #print(lengthLIST) # How many word in one box size
    
    shuffled_textLIST = []
    shuffled_textLIST = shuffle_text(raw_textLIST)
    #print("RAW text:", raw_textLIST)  # Checked
    #print("SHUFFLED text:", shuffled_textLIST)  # Checked
    
    #(SOLVED!) what if I store the boxes into a DICT, and index those boxes by it's length?? (NO, by the time)
    All_boxed_textLIST = []  # All the results of every boxed textLIST
    All_shuffled_boxed_textLIST = []  #All the results of every boxed textLIST from shuffled text
    
    #divide the text by the box size
    for s in lengthLIST:  # s = box isze
        # Unshuffled text
        boxed_textLIST = []  # the boxed result of the box size  i.e. the boxed result of s = 1
        box_wordLIST = [] # the boxed word  i.e.['rates']; ['passed', '70%']
        # Shuffled text
        shuffled_boxed_textLIST = [] # boxed result of the box size from shuffled text  i.e. the boxed result of s = 1
        shuffled_box_wordLIST = []  # the boxed word in shuffled text i.e.['rates']; ['passed', 'aged']
        
        
        # Unshuffled Box Disecction
        for c in range(len(raw_textLIST)):  # c = word count
            # only starting to box the word based on the box size (meaning the residue of that word index is equal to zero)
            if c%s == 0: # s == box size
                box_wordLIST = raw_textLIST[c:c+s]  # [w:w+s] => if w = 2; s = 2 , [w:w+s] = [2:4] = collect word from index 2-3 => [index2 , index3]
                #print(box_wordLIST)
                #print(len(box_wordLIST))
                boxed_textLIST.append(box_wordLIST)
            else:
                pass
        #print(boxed_textLIST)
        # Save all the boxed result into a big LIST
        All_boxed_textLIST.append(boxed_textLIST)
        
        # Shuffled Box Disecction
        # Using the shuffled textx
        for shuffled_c in range(len(shuffled_textLIST)):  #shuffled_c = word count in shuffled text
            # only starting to box the word based on the box size (meaning the residue of that word index is equal to zero)
            if shuffled_c%s == 0: # s == box size
                shuffled_box_wordLIST = shuffled_textLIST[shuffled_c:shuffled_c+s]  # [w:w+s] => if w = 2; s = 2 , [w:w+s] = [2:4] = collect word from index 2-3 => [index2 , index3]
                #print(shuffled_box_wordLIST)
                #print(len(shuffled_box_wordLIST))
                shuffled_boxed_textLIST.append(shuffled_box_wordLIST)
            else:
                pass
        #print(shuffled_boxed_textLIST)
        # Save all the boxed result into a big LIST
        All_shuffled_boxed_textLIST.append(shuffled_boxed_textLIST)
        
        #print(boxed_textLIST)
        #print(len(boxed_textLIST))  #Do I need to store every box_wordLIST into one big DICT??
        #print(shuffled_boxed_textLIST)
        #print(len(shuffled_boxed_textLIST))
    #print("Box dissecction DONE")
    #print("Shuffled Box dissecction DONE")
    
    ## Check for the box result of the unshuffled and shuffled types ##
    ## The unshuffled type ##
    #pprint(All_boxed_textLIST)
    #print(All_boxed_textLIST[2]) # should be the result of s=3  >> correct
    #print(len(All_boxed_textLIST[2])) # = 50 >> correct
    #print(All_boxed_textLIST[2][1]) # should be the second segment of the s=3 result >> = ['lockdown', 'in', 'sydney,'] =correct
    #print(len(All_boxed_textLIST[2][1])) # = 3 >> correct
    #print(All_boxed_textLIST[2][1][1]) # should be the second single word(STR) in the second segment of the s=3 result
    #print(len(All_boxed_textLIST[2][1][1])) # = the length of the certain target word(STR)

    ## The shuffled type ##
    #print(All_shuffled_boxed_textLIST)
    #print(All_shuffled_boxed_textLIST[2]) # >>correct
    #print(len(All_shuffled_boxed_textLIST[2]))  # >>correct
    #print(All_shuffled_boxed_textLIST[2][1])  # >>correct
    #print(len(All_shuffled_boxed_textLIST[2][1]))  # >>correct
    #print(All_shuffled_boxed_textLIST[2][1][1])  # >>correct
    #print(len(All_shuffled_boxed_textLIST[2][1][1]))  # >>correct
    
    
    # Calculate the box count
    # Original texts
    
    """
    # Peel the first layer of the LIST
    for ori_itemLIST in All_boxed_textLIST[0:5]:  # the first five box size collections
        print("ori_itemLIST", ori_itemLIST)
        box_size_allsegINDEX = All_boxed_textLIST.index(ori_itemLIST)
        box_countINT = 0
        
        for ori_seg_boxLIST in ori_itemLIST[0:5]:
            print("ori_seg_boxLIST", ori_seg_boxLIST)
            box_countINT += 1
            sizeINDEX = ori_itemLIST.index(ori_seg_boxLIST)

            for wordSTR in ori_seg_boxLIST[0:5]:
                wordINDEX = ori_seg_boxLIST.index(wordSTR)
                target_wcountINT = 0
                
                for target_wSTR in raw_textLIST[0:5]:  # the first five words
                    if target_wSTR == All_boxed_textLIST[box_size_allsegINDEX][sizeINDEX][wordINDEX]:   #if target_wSTR == wordSTR:
                        print("testing wordSTR<", wordSTR, ">; target word<", All_boxed_textLIST[box_size_allsegINDEX][sizeINDEX][wordINDEX], ">")
                        target_wcountINT +=1
                    else:
                        pass #print("ERROR: N/A")
                    print(target_wSTR, "'s box count:", target_wcountINT)
                    print("  ")
    print("  ")
    print("  ")
    print("### ROUND:", box_countINT)
    
    """
    
    #count_word = 0
    ## METHOD TWO FOR COUNTING APPEARENCE ##
    box_countDICT = {}
    ## Call out every words in the raw text to further counting its appearance
    for targ_word in raw_textLIST[0:3]:
        print("CHECKING:", targ_word)
        count_word = 0
        ## Open the outer layer of boxed LIST, which are the big LIST containing every boxed text set(all box sizes included)  # [[[the], [B], [C]], [the, B], [C, D]]
        for tmp_itemLIST in All_boxed_textLIST[0:3]:
            print(All_boxed_textLIST.index(tmp_itemLIST), tmp_itemLIST)
            
            ## Open the middle layer of the boxed LIST, which are the boxes text in different size  # [[the], [B], [C]] or [[the, B], [C, D]]
            for tmp_boxLIST in tmp_itemLIST:
                print(tmp_itemLIST.index(tmp_boxLIST), tmp_boxLIST)
                
                ## Open the inner layer, which are the wordSTR within each box based on the box size  # [the], [B], [C] or [the, B], [C, D]
                for tmp_wordSTR in tmp_boxLIST:
                    print(tmp_boxLIST.index(tmp_wordSTR), tmp_wordSTR)
                    #print()
                    if re.match(tmp_wordSTR, targ_word):
                        print("YES >>", tmp_wordSTR)
                        count_word += 1
                    else:
                        print("NOPE", tmp_wordSTR)
                    print(targ_word, "==", count_word)
                    print()
                    print()
                    
    
    
    ### DOWN below is the saving part, we'll deal with it later ###
    """
    # Save the boxes list word count into DICT
    boxedDICT = box2count(All_boxed_textLIST)
    shuffle_boxedDICT = box2count(All_shuffled_boxed_textLIST)
    pprint(shuffle_boxedDICT)
    #pprint(boxedDICT)
    
    
    
    dataDICT_1 = pd.DataFrame(boxedDICT)
    dataDICT_2 = pd.DataFrame(shuffle_boxedDICT)   # why it only until box size 99
    """
    """
    save_path_1 = data_path + file_name_1
    save_path_2 = data_path + file_name_2
    dataDICT_1.to_csv(save_path_1, sep = "," ,index = False , header = True, encoding = "UTF-8")
    dataDICT_2.to_csv(save_path_2, sep = "," ,index = False , header = True, encoding = "UTF-8")    
    """
    #try:
        #with open(csvfile_name, 'w') as csvfile:
            #writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            #writer.writeheader()
            #for data in boxedDICT:
                #print(data)
                ##writer.writerow(data)
    #except IOError:
        #print("I/O error")
    
    
    """
    #### SHUFFLED ####
    shuffuled_word_boxDICT = {}
    
    # Count the appearance of the target word in the box_wordLIST after the disecction was done
    # According to the sequence of the splited raw text = every segmented word in the text
    for wordSTR in raw_textLIST:
        #print(wordSTR)
        
        # Access every elements inside the stored All_boxed_textLIST & All_shuffled_boxed_textLIST, which are the boxed results of every box size
        for shuffled_boxedLIST in All_shuffled_boxed_textLIST:
            #print(wordSTR)
            #print(boxedLIST)
            #print(type(boxedLIST))
            t_wordcountINT = 0
            
            # Access the elements of boxed list based on the box size
            for small_s_box_wordLIST in shuffled_boxed_textLIST:
                #print("small_box_wordLIST = ", small_box_wordLIST)  # The model only catchs the last small_box_wordLIST, there for the word count might be wrong
                
                # Count the existence of the target word
                if wordSTR in small_s_box_wordLIST:
                    t_wordcountINT +=1
                    #print(wordSTR)
            #print("The word count of", "[", wordSTR, "]", "in box size = ", "[", len(boxedLIST[0]), "]", "is", t_wordcountINT)
            #print(type(t_wordcountINT))
            # The count in this section would need to be DICTed by the box size
            #word_boxDICT = {"marathon":{{"Box_size_1": 7},
                                      #  {"Box_size_2": 7},.....},
                        #    "the":{{"Box_size_1": 7},
                        #           {"Box_size_2": 7},...}, 
                        #    .....}
            
            #box_countDICT = {"Box_size_%d" %len(boxedLIST[0]):t_wordcountINT}
            #print(box_countDICT)
            
            # Store everything into a DICT
            # The old version
            shuffuled_word_boxDICT["%s_%d" %(wordSTR, len(shuffled_boxedLIST[0]))] = {"Box_size_%d" %len(shuffled_boxedLIST[0]):t_wordcountINT}
            
    print(shuffuled_word_boxDICT)
    print(len(shuffuled_word_boxDICT))
    """

