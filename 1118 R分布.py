#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/17 11:09
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
bin=[0]*110
bin_wld=[0]*11
#-----------------------------------------------------请修改需要的分布分档值
lopmin,lopmax,lopstep=80,115,10
vf1min,vf1max,vf1step=2.9,3.4,0.15
wldmin,wldmax,wldstep=440,467.5,2.5
vf3min,vf3max,vf3step=1.9,2.5,0.6
irmin,irmax,irstep=0,0.9,0.9
LOP1=['80~90','90~100','100~115']
VF1=["2.9~3.05","3.05~3.2","3.2~3.4"]
WLD=["440~442.5","442.5~445","445~447.5","447.5~450","450~452.5","452.5~455","455~457.5",
     "457.5~460","460~462.5","462.5~465","465~467.5"]
#WLD=["440~442.5","442.5~445","445~447.5","447.5~450","450~452.5","452.5~455","455~457.5","457.5~460","460~462.5","462.5~465","465~467.5"]
def one_bin(file):
    binnei=[0]*11
    df = pd.read_csv(file, skiprows=53)
    n1 = df.TEST.count()
    global na
    global bin
    global bin_wld
    na = na + n1
    for i in range(3):
        for j in range(3):
            for k in range(11):
                n = 33 * i+ 11 * j + k
                vf1_left = vf1min + vf1step*j
                vf1_right = vf1min+vf1step*(j+1)+0.05*(j//2)
                lop1_left = lopmin + lopstep * i
                lop1_right = lopmin + lopstep * (i+1) + 5 * (i// 2)
                wld1_left = wldmin + wldstep * k
                wld1_right = wld1_left+wldstep
                bin_file = df.TEST[
                    (df.IR < 0.8) & (df.VF3 < 2.5) & (df.VF3 >= 1.9) &(df.VF1<vf1_right)&(df.VF1>=vf1_left)&(df.LOP1<lop1_right)&(df.LOP1>=lop1_left)&(df.WLD1<wld1_right)&(df.WLD1>=wld1_left)].count()
                bin[n] = bin[n] + bin_file
                binnei[k]+=bin_file
                #print("n=",n," ","k=", k,bin_wld[k])
    for k in range(11):
                n=99+k
                wld1_left = wldmin + wldstep * k
                wld1_right = wld1_left + wldstep
                bin_file=df.TEST[(df.IR < 0.8) & (df.VF1<3.8)&(df.VF1>=2.6)&(df.LOP1<150)&(df.LOP1>=50)&(df.WLD1<wld1_right)&(df.WLD1>=wld1_left)].count()
                #print("bin_file",bin_file)
                bin_file=bin_file-binnei[k]
                #print("bin_file", bin_file)
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
        for k in range(11):
            n = 33 *i + 11* j + k
            print(LOP1[i]+" "+VF1[j]+" "+WLD[k]+" "+str(bin[n]))
print(na)
with open(outfile,'a') as out:
    for i in range(3):
        for j in range(3):
            for k in range(11):
                n = 33 * i + 11 * j + k
                zhanbi = bin[n] / na
                out.write(
                    LOP1[i] + "," + VF1[j] + "," + WLD[k] + ","+ str(bin[n]) + "," + str(zhanbi) + "\n")
    for k in range(11):
        n=99+k
        zhanbi=bin[n]/na
        out.write(
            "50~150,2.6~3.8," + WLD[k]  + "," + str(bin[n]) + "," + str(zhanbi) + "\n")
    out.write(str(na)+"\n")
