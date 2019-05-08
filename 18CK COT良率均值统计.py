#encoding:utf-8
# 1118CK COT统计均值，良率，

"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/9/17 11:09
"""
import pandas as pd
import numpy as np
import os
import glob

out_columns=['LOP1','VF1','WLD1','VZ1','VF3','VF4','HW1','LOP1良率','VF1良率','WLD1良率','VZ1良率','IR良率','VF3良率','VF4良率','HW1良率','测试颗数','好晶','R仓数']
DF_Average={'VF1':[2,5],'LOP1':[20,200],'WLD1':[430,480],'VZ1':[10,200],'VF3':[1,4],'VF4':[2,4.5],'HW1':[5,50]}                                   # 计算均值
DF_Yield={'VF1':[2.8,3.2],'LOP1':[87,200],'WLD1':[445,462.5],'IR':[0,0.2],'VZ1':[19,200],'VF3':[2,2.5],'VF4':[2.48,2.7],'HW1':[15,27]}           # 计算良率
R_Yield={'VF1':[2.6,3.8],'LOP1':[50,200],'WLD1':[435,475],'IR':[0,1]}                                                                               # R仓数计算

if __name__ == '__main__':
    out_df=pd.DataFrame()
    path=input("请输入文件夹地址：")
    file_number=0
    for file in glob.glob(os.path.join(path,"*.csv")):
        file_number+=1
        print(file_number)
        name=os.path.basename(file.upper().rstrip('.CSV')) # name 为CSV文件名,小写转大写
        f=open(file)                                        # 可以打开含有中文目录的地址
        df=pd.read_csv(f,skiprows=53)
        f.close()
        df=df.dropna(axis=1)
        test_num=df['TEST'].count()
        # 单项均值计算
        # 单项良率计算
        dic={"测试颗数":test_num}
        good_df = df.copy()
        for i in df.columns:
            if i in DF_Yield.keys():
                good_df=good_df.loc[df[i].apply(lambda a:DF_Yield[i][0]<=a<=DF_Yield[i][1])]
                item_yield=round((df.loc[df[i].apply(lambda a:DF_Yield[i][0]<=a<=DF_Yield[i][1])][i].count()/test_num),3)
                dic[i+'良率']=item_yield
            if i in DF_Average.keys():
                item_average=round(np.mean(df.loc[df[i].apply(lambda a:DF_Average[i][0]<=a<=DF_Average[i][1])][i]),3)
                dic[i]=item_average
    #not_good_df
        not_good_df=df.append(good_df)
        not_good_df.drop_duplicates(keep=False,inplace=True)
        R_df=not_good_df.copy()
        for i in R_Yield.keys():
            R_df=R_df.loc[R_df[i].apply(lambda a:R_Yield[i][0]<=a<=R_Yield[i][1])]
        # print("not-good-df数量：",not_good_df['TEST'].count())
        dic['好晶'] = good_df['TEST'].count()
        dic['R仓数']=R_df['TEST'].count()
        df1 = pd.DataFrame(dic, index=[name], columns=out_columns)
        out_df = out_df.append(df1)

    print(out_df)
    outfile=path+"\\COT统计.xlsx"
    out_df.to_excel(outfile,sheet_name="良率&均值")
    print('良率与均值数据已经写入：',outfile)