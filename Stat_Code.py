# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:40:17 2018

@author: Aum_Pandya
"""

import pandas as pd
import openpyxl

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
            for itr1 in range(1,date_limit):
                if(data.loc[itr+itr1,string]>data.loc[itr+itr1-1,string]):
                    summary["IncreaseCount"]+=1
                    percentinc+=((data.loc[itr+itr1,string]-data.loc[itr+itr1-1,string])/data.loc[itr+itr1-1,string])*100
                    summary["IncreasePercentageAvg"]=percentinc/summary["IncreaseCount"]
                elif(data.loc[itr+itr1,string] < data.loc[itr+itr1-1,string]):
                    summary["DecreaseCount"]+=1
                    percentdec+=((data.loc[itr+itr1,string]-data.loc[itr+itr1-1,string])/data.loc[itr+itr1-1,string])*100
                    summary["DecreasePercentageAvg"]=percentdec/summary["DecreaseCount"]                    
            temp_list.append(summary)  
        else:
            continue
    result= (pd.DataFrame(temp_list,columns=['Date','Type' ,'IncreaseCount', 'IncreasePercentageAvg','DecreaseCount', 'DecreasePercentageAvg']))
    result.to_excel(writer, sheet_name = string)
    writer.save()
    return 0
    
data_source =data = pd.read_csv(path+"Data.csv",header=0, sep=",", index_col=0, parse_dates = True)
data= data.reset_index().sort_values('date',ascending = True).reset_index(drop = True)
data = data[(data['albumin']>0) & (data['creatinine']>0)]
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

workbook=openpyxl.load_workbook('D:/Python/VoluntaryWork/Output.xlsx')
sheet=workbook.get_sheet_by_name('Sheet')
workbook.remove_sheet(sheet)
workbook.save('D:/Python/VoluntaryWork/Output.xlsx')