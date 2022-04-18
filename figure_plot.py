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
import matplotlib.pyplot as plt


if __name__ == "__main__":
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    # High Correctness group's RT
    y1_High_CD_RT_Mean_HighC = [783.1667, 879.3667]  #[783.1667, 879.3667, 1337.7, 1584.9333]  #[1100.9534, 958.6333, 783.1667, 1584.9333, 1337.7, 879.3667]
    y2_Low_CD_RT_Mean_HighC = [756.8841,869.1667]  #[756.8841,869.1667,1236.9333, 1417.8]   #[1118.6413, 845.6, 756.8841, 1417.8, 1236.9333, 869.1667]
    
    # Low Correctness group's RT
    y3_High_CD_RT_Mean_LowC = [1337.7, 1584.9333]
    y4_Low_CD_RT_Mean_LowC = [1236.9333, 1417.8]
    
    # Correctness
    x1_High_Correctness = [76.67, 84.17]   #[55.83, 65.83, 76.67, 30, 62.5, 84.17]
    x2_Low_Correctness = [30,62.5]
    
    # High-C & High/Low-CD RT plot
    plt.plot(x1_High_Correctness,y1_High_CD_RT_Mean_HighC, label = "HC High-CD RT")
    plt.plot(x1_High_Correctness,y2_Low_CD_RT_Mean_HighC, label = "HC Low-CD RT")
    
    # Low-C & High/Low-CD RT plot
    plt.plot(x2_Low_Correctness,y3_High_CD_RT_Mean_LowC, label = "LC High-CD RT")
    plt.plot(x2_Low_Correctness,y4_Low_CD_RT_Mean_LowC, label = "LC Low-CD RT")
    
    
    plt.title("High/Low Correctness v.s High/Low_CD RT") # title
    plt.ylabel("PLDT RT") # y label
    plt.xlabel("PLDT Correctness") # x label
    plt.legend()
    
    plt.savefig(result_data_path + "LTTC_HCo-and-LCo_RT-Correctness_plt(without Pilots).jpg")