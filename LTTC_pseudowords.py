#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json

if __name__ == "__main__":

	data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/二代語料/"
	tmpLIST = []
	tmpLIST_2 = []
	raw_pseudowordsLIST = []
	
	
	with open (data_path + "MALD1_PseudowordsData.csv", "r", encoding = "utf-8") as raw_file:   
		fileLIST = raw_file.read().split("\n")
		#pprint(fileLIST)
		
		for pseudo_item in fileLIST:
			tmpLIST = pseudo_item.split(",")
			if len(tmpLIST[0]) == 6:
				print(tmpLIST[0])
				raw_pseudowordsLIST.extend([tmpLIST[0]])
			else:
				pass

		for lvl2_pseudoItem in raw_pseudowordsLIST:
			print(lvl2_pseudoItem)
			print(type(lvl2_pseudoItem))
			
			if 'b' in lvl2_pseudoItem:
				print(lvl2_pseudoItem)
				tmpLIST_2.extend([lvl2_pseudoItem])
				if 'c' in lvl2_pseudoItem:
					print(lvl2_pseudoItem)
					tmpLIST_2.extend([lvl2_pseudoItem])				
								
			#if 'e' in lvl2_pseudoItem:
				#print(lvl2_pseudoItem)
				#tmpLIST_2.extend([lvl2_pseudoItem])				
			#if 'c' in lvl2_pseudoItem:
				#print(lvl2_pseudoItem)
				#tmpLIST_2.extend([lvl2_pseudoItem])				
			
			else:
				pass
		print(tmpLIST_2)
		print(len(tmpLIST_2))