# author:廖建亚;
#新实现功能：不区分型号、使用函数实验分布功能，缩短代码长度、输出计算的均值表csv
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
#处理文件的路径
path=input("请输入要合档的文件地址：")#path=   C:\Users\jianya_liao\Desktop\python\1
col=["Wafer ID","LOP","VF1","WLD","VF3_Yield","IR_Yield"]
lop=pd.DataFrame(columns=col)
na=0
dic1={}
first=True
while first==True:
    firstfile=glob.glob(os.path.join(path,"*.CSV"))[0]
    name1=os.path.basename(firstfile.upper().rstrip('.CSV'))[:2]
    name2=os.path.basename(firstfile.upper().rstrip('.CSV'))[:4]
    first=False
    if name1=='33':
      #-----------------------------------------------------请修改需要的33分布分档值
      lopmin,lopmax,lopstep=560,620,5
      vf1min,vf1max,vf1step=2.9,3.25,0.05
      vf3min,vf3max,vf3step=1.5,2.5,0.1
      irmin,irmax,irstep=0,1,0.1
    elif name1=="18":
      #-----------------------------------------------------请修改需要的18分布分档值
      lopmin,lopmax,lopstep=88,104,2
      vf1min,vf1max,vf1step=2.9,3.25,0.05
      vf3min,vf3max,vf3step=2.0,2.5,0.1
      irmin,irmax,irstep=0,1,0.1
    elif name1=="20":
      #-----------------------------------------------------请修改需要的20分布分档值
      lopmin,lopmax,lopstep=190,220,1
      vf1min,vf1max,vf1step=3.1,3.55,0.05
      vf3min,vf3max,vf3step=2.0,2.5,0.1
      irmin,irmax,irstep=0,1,0.1
    elif name1=="28":
      #-----------------------------------------------------请修改需要的28分布分档值
      lopmin,lopmax,lopstep=210,250,5
      vf1min,vf1max,vf1step=3.10,3.8,0.05
      vf3min,vf3max,vf3step=1.85,2.5,0.05
      irmin,irmax,irstep=0,0.5,0.05
    elif name1=="40":
      #-----------------------------------------------------请修改需要的40分布分档值
      lopmin,lopmax,lopstep=570,700,10
      vf1min,vf1max,vf1step=2.9,3.3,0.05
      vf3min,vf3max,vf3step=1.5,2.5,0.1
      irmin,irmax,irstep=0,1,0.1
    elif name1=="45":
      #-----------------------------------------------------请修改需要的40分布分档值
      lopmin,lopmax,lopstep=650,750,10
      vf1min,vf1max,vf1step=2.9,3.3,0.05
      vf3min,vf3max,vf3step=1.5,2.5,0.1
      irmin,irmax,irstep=0,1,0.1
    #LOP1分布的参数
    lop1=lopmin
    nlops=int((lopmax-lopmin)/lopstep)+2
    xlop=[0]*nlops
    nlop=[0]*nlops
    #VF1分布的参数
    nvf1s=int((vf1max-vf1min)/vf1step)+2
    xvf1=[0]*nvf1s
    nvf1=[0]*nvf1s
    #VF3分布的参数
    nvf3s=int((vf3max-vf3min)/vf3step)+2
    xvf3=[0]*nvf3s
    nvf3=[0]*nvf3s
    #IR分布的参数
    nirs=int((irmax-irmin)/irstep)+1
    nir=[0]*nirs
    xir=[0]*nirs
    break
#计算分布函数定义
def countx(para,paramin,paramax,parastep):
    if paramin==0:
      num=int((paramax-paramin)/parastep)+1
    else :
      num=int((paramax-paramin)/parastep)+2
    x=[0]*num
    if paramin!=0:
      for i in range(num):
        if i==0:
          x[i]="<{0}".format(round(paramin,2))
        elif i!=num-1:
          x[i]="{0}~{1}".format(round(paramin+parastep*(i-1),2),round(paramin+parastep*i,2))
        else:
          x[i]=">{0}".format(round(paramin+parastep*(i-1),2))
      return x
    else:
      for i in range(num):
        if i!=num-1:
          x[i]="{0}~{1}".format(round(paramin+parastep*(i),2),round(paramin+parastep*(i+1),2))
        else:
          x[i]=">{0}".format(round(paramin+parastep*(i-1),2))
      return x
      
def county(para,paramin,paramax,parastep):
    if paramin==0:
      num=int((paramax-paramin)/parastep)+1
      y=[0]*num
      for i in range(num):
        max1=paramin+(i+1)*parastep
        min1=max1-parastep
        if i!=num-1:
          y[i]=y[i]+df.loc[(df[para]>=min1)&(df[para]<max1)][para].count()
        else:
          y[i] +=df.loc[df[para]>=min1][para].count()
      return y
    else :
      num=int((paramax-paramin)/parastep)+2
      y=[0]*num
      for i in range(num):
        max1=paramin+i*parastep
        min1=max1-parastep
        if i==0:
          y[i]=y[i]+df.loc[df[para]<paramin][para].count()
        elif i!=num-1:
          y[i]=y[i]+df.loc[(df[para]>=min1) & (df[para]<max1)][para].count()
        else:
          y[i] +=df.loc[df[para]>=min1][para].count()
      return y
      
xlop=countx('LOP1',lopmin,lopmax,lopstep) 
xvf1=countx("VF1",vf1min,vf1max,vf1step)
xir=countx('IR',irmin,irmax,irstep)
xvf3=countx('VF3',vf3min,vf3max,vf3step)
for file in glob.glob(os.path.join(path,"{0}*.CSV".format(name1))):
    name=os.path.basename(file.upper().rstrip('.CSV'))
    df=pd.read_csv(file,skiprows=53)                        #读取CSV文件
    colu=df.columns
    n1 = df.TEST.count()
    na +=n1
    # -----------------------计算均值
    avglop=round(np.mean(df.LOP1[df.LOP1>=lopmin]),1)          #计算均值（去坏点）
    avgvf1=round(np.mean(df.VF1[(df.VF1>=2.8)&(df.VF1<=3.3)]),3)          #计算均值（去坏点）
    avgwld=round(np.mean(df.WLD1[(df.WLD1>=440)&(df.WLD1<=470)]),1)          #计算均值（去坏点）
    #计算良率
    vf3yield=round(df.VF3[(df.VF3>=1.5)&(df.VF3<=2.5)].count()/n1*100,2)
    iryield=round(df.IR[(df.IR<=1)].count()/n1*100,2)
    dic1[name]=[name,avglop,avgvf1,avgwld,vf3yield,iryield]
    #分布
    nlop1=county('LOP1',lopmin,lopmax,lopstep)
    nlop=[nlop1[i]+nlop[i] for i in range(nlops)]
    nvf11=county('VF1',vf1min,vf1max,vf1step)
    nvf1=[nvf11[i]+nvf1[i] for i in range(nvf1s)]
    nir1=county('IR',irmin,irmax,irstep)
    nir=[nir1[i]+nir[i] for i in range(nirs)]
    nvf31=county('VF3',vf3min,vf3max,vf3step)
    nvf3=[nvf31[i]+nvf3[i] for i in range(nvf3s)]
      
#输出均值，良率 
aa=list(dic1.values())
out=pd.DataFrame(aa,columns=col)
out.to_csv('C:\\Users\\jianya_liao\\Desktop\\python\\2\\avg.csv')
print('输出：',out)
#输出分布表格       
nlop_p=nlop/na*100
nvf1_p=nvf1/na*100
nir_p=nir/na*100
nvf3_p=nvf3/na*100
#输出图表
mpl.rcParams['font.sans-serif']='SimHei'
mpl.rcParams['xtick.labelsize'] = 20
plt.subplot(221)
for a, b in zip(xlop, nlop_p):  
    b=round(b,1)
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10) 
plt.bar(xlop,nlop_p,color='chocolate',label="比例")
plt.xticks(rotation=45,fontsize='small')
plt.title("LOP分布",fontsize=18)
plt.legend(loc="upper left")

plt.subplot(222)
for a, b in zip(xvf1, nvf1_p):  
    b=round(b,1)
    plt.text(a, b,b, ha='center', va='bottom', fontsize=10) 
plt.bar(xvf1,nvf1_p,color='g',label="比例")

plt.title("VF1分布",fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45,fontsize='small')
plt.ylim(0,55)
plt.ylabel('VF1占比')
#VF3分布画图
plt.subplot(224)
for a, b in zip(xvf3, nvf3_p):
   b=round(b,1)
   plt.text(a, b+0.1, b, ha='center', va='bottom', fontsize=10)
plt.bar(xvf3,nvf3_p,color='R',label="比例")

plt.title("VF3分布",fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45,fontsize='small')
plt.ylim(0,55)
plt.ylabel('VF3占比')

#IR分布画图
plt.subplot(223)
for a, b in zip(xir, nir_p):
   b=round(b,1)
   plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.bar(xir,nir_p,color='m',label="比例")

plt.title("IR分布",fontsize=18)
plt.legend(loc="upper right")
plt.xticks(rotation=45,fontsize='small')
plt.ylim(0,100)

plt.show()
