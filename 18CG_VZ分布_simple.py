#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/1/24 15:01
"""
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# 处理文件的路径
path = input("请输入要合档的文件地址：")
col = ["Wafer ID", "LOP", "VF1", "WLD", "VF3_Yield", "IR_Yield"]
lop = pd.DataFrame(columns=col)
na = 0
dic1 = {}

# -----------------------------------------------------请修改需要的分布分档值
lopmin, lopmax, lopstep = 87, 104, 1
vf1min, vf1max, vf1step = 2.8, 3.3, 0.1
vf3min, vf3max, vf3step = 1.4, 2.5, 0.1
irmin, irmax, irstep = 0, 1, 0.1
wldmin, wldmax, wldstep = 445, 465, 2.5
vz1min,vz1max,vz1step=19,30,2
# -------------------------------------------------------------------------
# LOP1分布的参数
lop1 = lopmin
nlops = int((lopmax - lopmin) / lopstep) + 2
xlop = []
nlop = [0] * nlops

# wld1分布的参数
wld1 = wldmin
nwlds = int((wldmax - wldmin) / wldstep) + 2
xwld = []
nwld = [0] * nwlds
# VF1分布的参数
nvf1s = int((vf1max - vf1min) / vf1step) + 2
xvf1 = [0] * nvf1s
nvf1 = [0] * nvf1s
# VF3分布的参数

nvf3s = int((vf3max - vf3min) / vf3step) + 2
xvf3 = [0] * nvf3s
nvf3 = [0] * nvf3s

# VZ1分布的参数
nvz1s = int((vz1max - vz1min) / vz1step) + 2
xvz1 = [0] * nvz1s
nvz1 = [0] * nvz1s
# IR分布的参数
irmin = 0
irmax = 1
irstep = 0.1
nirs = int((irmax - irmin) / irstep) + 1
nir = [0] * nirs
xir = [0] * nirs
# print(nlop[2])
number=0
for file in glob.glob(os.path.join(path, "*.csv")):
    number+=1
    print(number)
    name = os.path.basename(file.upper().rstrip('.CSV'))
    # print(name)                                            #返回片号
    df = pd.read_csv(file, skiprows=53)  # 读取CSV文件
    n1 = df.TEST.count()
    na += n1

    # -----------------------各VZ1段的颗粒数
    vz11 = vz1min
    for j in range(nvz1s):
        if j == 0:
            nvz1[0] = nvz1[0] + df.loc[df.VZ1 < vz11].VZ1.count()
        elif j != nvz1s - 1:
            vz12 = vz11 + vz1step
            nvz1[j] = nvz1[j] + df.loc[(df.VZ1 >= vz11) & (df.VZ1 < vz12)].VZ1.count()
            vz11 += vz1step
        else:
            nvz1[j] = nvz1[j] + df.loc[df.VZ1 >= vz11].VZ1.count()

# -------------------各VZ1段的表示
vz11 = vz1min
for i in range(nvz1s):
    vz12 = vz11 + vz1step
    if i == 0:
        xvz1[i] = "<{}".format(vz11)
        vz12 = vz11 + vz1step
    elif i != nvz1s - 1:
        xvz1[i] = "{0}~{1}".format(round(vz11, 2), round(vz12, 2))
        vz11 += vz1step
    else:
        xvz1[i] = "≥{}".format(round(vz11, 2))
# 输出均值，良率
aa = list(dic1.values())
out = pd.DataFrame(aa, columns=col)
print('输出：', out)
# 输出分布表格

nvz1_p = nvz1 / na * 100
# 输出图表
mpl.rcParams['font.sans-serif'] = 'SimHei'
mpl.rcParams['xtick.labelsize'] = 20

# vz1分布画图
plt.subplot()
for a, b in zip(xvz1, nvz1_p):
    b = round(b, 2)
    plt.text(a, b + 0.1, b, ha='center', va='bottom', fontsize=10)

plt.bar(xvz1, nvz1_p, color='R', label="比例")

plt.title("VZ1分布", fontsize=18)
plt.legend(loc="upper left")
plt.xticks(rotation=45, fontsize='small')
# plt.ylim(0,55)
# plt.ylabel('vz1占比')


plt.show()