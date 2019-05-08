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
import os
import glob
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
    print('df1:\n',df1.head())

    return df1

def backward_package_data(file):
    iron_name = os.path.basename(file).split('.')[0]
    print('封装后iron——name:',iron_name)
    f=open(file)
    df2 = pd.read_csv(f)
    f.close()
    df2.dropna(how='all',axis=1,inplace=True)
    df2 = df2[['序号','编号','IF(mA)','VF(V)','IR(uA)','Φe(mW)']]
    df2.insert(0,'Iron_name',iron_name)
    print('df2:\n',df2.head())
    return df2
def write_data(f,data):
    pass

alldata1=[]
alldata2=[]

for file in glob.glob(os.path.join(path,'*.csv')):
    print(file)
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
print(out1.head())
out1.to_excel(outfile,index=None)
