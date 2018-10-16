# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:40:17 2018

@author: Aum_Pandya
"""

import numpy as np
import pandas as pd

increase_rate = 0.02
date_limit = 7

data_source =data = pd.read_csv("D:\Python\VoluntaryWork\Data.csv",header=0, sep=",", index_col=0, parse_dates = True)
data= data.reset_index()
data.sort_values('date', ascending=True)
data = data[(data['albumin']>0) & (data['creatinine']>0)]
data = data.sample(n=30)
data['s_alb'] =data['albumin'].shift().fillna(0) #shift
data['s_cre'] =data['creatinine'].shift().fillna(0) #shift
data['c_cre'] = ((data['creatinine'] - data['s_cre'])/data['s_cre'])*100
data['c_alb'] = ((data['albumin'] - data['s_alb'])/data['s_alb'])*100
data= data.reset_index()
result=pd.DataFrame()
pd.DataFrame(result, columns=('Date','Type' ,'IncreaseCount', 'IncreasePresentageAvg','DecreaseCount', 'DecreasePresentageAvg'))

for itr in range(0,len(data.index)-date_limit-1):
    rbcsummary = {
           "date":data.get_value(itr,'date'),
           "type": "RBC",
           "inc_count":0,
           "inc_pre_avg":0,
           "dec_count":0,
           "dec_per_avg":0
           }
    percentinc= percentdec=0
    if(data.get_value(itr,'c_alb') >= increase_rate and data.get_value(itr,'c_cre') >=increase_rate):
        for itr1 in range(1,date_limit):
            #print(itr," ",itr1," ",data.get_value(itr+itr1,'rbc')," ",data.get_value(itr+itr1-1,'rbc'))
            if(data.get_value(itr+itr1,'rbc')>data.get_value(itr+itr1-1,'rbc')):
                rbcsummary["inc_count"]+=1
                percentinc+=((data.get_value(itr+itr1,'rbc')-data.get_value(itr+itr1-1,'rbc'))/data.get_value(itr+itr1,'rbc'))*100
                rbcsummary["inc_pre_avg"]=percentinc/rbcsummary["inc_count"]
            elif(data.get_value(itr+itr1,'rbc')<data.get_value(itr+itr1-1,'rbc')):
                rbcsummary["dec_count"]+=1
                percentdec+=((data.get_value(itr+itr1,'rbc')-data.get_value(itr+itr1-1,'rbc'))/data.get_value(itr+itr1,'rbc'))*100
                rbcsummary["dec_per_avg"]=percentdec/rbcsummary["dec_count"]
        result.append(pd.DataFrame.from_dict(rbcsummary),ignore_index=True)