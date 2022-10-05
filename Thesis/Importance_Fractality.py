#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pprint import pprint
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
    M = the word frequency >> count the appearance of the target word in the text  >> DONE
    s = the box size = how many words were count as one box >> from 1 to the maximum length of the text
    w = the target word
    
    
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
    
    raw_textLIST = testing_text.lower().split()
    print(raw_textLIST)
    
    """
    # set the value of N (N = "The length of the text")
    N = float(len(raw_textLIST))
    print("N (The length of the text) = ", N)
    #print(type(N))
    #pprint(raw_textLIST)
    print(len(raw_textLIST))
    
    # word frequency count  # M >> needs to call out the word(key) for its count(value)
    # method 1
    word_frequncyDICT = word_frequncy(testing_text)
    print("Func:", word_frequncyDICT) # Follow the word sequence of text
    print(len(word_frequncyDICT))
    
    # method 2
    word_frequncyDICT_2 = Counter(raw_textLIST)
    print("Counter:", word_frequncyDICT_2) # Listed in the rank of frequency
    print(len(word_frequncyDICT_2))
    
    """

    #make a box size list for segment the text according to the box size
    lengthLIST = list(range(1,len(raw_textLIST)+1))
    print(lengthLIST) # How long is this text
    
    #divide the text by the box size
    for s in lengthLIST:  # s = box isze
        boxed_textLIST = []
        boxLIST = []
        shuffled_boxed_textLIST = []
        shuffled_boxLIST = []
        
        # Unshuffled Box Disecction
        for c in range(len(raw_textLIST)):  # c = word count
            # only starting to box the word based on the box size (meaning the residue of that word index is equal to zero)
            if c%s == 0: # s == box size
                boxLIST = raw_textLIST[c:c+s]  # [w:w+s] => if w = 2; s = 2 , [w:w+s] = [2:4] = collect word from index 2-3 => [index2 , index3]
                #print(boxLIST)
                #print(len(boxLIST))
                boxed_textLIST.append(boxLIST)
            else:
                pass
    print(boxed_textLIST)
    print(len(boxed_textLIST))
    print("Box dissecction DONE")
        
    
    for wordSTR in raw_textLIST:
        print(wordSTR)
    
        
        
        
        """
        # Shuffled text Box Dissection (YET, Untested)
        for shuffle_c in range(len(raw_textLIST)):
            
            
            if shuffle_c%s == 0: # s == box size
                shuffled_boxLIST = raw_textLIST[shuffle_c:shuffle_c+s]  # [w:w+s] => if w = 2; s = 2 , [w:w+s] = [2:4] = collect word from index 2-3 => [index2 , index3]
                #print(boxLIST)
                #print(len(boxLIST))
                shuffled_boxed_textLIST.append(shuffled_boxLIST)
            else:
                pass            
        """

        #print(huffled_boxed_textLIST)
        #print(len(huffled_boxed_textLIST))
        #print("Shuffled Box dissecction DONE")
    
        #for w in raw_textLIST:
        
        # what if I store the boxes into a DICT, and index those boxes by it's length?? (NO, by the time)
    
    

        """
    # text preprocessing >> remove punctuation
    # Storing the sets of punctuation in variable result 
    puncSTR = string.punctuation
    
    puncLIST = []
    for punc in puncSTR:
        puncLIST.append(punc)
    print(puncLIST)
    print(type(puncLIST))
    
    boxed_textLIST = []
    for wordSTR in raw_textLIST:
        for punc in puncLIST:
            if punc in wordSTR:
                print(wordSTR)
                wordSTR.translate(wordSTR.maketrans('', '', punc))
                print("New word:", wordSTR)
       # print(wordSTR)
                #boxed_textLIST.append(wordSTR)
            #else:
                #boxed_textLIST.append(wordSTR)
                #pass
    #pprint(boxed_textLIST)
        #print(wordSTR)
        #print(type(strROW))
    """

