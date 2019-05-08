#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/26 13:49
"""
#导入库
import easygui as g
import pandas as pd
import glob
import os
import csv
import json

#gui实现
def get_bin():
    """
    在easygui图形界面中输入单个fenbin的值
    :return: fieldvalues[0] 为不含中文的文件夹地址
              onebin 为亮度，电压，波长等的数字列表
    """
    title="分选"
    fieldnames=["地址",'LOP_min','LOP_max','VF1_min','VF1_max','WLD1_min','WLD1_max','VF3_min','VF3_max',"IR_max",'VZ_min']
    values=["F:\\2018\\for resorting",200,230,3.0,3.3,450,452.5,2,2.5,0.1,19]
    fieldvalues=[]
    fieldvalues=g.multenterbox(msg='请输入规格范围',title=title,fields=fieldnames,values=values)
    onebin=list(map(float,fieldvalues[1:]))
    return fieldvalues[0],onebin
#对bin进行修改
def trans(i,path1,onebin):
    for file in glob.glob(os.path.join(path1,'*.csv')):
        print(file)
        newfile=path1+"\\after\\"+os.path.basename(file)
        df=pd.read_csv(file,header=52)
        df[df['BIN']>i]['BIN']=10

        index_conform=df[(df["LOP1"]>=onebin[0])&(df["LOP1"]<onebin[1])
                         &(df["VF1"]>=onebin[2])&(df["VF1"]<onebin[3])
                         &(df["WLD1"]>=onebin[4])&(df["WLD1"]<onebin[5])
                         &(df["VF3"]>=onebin[6])&(df["VF3"]<onebin[7])
                         &(df["IR"]<onebin[8])
                         &(df["VZ1"]>=onebin[9])].index
        df.loc[index_conform,'BIN']=i+1

        header="F:\\2018\\for resorting\\header\\28ASV27B180821B23W.CSV"
        rows=[json.loads(line) for line in open(header)]
        print(rows)

        with open(newfile,'a',newline="",encoding='utf-8') as openfile:
            writer=csv.writer(openfile)
            line='DataFileName,,"18CSA03P180604A37K.csv"'
            writer.writerows([line])

#导出文件


#main

if __name__ == '__main__':
    path,out=get_bin()

    print(path,out)
    trans(0, path, out)