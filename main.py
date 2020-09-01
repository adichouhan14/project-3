# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 19:32:17 2020

@author: adichouhanofficial
"""
import numpy as np
import pandas as pd

def main():
    url='dataset//global_terror.csv'
    terror=pd.read_csv(url)
    print(terror.shape)
    print(terror.head())
    india=terror[terror['country_txt']=='India']
    print(india.shape)
    india['nkill'].fillna(0, inplace=True)
   # print(india.isnull().sum()*100/india.shape[0])
   # print(india.columns.tolist())
    print(terror['attacktype1_txt'].unique().tolist())
    print(terror['weaptype1_txt'].unique().tolist())
    print(terror.isnull().all(axis=0))
    #print(india.iloc[:2,:5])
    print(sorted(india['iyear'].unique().tolist()))
    

if __name__=="__main__":
    main()