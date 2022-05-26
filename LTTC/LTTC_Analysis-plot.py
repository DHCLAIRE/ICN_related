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
from collections import Counter
import statistics
from scipy import stats

def LISTblankEraser(rawLIST):
    '''
    Remove the blank item inside the list
    '''
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    return newrawLIST

def Corr(x, y):
    '''
    To get the correlation of the target x and y
    '''
    XtoY_corr = x.corr(y)
    #print(XtoY_corr)
    return XtoY_corr

def get_List(resultLIST, i):
    '''
    Extract the wanted data from the raw data LIST
    '''
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    return contentLIST

def scatter_fit_plot(x, y1, y2, y1_c1, y2_c2, x_lable, y_lable, fig_title):  #, y3 = None, y4 = None ; , y3_c3 = None, y4_c4 = None
    plt.scatter(x, y1 ,c = y1_c1)
    plt.scatter(x, y2 , c = y2_c2)
    plt.xlabel(x_lable)
    plt.ylabel(y_lable)
    plt.title(fig_title)
    plt.legend()

    # 使用 Numpy 的 polyfit，參數 1 代表一維，算出 fit 直線斜率
    m_1, c_1 = np.polyfit(x, y1, 1) 
    m_2, c_2 = np.polyfit(x, y2, 1)
    plt.plot(x, m_1 * x + c_1, color = y1_c1)
    plt.plot(x, m_2 * x + c_2, color = y2_c2)
    print(m_1, c_1)
    print(m_2, c_2)
    
    plt.show()
    
    

if __name__ == "__main__":
    
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    """
    columns=['Sub_id',
    '(ms)H_raw_RTMean',
    '(ms)H_final_RTMean',
    '(ms)L_raw_RTMean',
    '(ms)L_final_RTMean',
    '(%)ALL_Correctness',
    '(%)H_raw_Correctness',
    '(%)H_final_Correctness',
    '(%)L_raw_Correctness',
    '(%)L_final_Correctness',
    'Self_rating_Mean',
    'H_Self_rating_Mean',
    'L_Self_rating_Mean',
    '(ms)Self_readingT_msMean',
    '(ms)H_Self_readingT_msMean',
    '(ms)L_Self_readingT_msMean',
    '(min)Self_readingT_minMean',
    '(min)H_Self_readingT_minMean',
    '(min)L_Self_readingT_minMean'])
    """
    
    
    with open (result_data_path + "000_007-035_PLDT_analyzed_results.csv", "r", encoding = "utf-8") as csvfile:
        data = pd.read_csv(csvfile, index_col=0)
        
        x_correctness = data['(%)ALL_Correctness']
        x_Hcorrectness = data['(%)H_final_Correctness']
        x_Lcorrectness = data['(%)L_final_Correctness']
        
        y_H_RT = data['(ms)H_final_RTMean']
        y_L_RT = data['(ms)L_final_RTMean']
        
        y_rating_all = data['Self_rating_Mean']
        y_rating_H = data['H_Self_rating_Mean']
        y_rating_L = data['L_Self_rating_Mean']
        
        y_reading_allT = data['(min)Self_readingT_minMean']
        y_reading_HT = data['(min)H_Self_readingT_minMean']
        y_reading_LT = data['(min)L_Self_readingT_minMean']
        #print(y_H_RT)
        
        # To check whether the data is considered as normal distributed or not
        sub_normality = stats.shapiro(data['(%)ALL_Correctness'])  # because the num of subjects is < 50
        print(sub_normality)  # (0.9736784100532532, 0.6064378619194031)  p-value > .05 , therefore the subjects are normal distributed.
        # https://quantifyinghealth.com/report-shapiro-wilk-test/  >> How to interpret the test result
        
        # correlation: C to RT
        H_C = Corr(x_correctness, y_H_RT)
        L_C = Corr(x_correctness, y_L_RT)
        H_HC = Corr(x_Hcorrectness, y_H_RT)
        L_LC = Corr(x_Lcorrectness, y_L_RT)
        print("H to ALL-C: ", H_C)
        print("L to ALL-C: ", L_C)
        print("H to H-C: ", H_HC)
        print("L to L-C: ", L_LC)
        
        # correlation: C to rating
        Cto_ratingALL_corr = Corr(x_correctness, y_rating_all)
        Cto_ratingH_corr = Corr(x_Hcorrectness, y_rating_H)
        Cto_ratingL_corr = Corr(x_Lcorrectness, y_rating_L)
        print("ratingALL to C: ", Cto_ratingALL_corr)
        print("rating-H to C: ", Cto_ratingH_corr)
        print("rating-L to C: ", Cto_ratingL_corr)
        
        # correlation: C to reading time
        Cto_readingALL_corr = Corr(x_correctness, y_reading_allT)
        Cto_readingH_corr = Corr(x_Hcorrectness, y_reading_HT)
        Cto_readingL_corr = Corr(x_Lcorrectness, y_reading_LT)
        print("readingALL to C: ", Cto_readingALL_corr)
        print("reading-H to C: ", Cto_readingH_corr)
        print("reading-L to C: ", Cto_readingL_corr)
        
        # correlation: Rating to Reading
        Ratingto_ReadingALL_corr = Corr(y_rating_all, y_reading_allT)
        Ratingto_ReadingH_corr = Corr(y_rating_H, y_reading_HT)
        Ratingto_ReadingL_corr = Corr(y_rating_L, y_reading_LT)
        print("rating to reading ALL: ", Ratingto_ReadingALL_corr)
        print("rating to reading H: ", Ratingto_ReadingH_corr)
        print("rating to reading L: ", Ratingto_ReadingL_corr)
                
        
        
        """
        # T test section #  WEIRD!!!!
        t_testCtoHRT_R = stats.ttest_rel(x_correctness, y_H_RT)
        t_testCtoLRT_R = stats.ttest_rel(x_correctness, y_L_RT)
        print("C to H-RT: ", t_testCtoHRT_R)  # sig. >> e-15
        print("C to L-RT: ", t_testCtoLRT_R)  # sig. >> e-17
        
        t_testLRTtoHRT_R = stats.ttest_rel(y_L_RT, y_H_RT)
        print("L-RT to H-RT: ", t_testLRTtoHRT_R) # n.s.
        """
        
        """
    for z in range(1):
        sub_num = "0{0:02d}".format(z+7)
        with open (result_data_path + "{}_Reading_task.csv".format(sub_num), "r", encoding = "unicode_escape") as csvfile:
            data = pd.read_csv(csvfile, index_col=0)
            
            Count = [1,2,3,4,5,6,7]
            df = pd.DataFrame({"rating": data['Rating Scale'], "Count": Count})
            ax = df.plot.hist(column=["rating"], by= "Count")
            
            #age_list = [8, 10, 12, 14, 72, 74, 76, 78, 20, 25, 30, 35, 60, 85]
            #df = pd.DataFrame({"gender": list("MMMMMMMMFFFFFF"), "age": age_list})
            #ax = df.plot.hist(column=["age"], by="gender", figsize=(10, 8))
           
            #data['Rating Scale'].plot(data['Rating Scale'], Count, kind="bar")
        """
            
        
        """
        # H & L RT & ALL_Correctness(Scatter & Regression line)
        # Setting the ax and the plot content of H & L raw RT with Correctness
        ax1 = data.plot.scatter(x = "(%)ALL_Correctness", y = "(ms)H_final_RTMean", alpha = 0.5, color='Blue',label='H_rawRT')
        data.plot.scatter(x = "(%)ALL_Correctness", y = "(ms)L_raw_RTMean", alpha = 0.5, color='Red',label='L_rawRT', ax = ax1)
        
        # 使用 Numpy 的 polyfit，參數 1 代表一維，算出 fit 直線斜率
        m_rawH, c_rawH = np.polyfit(data['(%)ALL_Correctness'], data['(ms)H_raw_RTMean'], 1) 
        m_rawL, c_rawL = np.polyfit(data['(%)ALL_Correctness'], data['(ms)L_raw_RTMean'], 1)
        ax1.plot(data['(%)ALL_Correctness'], m_rawH * data['(%)ALL_Correctness'] + c_rawH, color = 'Blue')
        ax1.plot(data['(%)ALL_Correctness'], m_rawL * data['(%)ALL_Correctness'] + c_rawL, color = 'Red')
        print(m_rawH, c_rawH)
        print(m_rawL, c_rawL)
        
        
        ax1 = data.plot.scatter(x = "(%)ALL_Correctness", y = "(ms)H_final_RTMean", alpha = 0.5, color='Blue',label='H_rawRT')
        data.plot.scatter(x = "(%)ALL_Correctness", y = "(ms)L_final_RTMean", alpha = 0.5, color='Red',label='L_rawRT', ax = ax1)
        
        # 使用 Numpy 的 polyfit，參數 1 代表一維，算出 fit 直線斜率
        m_rawH, c_rawH = np.polyfit(data['(%)ALL_Correctness'], data['(ms)H_final_RTMean'], 1) 
        m_rawL, c_rawL = np.polyfit(data['(%)ALL_Correctness'], data['(ms)L_final_RTMean'], 1)
        ax1.plot(data['(%)ALL_Correctness'], m_rawH * data['(%)ALL_Correctness'] + c_rawH, color = 'Blue')
        ax1.plot(data['(%)ALL_Correctness'], m_rawL * data['(%)ALL_Correctness'] + c_rawL, color = 'Red')
        ax1.xlabel("Correctness")
        ax1.ylabel("Correctness")
        print(m_rawH, c_rawH)
        print(m_rawL, c_rawL)
        
        
        # H & L RT & H & L_Correctness(Scatter & Regression line)
        ax3 = data.plot.scatter(x = "(%)H_raw_Correctness", y = "(ms)H_raw_RTMean", alpha = 0.5, color='Purple',label='H_rawRT')
        data.plot.scatter(x = "(%)H_final_Correctness", y = "(ms)H_final_RTMean", alpha = 0.5, color='Red',label='H_finalRT', ax = ax3)
        
        m_rawH, c_rawH = np.polyfit(data['(%)H_raw_Correctness'], data['(ms)H_raw_RTMean'], 1) 
        m_finalH, c_finalH = np.polyfit(data['(%)H_final_Correctness'], data['(ms)H_final_RTMean'], 1)
        ax3.plot(data['(%)H_raw_Correctness'], m_rawH * data['(%)H_raw_Correctness'] + c_rawH, color = 'Purple')
        ax3.plot(data['(%)H_final_Correctness'], m_finalH * data['(%)H_final_Correctness'] + c_finalH, color = 'Red')
        
        
        data.plot.scatter(x = "(%)L_raw_Correctness", y = "(ms)L_raw_RTMean", alpha = 0.5, color='Navy',label='L_rawRT', ax = ax3)
        data.plot.scatter(x = "(%)L_final_Correctness", y = "(ms)L_final_RTMean", alpha = 0.5, color='Gray',label='L_finalRT', ax = ax3)
        
        m_rawL, c_rawL = np.polyfit(data['(%)L_raw_Correctness'], data['(ms)L_raw_RTMean'], 1) 
        m_finalL, c_finalL = np.polyfit(data['(%)L_final_Correctness'], data['(ms)L_final_RTMean'], 1)
        ax3.plot(data['(%)L_raw_Correctness'], m_rawL * data['(%)L_raw_Correctness'] + c_rawL, color = 'Navy')
        ax3.plot(data['(%)L_final_Correctness'], m_finalL * data['(%)L_final_Correctness'] + c_finalL, color = 'Orange')
        
        
        # Self-rating
        ax4 = data.plot.scatter(x = "(%)ALL_Correctness", y = "Self_rating_Mean", alpha = 0.5, color='Black',label='Self_rating_All')
        data.plot.scatter(x = "(%)ALL_Correctness", y = "H_Self_rating_Mean", alpha = 0.5, color='Green',label='Self_rating_H', ax = ax4)
        data.plot.scatter(x = "(%)ALL_Correctness", y = "L_Self_rating_Mean", alpha = 0.5, color='Red',label='Self_rating_L', ax = ax4)
        
        m_allC, c_allC = np.polyfit(data['(%)ALL_Correctness'], data['Self_rating_Mean'], 1)
        m_HC, c_HC = np.polyfit(data['(%)ALL_Correctness'], data['H_Self_rating_Mean'], 1)
        m_LC, c_LC = np.polyfit(data['(%)ALL_Correctness'], data['L_Self_rating_Mean'], 1)
        ax4.plot(data['(%)ALL_Correctness'], m_allC * data['(%)ALL_Correctness'] + c_allC, color = 'Black')
        ax4.plot(data['(%)ALL_Correctness'], m_HC * data['(%)ALL_Correctness'] + c_HC, color = 'Green')
        ax4.plot(data['(%)ALL_Correctness'], m_LC * data['(%)ALL_Correctness'] + c_LC, color = 'Red')
        
        # Self-reading
        ax5 = data.plot.scatter(x = "(%)ALL_Correctness", y = "(min)Self_readingT_minMean", alpha = 0.5, color='Orange',label='Self_reading_All')
        data.plot.scatter(x = "(%)ALL_Correctness", y = "(min)H_Self_readingT_minMean", alpha = 0.5, color='Navy',label='Self_reading_H', ax = ax5)
        data.plot.scatter(x = "(%)ALL_Correctness", y = "(min)L_Self_readingT_minMean", alpha = 0.5, color='Lightgray',label='Self_reading_L', ax = ax5)
        
        m_allR, c_allR = np.polyfit(data['(%)ALL_Correctness'], data['(min)Self_readingT_minMean'], 1)
        m_HR, c_HR = np.polyfit(data['(%)ALL_Correctness'], data['(min)H_Self_readingT_minMean'], 1)
        m_LR, c_LR = np.polyfit(data['(%)ALL_Correctness'], data['(min)L_Self_readingT_minMean'], 1)
        ax5.plot(data['(%)ALL_Correctness'], m_allR * data['(%)ALL_Correctness'] + c_allR, color = 'Orange')
        ax5.plot(data['(%)ALL_Correctness'], m_HR * data['(%)ALL_Correctness'] + c_HR, color = 'Navy')
        ax5.plot(data['(%)ALL_Correctness'], m_LR * data['(%)ALL_Correctness'] + c_LR, color = 'Lightgray')
        
        # Self-rating to Reading time
        ax6 = data.plot.scatter(x = "Self_rating_Mean", y = "(min)Self_readingT_minMean", alpha = 0.5, color='Black',label='Reading-Rating_All')
        data.plot.scatter(x = "H_Self_rating_Mean", y = "(min)H_Self_readingT_minMean", alpha = 0.5, color='Red',label='Reading-Rating_H', ax = ax6)
        data.plot.scatter(x = "L_Self_rating_Mean", y = "(min)L_Self_readingT_minMean", alpha = 0.5, color='Blue',label='Reading-Rating_L', ax = ax6)
        
        m_allRtoR, c_allRtoR = np.polyfit(data['Self_rating_Mean'], data['(min)Self_readingT_minMean'], 1)
        m_HRtoR, c_HRtoR = np.polyfit(data['H_Self_rating_Mean'], data['(min)H_Self_readingT_minMean'], 1)
        m_LRtoR, c_LRtoR = np.polyfit(data['L_Self_rating_Mean'], data['(min)L_Self_readingT_minMean'], 1)
        ax6.plot(data['Self_rating_Mean'], m_allRtoR * data['Self_rating_Mean'] + c_allRtoR, color = 'Black')
        ax6.plot(data['H_Self_rating_Mean'], m_HRtoR * data['H_Self_rating_Mean'] + c_HRtoR, color = 'Red')
        ax6.plot(data['L_Self_rating_Mean'], m_LRtoR * data['L_Self_rating_Mean'] + c_LRtoR, color = 'Blue')
        """
        
        
        