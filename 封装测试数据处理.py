#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/5/5 10:32

备注：
处理 封装前数据
     封装后数据  均值，最大值，最小值，错误值 删除

"""
import pandas as pd
import numpy as np
import os
import glob
# import xlrd
path=r'C:\Users\jianya_liao\Desktop\test_package'


def forward_package_data(file):
    drop_x = [2,3,4,5,13]
    drp_x2=[15,18,'WLP1']
    name = os.path.basename(file)
    iron_name = name.split('-')[1]
    iron_name = iron_name.split('.')[0]
    # print(iron_name)
    f=open(file)
    df =pd.read_csv(f,skiprows=18,header=None)
    f.close()
    df.dropna(how='all', axis=1, inplace=True)
    df.drop(df.columns[drop_x],axis=1,inplace=True)
    df1 = df[0:14]
    df1.insert(0,'Iron_name',iron_name)
    df1.rename(columns={0:'序号',7:'VF1',1:'WaferID',11:'LOP1',12:'WLD1',13:'WLP1',15:'drop1',18:'drop2',9:'IR'},inplace=True)
    df1.drop(['WLP1','drop1','drop2'],axis=1,inplace=True)     #,'drop1','drop2'
    # print('df1:\n',df1.head())

    return df1

def backward_package_data(file):
    iron_name = os.path.basename(file).split('.')[0]
    # print('封装后iron——name:',iron_name)
    iron_name_list.append(iron_name)
    f=open(file)
    df2 = pd.read_csv(f)
    f.close()
    df2.dropna(how='all',axis=1,inplace=True)
    df2 = df2[['序号','编号','IF(mA)','VF(V)','IR(uA)','Φe(mW)']]
    df2.insert(0,'Iron_name',iron_name)
    # print('df2:\n',df2.head())
    return df2
def write_data(f,data):
    pass

alldata1=[]
alldata2=[]
iron_name_list=[]
for file in glob.glob(os.path.join(path,'*.csv')):
    # print(file)
    outfile = path+'\\outdata.xlsx'
    if len(os.path.basename(file))>12:
        df1 = forward_package_data(file)
        alldata1.append(df1)
    else:
        df2 = backward_package_data(file)
        alldata2.append(df2)

alldata1_1 =pd.concat(alldata1,axis=0)
alldata2_2 =pd.concat(alldata2,axis=0)


alldata1_1.to_excel(path+'\df1.xlsx')
alldata2_2.to_excel(path+'\df2.xlsx')
out1 =pd.merge(alldata1_1,alldata2_2)
# print(out1.head())
out1.to_excel(outfile,index=None)
pivot_out1 =out1.pivot_table(index='Iron_name',aggfunc=['mean'])

def average(a):
    out=0
    for i in a:
        out+=i
    return out/len(a)

# print(pivot_out1)
outfile_p = path+'\\pivot.xlsx'
pivot_out1.to_excel(outfile_p)





out2=out1[out1.IR<0.005]
# out2=out2[out2['LOP1'].apply(delete_lop)]
print(path)
print(out2.head())
out2.to_excel(path+'\\deleteIR.xlsx')



for name,group in out2.groupby('Iron_name'):
    print('-'*30)
    print(group)
    print('group2***********************')
    median_lop=np.median(group['Φe(mW)'])

    median_lop=np.median(group['Φe(mW)'])
    def delete_lop(x, median=median_lop):

        return median * 0.992 < x < median * 1.008

    group2=group[group['Φe(mW)'].apply(delete_lop)]
    print(group2)