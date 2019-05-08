#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/20 10:19
"""
import pandas as pd
import os
import glob

path1 = input("请输入要合档的文件地址：")
# path1="F:\\2018\join"
outsomedata = path1 + "\\123.csv"
# outexcel=path1+"\\合档.xlsx"
# outtemp=path1+"\\temp.csv"
print(outsomedata)
firstfile = True
alldata = []
for file in glob.glob(os.path.join(path1, "*.csv")):
    name = os.path.basename(file.upper().rstrip('.CSV'))
    print(name)
    if firstfile:
        df = pd.read_csv(file, header=52)
        df.insert(0, "Wafer", name)


        columns = df.columns.values
        firstfile = False
        df = df.dropna(axis=1, how='all')
        # print(df.columns)
        # df.to_csv(outtemp)
        x = [15, 16, 17, 18, 19]
        # x=[1,2,3,5,6,7,10,12,13,14,15,16,17,18,19,20,21]
        df.drop(df.columns[x], axis=1, inplace=True)



        minl = int(min(df['PosY']))
        maxl = int(max(df["PosY"]))
        for k in range(minl, (maxl + 1)):
            df[df['PosY']==k]['PosX']
            df_max = max(df[df['PosY']==k]['PosX'])
            df_min = min(df[df['PosY']==k]['PosX'])
            wai_1 = (df['PosX'] - df_min + 1)
            wai_2=df_max-df['PosX']+1
            wai=[0]*len(wai_1)

            for x in range(df.iloc[:0].size):
                if df.loc[x,"PosY"]==k:
                    wai=
                    df.loc[x,"PosX"]=wai

            for i in range(len(wai_1)):
                if wai_1[i]>wai_2[i]:
                    wai[i]=wai_2[i]
                else:
                    wai[i] = wai_1[i]
            print(wai)
            df[df['PosY']==k]['HW1']=wai

        alldata.append(df)
    else:
        df = pd.read_csv(file, skiprows=53)
        df.insert(0, "Wafer", name)
        df = df.dropna(axis='columns', how='all')
        df.drop(df.columns[x], axis=1, inplace=True)

        minl = int(min(df['PosY']))
        maxl = int(max(df["PosY"]))
        for k in range(minl, (maxl + 1)):
            df[df['PosY']==k]['PosX']
            df_max = max(df[df['PosY']==k]['PosX'])
            df_min = min(df[df['PosY']==k]['PosX'])
            wai_1 = (df['PosX'] - df_min + 1)
            wai_2=df_max-df['PosX']+1
            wai=[0]*len(wai_1)
            for i in range(len(wai_1)):
                if wai_1[i]>wai_2[i]:
                    wai[i]=wai_2[i]
                else:
                    wai[i] = wai_1[i]
            print(wai)
            df[df['PosY']==k]['HW1']=wai
        alldata.append(df)
alldata_concat = pd.concat(alldata, axis=0)
alldata_concat.to_csv(outsomedata, index=False)
# a=pd.read_csv(outsomedata)
# a.to_excel(outexcel,sheet_name="data")