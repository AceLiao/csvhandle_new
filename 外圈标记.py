#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/20 15:55
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
使用说明：运行后请输入文件夹地址，暂时不支持中文名称地址；并在改地址中新建一个文件夹，命名为“biaoji”
标记一片1028数据约23s
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
"""
import os
import pandas as pd
import glob
import csv

path=input("请输入需要标记外圈的文件夹地址：")

for file in glob.glob(os.path.join(path,"*.csv")):
    name=os.path.basename(file)
    newfile=path+"\\biaoji\\"+name
    df=pd.read_csv(file,header=52)
    print(max(df[df['PosY'] == 2]['PosX']),min(df[df['PosY'] == 2]['PosX']))
    df1 = df.copy
    max_x = max(df['PosX'])
    min_x = min(df['PosX'])
    max_y = max(df['PosY'])
    min_y = min(df['PosY'])
    print(max_x,min_x,max_y,min_y)
    for y in range(min_y, max_y + 1):
        maxx = max(df[df["PosY"] == y]['PosX'])
        minx = min(df[df["PosY"] == y]['PosX'])
        indexy = df[df['PosY'] == y].index
        left = df[df['PosY'] == y]['PosX'] - minx
        right = maxx - df[df['PosY'] == y]['PosX']
        for i in indexy:
            df.loc[i, 'LOP2'] = min(left[i], right[i])+1
    for x in range(min_x,max_x+1):
        #print(df[df['PosX'==x]]['PosY'])
        maxy=max(df[df['PosX']==x]['PosY'])
        miny = min(df[df['PosX'] == x]['PosY'])
        indexx = df[df['PosX'] == x].index
        down=df[df['PosX'] == x]['PosY'] - miny
        up=maxy-df[df['PosX'] == x]['PosY']
        for j in indexx:
            df.loc[j,'LOP2']=int(min(up[j]+1,down[j]+1,df.loc[j,'LOP2']))

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
