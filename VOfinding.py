#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json

if __name__ == "__main__":
        
        data_path = "/Users/neuroling/Datasets/中研院平衡語料庫/00_documents_only/"
        tmpLIST = []
        with open (data_path + "txt_001_40.txt", "r", encoding = "utf-8") as raw_file:   
                fileLIST = raw_file.read().split("\n")
                for big_item in fileLIST:
                        k = big_item.split("\u3000")
                        tmpLIST.extend(k)
                fileLIST = tmpLIST
                pprint(fileLIST)