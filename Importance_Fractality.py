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
    print(type(testing_text))
    print(testing_text)
    
    tmpLIST = testing_text.lower().split(" ")
    
    pprint(tmpLIST)
    print(len(tmpLIST))
    
    for strROW in tmpLIST:
        print(strROW)
        #print(type(strROW))