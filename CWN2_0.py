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
    
    """
    #TESTING SECTION#
    
    # Find out the target word
    lemmasList = cwn.find_lemma("電腦")
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
    
    