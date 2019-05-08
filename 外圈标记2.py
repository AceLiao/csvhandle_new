#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/21 14:51
"""
import os
import pandas as pd
import glob
import csv

path=input("请输入非中文文件夹地址：")

for file in glob.glob(os.path.join(path,"*.csv")):
    name=os.path.basename(file)
    newfile=path+"\\biaoji\\"+name
    df=pd.read_csv(file,header=52)
    max_x = int(max(df['PosX']))
    min_x = int(min(df['PosX']))
    max_y = int(max(df['PosY']))
    min_y = int(min(df['PosY']))
    listy=[]
    listx=[]
    for x in range(min_x,max_x+1):
        listy.append([min(df[df["PosX"]==x]['PosY']),max(df[df["PosX"]==x]['PosY'])])
    for y in range(min_y,max_y+1):
        listx.append([min(df[df['PosY']==y]['PosX']),max(df[df['PosY']==y]['PosX'])])
    print("listx=",listx)
    num=max(df['TEST'])
    for i in range(1,num+1):
        x=df[df['TEST']==i]['PosX'].values
        y=df[df['TEST']==i]['PosY'].values

        up=listy[int(x-min_x)][1]-y
        down=y-listy[int(x-min_x)][0]
        left=x-listx[int(y-min_y)][0]
        right=listx[int(y-min_y)][1]-x
        df.loc[(i-1),'LOP2']=int(min(up,down,left,right))+1

    with open(file,'r',newline="") as openfile:
        csvdata=csv.reader(openfile)
        print(csvdata)
        with open(newfile,'a',newline="\n") as firstcsv:
            i=0
            writer=csv.writer(firstcsv)
            for line in csvdata:
                if i < 53:
                    print(line)
                    i+=1
                    writer.writerows([line])

    df.to_csv(newfile,mode='a',index=None)