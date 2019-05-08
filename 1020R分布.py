#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/8/29 16:29
"""
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

#处理文件的路径
path=input("请输入要合档的文件地址：")
#col=["Wafer ID","LOP","VF1","WLD","VF3_Yield","IR_Yield"]
#lop=pd.DataFrame(columns=col)
outfile=path+"\\outfile_new.csv"
na=0
#dic1={}
bin=[0]*81
#-----------------------------------------------------请修改需要的分布分档值
lopmin,lopmax,lopstep=180,225,15
vf1min,vf1max,vf1step=2.95,3.6,0.2
wldmin,wldmax,wldstep=440,465,2.5
vf3min,vf3max,vf3step=1.9,2.5,0.6
irmin,irmax,irstep=0,0.9,0.9
LOP1=['180~195','195~210','210~240']
VF1=["2.95~3.2","3.2~3.4","3.4~3.65"]
WLD=["440~442.5","442.5~445","445~447.5","447.5~450","450~452.5","452.5~455","455~457.5","457.5~460","460~462.5"]
#WLD=["440~442.5","442.5~445","445~447.5","447.5~450","450~452.5","452.5~455","455~457.5","457.5~460","460~462.5","462.5~465","465~467.5"]
def one_bin(file):
    df = pd.read_csv(file, skiprows=53)
    n1 = df.TEST.count()
    global na
    global bin
    na = na + n1
    for i in range(3):
        for j in range(3):
            for k in range(9):
                n = 27 * (i % 4) + 9 * (j % 4) + k
                vf1_left = vf1min + 0.45 * (j % 3 // 2) + 0.25 * ((j % 3) % 2)
                vf1_right = vf1_left + 0.25 - 0.05 * (j % 2)
                lop1_left = lopmin + lopstep * (i % 3)
                lop1_right = lopmin + lopstep * (1 + i % 3) + lopstep * (i % 3 // 2)
                wld1_left = wldmin + wldstep * (k % 9)
                wld1_right = wldmin + wldstep * (1 + k % 9)
                bin_file = df.TEST[
                    (df.IR < 0.9) & (df.VF3 < 2.5) & (df.VF3 >= 2) &(df.VF1<vf1_right)&(df.VF1>=vf1_left)&(df.LOP1<lop1_right)&(df.LOP1>=lop1_left)&(df.WLD1<wld1_right)&(df.WLD1>=wld1_left)].count()
                #bin_file=df.TEST[(df.IR<0.9)&(df.VF3<2.5)&(df.VF3>=1.9)&(df.VF1<vf1_right)&(df.VF1>=vf1_left)&(df.LOP1<lop1_right)&(df.LOP1>=lop1_left)&(df.WLD1<wld1_right)&(df.WLD1>=wld1_left)].count()
                #df.VF3[(df.VF3 >= 1.5) & (df.VF3 <= 2.5)].count()
                bin[n]=bin[n]+bin_file
        #print(bin_file)
        #print("bin[%d]"%n,bin[n])

    return bin
i=0
for file in glob.glob(os.path.join(path,"S*.csv")):
    i=i+1
    print(i)
    #print(file.basename())
    BIN=one_bin(file)
for i in range(3):
    for j in range(3):
        for k in range(9):
            n = 27 * (i % 4) + 9 * (j % 4) + k
            print(LOP1[i%3]+" "+VF1[j%3]+" "+WLD[k%9]+" "+str(bin[n]))
print(na)
with open(outfile,'a') as out:
    for i in range(3):
        for j in range(3):
            for k in range(9):
                n = 27 * (i % 4) + 9 * (j % 4) + k
                zhanbi = bin[n] / na
                out.write(
                    LOP1[i % 3] + " " + VF1[j % 3] + " " + WLD[k % 9] + " "+ str(bin[n]) + " " + str(zhanbi) + "\n")
    out.write(str(na)+"\n")
