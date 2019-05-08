#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/8/28 14:43
"""
import os
import glob
import pandas as pd
import numpy as np

path1="F:\\2018\join"
#outsomedata=path1+"\\123.csv"
outexcel=path1+"\\resorting_join.csv"
print(outexcel)
#outtemp=path1+"\\temp.csv"
#print(outsomedata)
firstfile=True
alldata=[]
for file in glob.glob(os.path.join(path1,"*.csv")):
    name=os.path.basename(file.upper().rstrip('.CSV'))
    print(name)
    with open(file,'r') as f:
        i=0
        for row in f:
            i+=1
            if (i>=11)&(i<=13):
                alldata.append(name+','+row)
            elif i>13:
                break
with open(outexcel,'a') as out          :
    for line in alldata:
        out.write(line)
print(out)

