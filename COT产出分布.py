# author:廖建亚
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
#处理文件的路径
path=input("请输入要合档的文件地址：")
col=["Wafer ID","LOP","VF1","WLD","VF3_Yield","IR_Yield"]
lop=pd.DataFrame(columns=col)
na=0
dic1={}

#-----------------------------------------------------请修改需要的分布分档值
lopmin,lopmax,lopstep=90,112,1
vf1min,vf1max,vf1step=2.9,3.35,0.05
vf3min,vf3max,vf3step=1.8,2.5,0.1
irmin,irmax,irstep=0,1,0.1
wldmin,wldmax,wldstep=445,465,2.5
#-------------------------------------------------------------------------
#LOP1分布的参数
lop1=lopmin
nlops=int((lopmax-lopmin)/lopstep)+2
xlop=[]
nlop=[0]*nlops

#wld1分布的参数
wld1=wldmin
nwlds=int((wldmax-wldmin)/wldstep)+2
xwld=[]
nwld=[0]*nwlds
#VF1分布的参数
nvf1s=int((vf1max-vf1min)/vf1step)+2
xvf1=[0]*nvf1s
nvf1=[0]*nvf1s
#VF3分布的参数

nvf3s=int((vf3max-vf3min)/vf3step)+2
xvf3=[0]*nvf3s
nvf3=[0]*nvf3s
#IR分布的参数
irmin=0
irmax=1
irstep=0.1
nirs=int((irmax-irmin)/irstep)+1
nir=[0]*nirs
xir=[0]*nirs
# print(nlop[2])
for file in glob.glob(os.path.join(path,"*.csv")):
    name=os.path.basename(file.upper().rstrip('.CSV'))
    print(name,end='  ')                                            #返回片号
    f=open(file)
    df=pd.read_csv(f,skiprows=53)                        #读取CSV文件
    f.close()
    n1 = df.TEST.count()
    print(n1)
    na +=n1
    # -----------------------计算均值
    avglop=round(np.mean(df.LOP1[df.LOP1>=80]),1)          #计算均值（去坏点）
    avgvf1=round(np.mean(df.VF1[(df.VF1>=2.8)&(df.VF1<=3.8)]),3)          #计算均值（去坏点）
    avgwld=round(np.mean(df.WLD1[(df.WLD1>=440)&(df.WLD1<=470)]),1)          #计算均值（去坏点）
    #计算良率
    vf3yield=round(df.VF3[(df.VF3>=1.5)&(df.VF3<=2.5)].count()/n1*100,2)
    iryield=round(df.IR[(df.IR<=1)].count()/n1*100,2)
    dic1[name]=[name,avglop,avgvf1,avgwld,vf3yield,iryield]
    print(dic1[name])
    #分布
    j=1
    # -----------------------各亮度段的颗粒数
    lop1 = lopmin
    for j in range(nlops):
        if j==0:
            nlop[0]=nlop[0]+df.loc[df.LOP1<lop1].LOP1.count()
        elif j!=nlops-1:
            lop2=lop1+lopstep
            nlop[j] =nlop[j]+df.loc[(df.LOP1>=lop1)&(df.LOP1<lop2)].LOP1.count()
            lop1 +=lopstep
        else:
            nlop[j]=nlop[j]+df.loc[df.LOP1>=lop1].LOP1.count()

    # -----------------------各亮度段的颗粒数
    wld1 = wldmin
    for j in range(nwlds):
        if j == 0:
            nwld[0] = nwld[0] + df.loc[df.WLD1 < wld1].WLD1.count()
        elif j != nwlds - 1:
            wld2 = wld1 + wldstep
            nwld[j] = nwld[j] + df.loc[(df.WLD1 >= wld1) & (df.WLD1 < wld2)].WLD1.count()
            wld1 += wldstep
        else:
            nwld[j] = nwld[j] + df.loc[df.WLD1 >= wld1].WLD1.count()
   
    # -----------------------各VF1段的颗粒数
    vf11=vf1min
    for j in range(nvf1s):
      if j==0:
          nvf1[0]=nvf1[0]+df.loc[df.VF1<vf11].VF1.count()
      elif j!=nvf1s-1:
          vf12=vf11+vf1step
          nvf1[j] =nvf1[j]+df.loc[(df.VF1>=vf11)&(df.VF1<vf12)].VF1.count()
          vf11 +=vf1step
      else:
          nvf1[j]=nvf1[j]+df.loc[df.VF1>=vf11].VF1.count()
    '''
    # -----------------------各IR段的颗粒数
    ir1=irmin
    for j in range(nirs):
      if j!=nirs-1:
          ir2=ir1+irstep
          nir[j] +=df.loc[(df.IR>=ir1)&(df.IR<ir2)].IR.count()
          ir1 +=irstep
      else:
          nir[j]+=df.loc[df.IR>=ir1].IR.count()
    '''
    # -----------------------各VF3段的颗粒数
    vf31=vf3min
    for j in range(nvf3s):
      if j==0:
          nvf3[0]=nvf3[0]+df.loc[df.VF3<vf31].VF3.count()
      elif j!=nvf3s-1:
          vf32=vf31+vf3step
          nvf3[j] =nvf3[j]+df.loc[(df.VF3>=vf31)&(df.VF3<vf32)].VF3.count()
          vf31 +=vf3step
      else:
          nvf3[j]=nvf3[j]+df.loc[df.VF3>=vf31].VF3.count()
# ------------------各亮度段的表示
lop1 = lopmin
for i in range(nlops):
    lop2=lop1+lopstep
    if i==0:
        xlop=xlop+["<{}".format(lop1)]
    elif i!=nlops-1:
        xlop=xlop+["{0}~{1}".format(round(lop1,2),round(lop2,2))]
        lop1 +=lopstep
    else :
        xlop=xlop+["≥{}".format(lop1)]
        
# ------------------各波长段的表示
wld1 = wldmin
for i in range(nwlds):
    wld2=wld1+wldstep
    if i==0:
        xwld=xwld+["<{}".format(wld1)]
    elif i!=nwlds-1:
        xwld=xwld+["{0}~{1}".format(round(wld1,2),round(wld2,2))]
        wld1 +=wldstep
    else :
        xwld=xwld+["≥{}".format(wld1)]



# -------------------各VF1段的表示
vf11=vf1min
for i in range(nvf1s):
    vf12=vf11+vf1step
    if i==0:
        xvf1[i]="<{}".format(vf11)
        vf12=vf11+vf1step
    elif i!=nvf1s-1:
        xvf1[i]="{0}~{1}".format(round(vf11,2),round(vf12,2))
        vf11 +=vf1step
    else :
        xvf1[i]="≥{}".format(round(vf11,2))

# -------------------各IR段的表示
ir1=irmin
for i in range(nirs):
    ir2=ir1+irstep
    if i!=nirs-1:
        xir[i]="{0}~{1}".format(round(ir1,2),round(ir2,2))
        ir1 +=irstep
    else :
        xir[i]="≥{}".format(round(ir1,2))
# -------------------各VF3段的表示
vf31=vf3min
for i in range(nvf3s):
    vf32=vf31+vf3step
    if i==0:
        xvf3[i]="<{}".format(vf31)
        vf32=vf31+vf3step
    elif i!=nvf3s-1:
        xvf3[i]="{0}~{1}".format(round(vf31,2),round(vf32,2))
        vf31 +=vf3step
    else :
        xvf3[i]="≥{}".format(round(vf31,2))
      
#输出均值，良率 
aa=list(dic1.values())
out=pd.DataFrame(aa,columns=col)
print('输出：',out)
#输出分布表格       
print("xlop",xvf1)
print("nlop",nvf1)
nlop_p=nlop/na*100
nwld_p=nwld/na*100
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
ax=plt.bar(xlop,nlop_p,color='chocolate',label="比例")
plt.xticks(rotation=45,fontsize='small')
plt.title("LOP分布",fontsize=18)
plt.legend(loc="upper left")

plt.subplot(223)
for a, b in zip(xvf1, nvf1_p):  
    b=round(b,1)
    plt.text(a, b+0.1, b, ha='center', va='bottom', fontsize=10) 
    
plt.bar(xvf1,nvf1_p,color='g',label="比例")

plt.title("VF1分布",fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45,fontsize='small')
#plt.ylim(0,55)
#plt.ylabel('VF1占比')
#VF3分布画图
plt.subplot(224)
for a, b in zip(xvf3, nvf3_p):  
    b=round(b,1)
    plt.text(a, b+0.1, b, ha='center', va='bottom', fontsize=10) 
    
plt.bar(xvf3,nvf3_p,color='R',label="比例")

plt.title("VF3分布",fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45,fontsize='small')
#plt.ylim(0,55)
#plt.ylabel('VF3占比')

#WLD分布画图
plt.subplot(222)
for a, b in zip(xwld, nwld_p):
    b=round(b,1)
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10) 
    
plt.bar(xwld,nwld_p,color='m',label="比例")

plt.title("WLD分布",fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45,fontsize='small')
#plt.ylim(0,100)

plt.show()