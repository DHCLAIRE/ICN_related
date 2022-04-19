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
    Number of shuffled box count(Nsh-b(s, w)) = M(The frequency of the word ) / 1+(M-1/N-1)(s-1)
    N = the number of word in a text
    s = the box size = how many words were count as one box
    """