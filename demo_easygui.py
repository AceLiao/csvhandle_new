#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/8/24 11:26
"""
import easygui as g
import os
import glob
import pandas as pd
import numpy as np

import sys
title="COT文件处理"
msg="你想输出什么？"
choices=['合档 输出csv','合档 输出excel',"统计均值+良率"]
reply=g.choicebox(msg,title,choices=choices)

def path_get():
    i=g.enterbox("请输入需要处理的文件夹地址：",title="地址",default="F:\\2018\join")
    return i

def out_excel():
    outexcel = path1 + "\\csvjoin.xlsx"
    firstfile = 1
    alldata = []
    for file in glob.glob(os.path.join(path1, "*.csv")):
        name = os.path.basename(file.upper().rstrip('.CSV'))
        print(name)
        if firstfile:
            df = pd.read_csv(file, header=52)
            df.insert(0, "Wafer", name)
            columns = df.columns.values
            firstfile = 0
            df = df.dropna(axis=1, how='all')
            x = [1, 2, 3, 5, 6, 7, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            #df.drop(df.columns[x], axis=1, inplace=True)
            alldata.append(df)
        else:
            df = pd.read_csv(file, skiprows=53)
            df.insert(0, "Wafer", name)
            df = df.dropna(axis='columns', how='all')
            #df.drop(df.columns[x], axis=1, inplace=True)
            alldata.append(df)
    alldata_concat = pd.concat(alldata, axis=0)
    alldata_concat.to_excel(outexcel, sheet_name="data", index=None)

def out_csv():
    outcsv = path1 + "\\csvjoin.csv"
    firstfile = 1
    alldata = []
    for file in glob.glob(os.path.join(path1, "*.csv")):
        name = os.path.basename(file.upper().rstrip('.CSV'))
        print(name)
        if firstfile:
            df = pd.read_csv(file, header=52)
            df.insert(0, "Wafer", name)
            columns = df.columns.values
            firstfile = 0
            df = df.dropna(axis=1, how='all')
            x = [1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            df.drop(df.columns[x],  inplace=True)
            alldata.append(df)
        else:
            df = pd.read_csv(file, skiprows=53)
            df.insert(0, "Wafer", name)
            df = df.dropna(axis='columns', how='all')
            df.drop(df.columns[x], inplace=True)
            alldata.append(df)
    alldata_concat = pd.concat(alldata, axis=0)
    alldata_concat.to_csv(outcsv, index=None)

def avg(path):
    out_avg_yield=path+"\\out_avg_yield.xlsx"
    col = ["Wafer ID", "LOP", "VF1", "WLD","VF1_Yield" ,"LOP1_Yield","VF3_Yield", "IR_Yield"]
    lop = pd.DataFrame(columns=col)
    na = 0

    pd_data1=pd.DataFrame(columns=col)
    first = True
    #寻找头文件的型号；对应不用型号的卡控标准
    while first == True:
        firstfile = glob.glob(os.path.join(path, "*.CSV"))[0]
        name1 = os.path.basename(firstfile.upper().rstrip('.CSV'))[:2]
        name2 = os.path.basename(firstfile.upper().rstrip('.CSV'))[:4]
        first = False
        if name1 == '33':
            # -----------------------------------------------------请修改需要的33分布分档值
            lopmin, lopmax, lopstep = 540, 620, 10
            vf1min, vf1max, vf1step = 2.9, 3.3, 0.05
            vf3min, vf3max, vf3step = 1.5, 2.5, 0.1
            irmin, irmax, irstep = 0, 1, 0.1
        elif name1 == "18":
            # -----------------------------------------------------请修改需要的18分布分档值
            lopmin, lopmax, lopstep = 80, 118, 2
            vf1min, vf1max, vf1step = 2.9, 3.3, 0.05
            vf3min, vf3max, vf3step = 2.0, 2.5, 0.1
            irmin, irmax, irstep = 0,0.2, 0.1
        elif name1 == "20":
            # -----------------------------------------------------请修改需要的20分布分档值
            lopmin, lopmax, lopstep = 100, 300, 1
            vf1min, vf1max, vf1step = 2.8, 3.40, 0.05
            vf3min, vf3max, vf3step = 2.0, 2.5, 0.1
            irmin, irmax, irstep = 0, 0.2, 0.1
        elif name1 == "28":
            # -----------------------------------------------------请修改需要的28分布分档值
            lopmin, lopmax, lopstep = 200, 248, 2
            vf1min, vf1max, vf1step = 3.0, 3.5, 0.02
            vf3min, vf3max, vf3step = 2.0, 2.5, 0.1
            irmin, irmax, irstep = 0, 1, 0.1
        elif name1 == "40":
            # -----------------------------------------------------请修改需要的40分布分档值
            lopmin, lopmax, lopstep = 570, 700, 10
            vf1min, vf1max, vf1step = 2.9, 3.3, 0.05
            vf3min, vf3max, vf3step = 1.5, 2.5, 0.1
            irmin, irmax, irstep = 0, 1, 0.1
        elif name1 == "45":
            # -----------------------------------------------------请修改需要的40分布分档值
            lopmin, lopmax, lopstep = 650, 750, 10
            vf1min, vf1max, vf1step = 2.9, 3.3, 0.05
            vf3min, vf3max, vf3step = 1.5, 2.5, 0.1
            irmin, irmax, irstep = 0, 1, 0.1

    i=0
    for file in glob.glob(os.path.join(path, "{0}*.CSV".format(name1))):
        name = os.path.basename(file.upper().rstrip('.CSV'))
        df = pd.read_csv(file, skiprows=53)  # 读取CSV文件
        colu = df.columns
        n1 = df.TEST.count()
        na += n1
        # -----------------------计算均值
        avglop = round(np.mean(df.LOP1[df.LOP1 >= lopmin]), 1)  # 计算均值（去坏点）
        avgvf1 = round(np.mean(df.VF1[(df.VF1 >= 2.8) & (df.VF1 <= 3.5)]), 3)  # 计算均值（去坏点）
        avgwld = round(np.mean(df.WLD1[(df.WLD1 >= 440) & (df.WLD1 <= 470)]), 1)  # 计算均值（去坏点）

        # -----------------------计算良率
        VF1yield=round(df.VF1[(df.VF1>=2.70)&(df.VF1<=3.4)].count()/n1*100,2)
        LOP1yield=round(df.LOP1[(df.LOP1>=lopmin)&(df.LOP1<=lopmax)].count()/n1*100,2)
        vf3yield = round(df.VF3[(df.VF3 >= 1.5) & (df.VF3 <= 2.5)].count() / n1 * 100, 2)
        iryield = round(df.IR[(df.IR <= 1)].count() / n1 * 100, 2)

        pd_data1.loc[i]=(name, avglop, avgvf1, avgwld, VF1yield,LOP1yield,vf3yield, iryield)
        i=i+1
    pd_data1.to_excel(out_avg_yield,sheet_name="Avg&Yield",index=None)

if __name__ == '__main__':
    path1 = path_get()
    if reply == choices[1]:
        out_excel()
    elif reply == choices[0]:
        out_csv()
    elif reply ==choices[2]:
        avg(path1)



