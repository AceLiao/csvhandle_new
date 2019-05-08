#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/12 16:25
"""
from tkinter import *
import tkinter.filedialog
import pandas as pd
import matplotlib.pyplot as plt
import os

# 弹出对话框，选择需要的文件，关闭后继续执行
root = Tk()
filename=''
def xz():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    print(filename)
    if filename != '':
        lb.config(text = "您选择的文件是："+filename);
        return filename
    else:
        lb.config(text = "您没有选择任何文件");

lb = Label(root,text = '')
lb.pack()
btn = Button(root,text="弹出选择文件对话框",command=xz)
btn.pack()
root.mainloop()

#判断产品型号，判断文件格式是否正确，并非必须


#文件名拆分；读取数据
file=os.path.basename(filename)
print(file)
df=pd.read_csv(filename,skiprows=53)
x=max(df['PosX'])-min(df["PosX"])+1
y=max(df['PosY'])-min(df["PosY"])+1
print(x,y)
df2=pd.DataFrame(0,index=range(0,x),columns=range(0,y))

print(df2.shape)
#数据按照坐标，并绘二维图

lopmin,lopmax,lopstep=200,240,5
vf1min,vf1max,vf1step=2.9,3.25,0.05
wldmin,wldmax,wldstep=1.5,2.5,0.1
irmin,irmax,irstep=0,1,0.1

line=df['TEST'].count()
print("line:",line)
print("max&min PosX",max(df['PosX']),min(df['PosX']))
print(int(int(df.loc[0,'PosX']))-min(df['PosX']))
print((int(df.loc[0,'PosY'])-min(df['PosY'])))
print(df.loc[12563,'LOP1'])

for i in range(line):
    #print(i)
    df2.iloc[int(int(df.loc[i,'PosX'])-min(df['PosX'])),(int(df.loc[i,'PosY'])-min(df['PosY']))]=df.loc[i,'LOP1']
print(df2)
"""
num_lop=(lopmax-lopmin)/lopstep
n_lop=[]
for i in range(num_lop+2):
    if i ==0:
        n_lop.append("<{0}".format(lopmin))
    elif i<num_lop-1:
        n_lop.append("")

df = DataFrame(np.random.randn(10,10))
fig = plt.figure(figsize=(12,5))
ax = fig.add_subplot(111)
axim = ax.imshow(df.values,interpolation='nearest')#cmap=plt.cm.gray_r, #cmap用来显示颜色，可以另行设置
plt.colorbar(axim)
plt.show()
"""
fig=plt.figure(figsize=(12,5))
ax=fig.add_subplot(111)
axim=ax.imshow(df2.values,interpolation='nearest')
plt.colorbar(axim)
plt.show()