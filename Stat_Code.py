# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:40:17 2018

@author: Aum_Pandya
"""

import numpy as np
import pandas as pd
import openpyxl

increase_rate = 0.02
date_limit = 7
count = 0
data =pd.DataFrame()
path = r'D:/Python/VoluntaryWork/'

data_source =data = pd.read_csv(path+"Data.csv",header=0, sep=",", index_col=0, parse_dates = True)
data= data.reset_index().sort_values('date',ascending = True).reset_index(drop = True)
#data.sort_values('date', ascending=True)
data = data[(data['albumin']>0) & (data['creatinine']>0)]
#data_sam = data.sample(n=30)
data['s_alb'] =data['albumin'].shift().fillna(0) #shift
data['s_cre'] =data['creatinine'].shift().fillna(0) #shift
data['c_cre'] = ((data['creatinine'] - data['s_cre'])/data['s_cre'])*100
data['c_alb'] = ((data['albumin'] - data['s_alb'])/data['s_alb'])*100
#data= data.reset_index()
result=pd.DataFrame(columns = ['date','type','inc_count','inc_pre_avg','dec_count','dec_per_avg'])
#pd.DataFrame(result, columns=('Date','Type' ,'IncreaseCount', 'IncreasePresentageAvg','DecreaseCount', 'DecreasePresentageAvg'))

for itr in range(0,len(data.index)-date_limit-1):
    rbcsummary = {
           "date":data.iat[itr,1],
           "type": "RBC",
           "inc_count":0,
           "inc_pre_avg":0,
           "dec_count":0,
           "dec_per_avg":0
           }
    
#using .iat[] instead of .get_value() as the latter is deprecated and will be removed in a future release
    percentinc= percentdec=0
    if(data.iat[itr,10] >= increase_rate and data.iat[itr,9] >=increase_rate):
        count += 1
        #Find a way to remove the row[0] as value of c_alb and c_creatinine is inf
        for itr1 in range(1,date_limit):
            #print(itr," ",itr1," ",data.get_value(itr+itr1,'rbc')," ",data.get_value(itr+itr1-1,'rbc'))
            if(data.iat[itr+itr1,5]>data.iat[itr+itr1-1,5]):
                rbcsummary["inc_count"]+=1
                percentinc+=((data.iat[itr+itr1,5]-data.iat[itr+itr1-1,5])/data.iat[itr+itr1,5])*100
                rbcsummary["inc_pre_avg"]=percentinc/rbcsummary["inc_count"]
            elif(data.iat[itr+itr1,5]<data.iat[itr+itr1-1,5]):
                rbcsummary["dec_count"]+=1
                percentdec+=((data.iat[itr+itr1,5]-data.iat[itr+itr1-1,5])/data.iat[itr+itr1,5])*100
                rbcsummary["dec_per_avg"]=percentdec/rbcsummary["dec_count"]
        res = pd.DataFrame([rbcsummary],columns = ['date','type','inc_count','inc_pre_avg','dec_count','dec_per_avg'],index = [count])
        result = pd.concat([result,res],axis = 0)
    
