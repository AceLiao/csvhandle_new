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
LOP1=[92,98,102,106,1000]
VF1=[2.8,2.9,3.05,3.2]
WLD=[445,447.5,450,452.5,455,457.5,460,462.5]
len_lop=len(LOP1)-1
len_vf1=len(VF1)-1
len_wld=len(WLD)-1

bin=[0]*len_lop*len_vf1*len_wld
bin_wld=[0]*len_wld
#WLD=["440~442.5","442.5~445","445~447.5","447.5~450","450~452.5","452.5~455","455~457.5","457.5~460","460~462.5","462.5~465","465~467.5"]
def one_bin(file):
    binnei=[0]*len_wld
    f=open(file)
    df = pd.read_csv(f, skiprows=53)
    f.close()
    n1 = df.TEST.count()
    global na
    global bin
    global bin_wld
    na = na + n1
    for i in range(len_lop):
        for j in range(len_vf1):
            for k in range(len_wld):
                n = (len_vf1*len_wld) * i+ (len_wld) * j + k
                '''
                vf1_left = vf1min + vf1step*j
                vf1_right = vf1min+vf1step*(j+1)+0.05*(j//2)
                lop1_left = lopmin + lopstep * i
                lop1_right = lopmin + lopstep * (i+1) + 5 * (i// 2)
                wld1_left = wldmin + wldstep * k
                wld1_right = wld1_left+wldstep
              '''
                vf1_left=VF1[j]
                vf1_right=VF1[j+1]
                lop1_left = LOP1[i]
                lop1_right = LOP1[i+1]
                wld1_left = WLD[k]
                wld1_right = WLD[k+1]

                bin_file = df.TEST[
                    (df.IR < 0.2) & (df.VF3 < 2.5) & (df.VF3 >= 2) &(df.VF1<vf1_right)&(df.VF1>=vf1_left)&(df.LOP1<lop1_right)&(df.LOP1>=lop1_left)&(df.WLD1<wld1_right)&(df.WLD1>=wld1_left)].count()
                bin[n] = bin[n] + bin_file
                binnei[k]+=bin_file
                #print("n=",n," ","k=", k,bin_wld[k])

    return bin
i=0
for file in glob.glob(os.path.join(path,"18*.csv")):
    i=i+1
    print(i)
    #print(file.basename())
    BIN=one_bin(file)
for i in range(len_lop):
    for j in range(len_vf1):
        for k in range(len_wld):
            n = len_vf1*len_wld *i + len_wld* j + k
            print(str(LOP1[i])+"~"+str(LOP1[i+1])+" "+str(VF1[j])+"~"+str(VF1[j+1])+" "+str(WLD[k])+"~"+str(WLD[k+1])+" "+str(bin[n]))
print(na)
with open(outfile,'a') as out:
    for i in range(len_lop):
        for j in range(len_vf1):
            for k in range(len_wld):
                n = len_vf1 * len_wld * i + len_wld * j + k
                zhanbi = bin[n] / na
                out.write(
                    str(LOP1[i]) + "~" + str(LOP1[i + 1]) + " " + str(VF1[j]) + "~" + str(VF1[j + 1]) + " " + str(
                        WLD[k]) + "~" + str(WLD[k + 1]) + " "+ str(bin[n]) + "," + str(zhanbi) + "\n")

    out.write(str(na)+"\n")
