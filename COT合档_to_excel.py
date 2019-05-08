# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:46:24 2018
可以输入中文地址
@author: jianya_liao
"""
#文件输出自动保存到输入文件夹
#V2版本更新：列全部为缺省值的丢弃,删除部分不用的数据
import pandas as pd
import os
import glob

path1=input(r"请输入要合档的文件地址：")
#path1="F:\\2018\join\1"
#outsomedata=path1+"\\123.csv"
outexcel=path1+"\\csvjoin.xlsx"

print(outexcel)
#outtemp=path1+"\\temp.csv"
#print(outsomedata)
firstfile=True
alldata=[]
for file in glob.glob(os.path.join(path1,"*.csv")):
    #print(file)
    #print(os.path.basename(file.upper()))
    #print(os.path.basename(file.upper()).strip(4))
    name=os.path.basename(file.upper().rstrip('.CSV'))
    print(name)
    if firstfile:
          f=open(file)
          df=pd.read_csv(f,header=52)
          f.close()
          df.insert(0,"Wafer",name)
          columns=df.columns.values
          firstfile=False
          df=df.dropna(axis=1,how='all')
          x=[]
          #x=[2,3,14,15,16,17,18]
          df.drop(df.columns[x], axis=1, inplace=True)
          alldata.append(df)
    else:
          f = open(file)
          df=pd.read_csv(f,skiprows=53)
          f.close()
          df.insert(0,"Wafer",name) ########################################
          df=df.dropna(axis='columns',how='all')
          df.drop(df.columns[x], axis=1, inplace=True)
          alldata.append(df)

alldata_concat=pd.concat(alldata,axis=0)
#alldata_concat.to_csv(outsomedata,index=False)
#a=pd.read_csv(outsomedata)
alldata_concat.to_excel(outexcel,sheet_name="data",index=None)
