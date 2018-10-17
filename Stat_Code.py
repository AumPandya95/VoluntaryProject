# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:40:17 2018

@author: Aum_Pandya
"""

import numpy as np
import pandas as pd
import openpyxl
import math

increase_rate = 0.02
date_limit = 7
count = 0
data =pd.DataFrame()
path = r'D:/Python/VoluntaryWork/'

def calc_engine(string):
    global increase_rate
    global date_limit
    global data
    global writer
    result=pd.DataFrame(columns=['Date','Type' ,'IncreaseCount', 'IncreasePercentageAvg','DecreaseCount', 'DecreasePercentageAvg'])
    #pd.DataFrame(result, columns=('Date','Type' ,'IncreaseCount', 'IncreasePresentageAvg','DecreaseCount', 'DecreasePresentageAvg'))
    temp_list=[]
    data = data[(data[string] != 0)]   #violated the namespace; hence it changes the data file
    data= data.reset_index(drop = True)  #Resets after every run 
    for itr in range(1,len(data.index)-(date_limit-1)):
        
        summary = {
               "Date":data.loc[itr,'date'],
               "Type": string,
               "IncreaseCount":0,
               "IncreasePercentageAvg":0,
               "DecreaseCount":0,
               "DecreasePercentageAvg":0
               }
        percentinc= percentdec=0
        if((data.loc[itr,'c_alb'] >= increase_rate) & (data.loc[itr,'c_cre'] >= increase_rate)):
            
            #count += 1
            for itr1 in range(1,date_limit):
                #print(itr," ",itr1," ",data.get_value(itr+itr1,'rbc')," ",data.get_value(itr+itr1-1,'rbc'))
                if(data.loc[itr+itr1,string]>data.loc[itr+itr1-1,string]):
                    summary["IncreaseCount"]+=1
                    percentinc+=((data.loc[itr+itr1,string]-data.loc[itr+itr1-1,string])/data.loc[itr+itr1-1,string])*100
                    summary["IncreasePercentageAvg"]=percentinc/summary["IncreaseCount"]
                    #print(rbcsummary)
                elif(data.loc[itr+itr1,string] < data.loc[itr+itr1-1,string]):
                    summary["DecreaseCount"]+=1
                    percentdec+=((data.loc[itr+itr1,string]-data.loc[itr+itr1-1,string])/data.loc[itr+itr1-1,string])*100
                    summary["DecreasePercentageAvg"]=percentdec/summary["DecreaseCount"]
                    #print(rbcsummary)
                    
            temp_list.append(summary)
            
        else:
            continue
        
    result= (pd.DataFrame(temp_list,columns=['Date','Type' ,'IncreaseCount', 'IncreasePercentageAvg','DecreaseCount', 'DecreasePercentageAvg']))
    result.to_excel(writer, sheet_name = string)
    writer.save()

    return 0
    #using .loc[] instead of .get_value() as the latter is deprecated and will be removed in a future release
    
data_source =data = pd.read_csv(path+"Data.csv",header=0, sep=",", index_col=0, parse_dates = True)
data= data.reset_index().sort_values('date',ascending = True).reset_index(drop = True)
#data.sort_values('date', ascending=True)
data = data[(data['albumin']>0) & (data['creatinine']>0)]
#data_sam = data.sample(n=30)
data['s_alb'] =data['albumin'].shift().fillna(0) #shift
data['s_cre'] =data['creatinine'].shift().fillna(0) #shift
data['c_cre'] = ((data['creatinine'] - data['s_cre'])/data['s_cre'])#*100
data['c_alb'] = ((data['albumin'] - data['s_alb'])/data['s_alb'])#*100

o_path = path+'Output.xlsx'

writer = pd.ExcelWriter(o_path, engine = 'openpyxl')
writer.book = openpyxl.Workbook()
calc_engine('rbc')
calc_engine('wbc')
calc_engine('platelets')
writer.close()
# =============================================================================
#         percentinc= percentdec=0
#         if(data.iat[itr,10] >= increase_rate and data.iat[itr,9] >=increase_rate):
#             count += 1
#             #Find a way to remove the row[0] as value of c_alb and c_creatinine is inf
#             for itr1 in range(1,date_limit):
#                 #print(itr," ",itr1," ",data.get_value(itr+itr1,'rbc')," ",data.get_value(itr+itr1-1,'rbc'))
#                 if(data.iat[itr+itr1,5]>data.iat[itr+itr1-1,5]):
#                     rbcsummary["inc_count"]+=1
#                     percentinc+=((data.iat[itr+itr1,5]-data.iat[itr+itr1-1,5])/data.iat[itr+itr1,5])*100
#                     rbcsummary["inc_pre_avg"]=percentinc/rbcsummary["inc_count"]
#                 elif(data.iat[itr+itr1,5]<data.iat[itr+itr1-1,5]):
#                     rbcsummary["dec_count"]+=1
#                     percentdec+=((data.iat[itr+itr1,5]-data.iat[itr+itr1-1,5])/data.iat[itr+itr1,5])*100
#                     rbcsummary["dec_per_avg"]=percentdec/rbcsummary["dec_count"]
#             res = pd.DataFrame([rbcsummary],columns = ['date','type','inc_count','inc_pre_avg','dec_count','dec_per_avg'],index = [count])
#             result = pd.concat([result,res],axis = 0)
# =============================================================================
        
