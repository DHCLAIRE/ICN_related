#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json


if __name__ == "__main__":
	
	data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/二代語料/"
	tmpLIST = []
	tmpLIST_2 = []
	tmpLIST_3 = []
	tmpLIST_4 = []
	tmpLIST_5 = []
	tmpLIST_6 = []
	raw_pseudowordsLIST = []
	
	
	with open (data_path + "MALD1_PseudowordsData.csv", "r", encoding = "utf-8") as raw_file:
		fileLIST = raw_file.read().split("\n")
		#pprint(fileLIST)
		
		for pseudo_item in fileLIST:
			tmpLIST = pseudo_item.split(",")
			if len(tmpLIST[0]) == 8:
				#print(tmpLIST[0])
				raw_pseudowordsLIST.extend([tmpLIST[0]])
			else:
				pass
			
			
		# the 1st layer
		for lvl2_pseudoItem in raw_pseudowordsLIST:
			#print(lvl2_pseudoItem)
			#print(type(lvl2_pseudoItem))
			
			if 'a' in lvl2_pseudoItem:
				print(lvl2_pseudoItem)
				tmpLIST_2.extend([lvl2_pseudoItem])
			else:
				pass
		pprint(tmpLIST_2)
		print(len(tmpLIST_2))
		"""
		# the 2nd layer
		for c in tmpLIST_2:
			if 'e' in c:
				print(c)
				tmpLIST_3.extend([c])
			else:
				pass
		print(tmpLIST_3)
		print(len(tmpLIST_3))
		
		
		# the 3rd layer
		for z in tmpLIST_3:
			if 's' in z:
				print(z)
				tmpLIST_4.extend([z])
			else:
				pass
		print(tmpLIST_4)
		print(len(tmpLIST_4))
		
		
		# the 4th layer
		for a in tmpLIST_4:
			if 't' in a:
				print(a)
				tmpLIST_5.extend([a])
			else:
				pass
		print(tmpLIST_5)
		print(len(tmpLIST_5))	
		
		
		# the 5th layer
		for b in tmpLIST_5:
			if 'n' in b:
				print(c)
				tmpLIST_6.extend([b])
			else:
				pass
		print(tmpLIST_6)
		print(len(tmpLIST_6))			
		#"""
