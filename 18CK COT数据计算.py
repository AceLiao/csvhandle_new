#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/4/16 9:08

备注：

"""
import pandas as pd
import numpy as np
import os
import glob

wafer_yield_column=['LOP','VF1','WLD','VZ','VF3','VF4','HW','LOP良率','VF1良率','WLD良率','VZ良率','IR良率','VF3良率','VF4良率','HW良率','VFD良率','DP良率','BS良率']
wafer_yield_rule={'lop_min':87,'lop_max':1000,#计算良率
                  'vf1_min':2.8,'vf1_max':3.2,
                  'wld_min':445,'wld_max':462.5,
                  'vz_min':19,'vz_max':200,
                  'ir_max':0.2,'ir_min':0,
                  'vf3_min':2,'vf3_max':2.5,
                  'vf4_min':2.48,'vf4_max':2.7,
                  'hw_min':15,'hw_max':27,
                  # 'vfd_max':0.06,
                  # 'dp_max':10,
                  # 'bs_max':4,
              'rmlop_min':20,#计算均值
              'rmvf1_min':2,'rmvf1_max':5,
              'rmwld_min':430,'rmwld_max':480,
              'rmvz_min':10,
              'rmvf3_min':1,'rmvf3_max':4,
              'rmvf4_min':2,'rmvf4_max':4.5,
              'rmhw_min':5,'rmhw_max':50,
              }
def bad_remove(a,min=wafer_yield_rule['lop_min'],max=wafer_yield_rule['lop_max']):
    return min<=a<=max
def wafer_yield(waferid,df):
    # print('columns',df.columns)
    test_num=df.loc[:,'TEST'].count() #测试数量test_num
    # print('test_num',test_num)
    avgvf1 = round(np.mean(df.VF1[(df.VF1 >= wafer_yield_rule['rmvf1_min']) & (df.VF1 <= wafer_yield_rule['rmvf1_max'])]), 3)
    avglop = round(np.mean(df.LOP1[(df.LOP1 >= wafer_yield_rule['rmlop_min'])]), 2)
    avgvf3 = round(np.mean(df.VF3[(df.VF3 >= wafer_yield_rule['rmvf3_min']) & (df.VF3 <= wafer_yield_rule['rmvf3_max'])]), 3)
    avgvf4 = round(np.mean(df.VF4[(df.VF4 >= wafer_yield_rule['rmvf4_min']) & (df.VF4 <= wafer_yield_rule['rmvf4_max'])]), 3)
    avgwld = round(np.mean(df.WLD1[(df.WLD1 >= wafer_yield_rule['rmwld_min']) & (df.WLD1 <= wafer_yield_rule['rmwld_max'])]),2)
    avgvz  = round(np.mean(df.VZ1[(df.VZ1 >= wafer_yield_rule['rmvz_min'])]), 1)
    avghw = round(np.mean(df.HW1[(df.HW1>= wafer_yield_rule['rmhw_min']) & (df.HW1 <= wafer_yield_rule['rmhw_max'])]), 1)
    yieldvf1=round((df.VF1[(df.VF1 >= wafer_yield_rule['vf1_min']) & (df.VF1 <= wafer_yield_rule['vf1_max'])].count()/test_num),3)
    yieldvf3=round((df.VF3[(df.VF3 >= wafer_yield_rule['vf3_min']) & (df.VF3 <= wafer_yield_rule['vf3_max'])].count()/test_num),3)
    yieldvf4=round((df.VF4[(df.VF4 >= wafer_yield_rule['vf4_min']) & (df.VF4 <= wafer_yield_rule['vf4_max'])].count()/test_num),3)
    yieldir=round((df.IR[ (df.IR <= wafer_yield_rule['ir_max'])].count()/test_num),3)
    yieldwld=round((df.WLD1[(df.WLD1 >= wafer_yield_rule['wld_min']) & (df.WLD1 <= wafer_yield_rule['wld_max'])].count()/test_num),3)
    yieldhw=round((df.HW1[(df.HW1 >= wafer_yield_rule['hw_min']) & (df.HW1 <= wafer_yield_rule['hw_max'])].count()/test_num),3)
    yieldlop=round((df.LOP1[(df.LOP1 >= wafer_yield_rule['lop_min'])].count()/test_num),3)
    yieldvz=round((df.VZ1[(df.VZ1 >= wafer_yield_rule['vz_min'])].count()/test_num),3)
    LOP_yield=round(df.loc[df.LOP1.apply(bad_remove,(wafer_yield_rule['lop_min'],wafer_yield_rule['lop_max']))].LOP1.count()/test_num,3)
    print('LOP_yield:',LOP_yield)
    # totalyield=round((df.VF1[(df.VF1 >= wafer_yield_rule['vf1_min']) & (df.VF1 <= wafer_yield_rule['vf1_max'])&(df.VF3[(df.VF3 >= wafer_yield_rule['vf3_min']) & (df.VF3 <= wafer_yield_rule['vf3_max'])&(df.VF4[(df.VF4 >= wafer_yield_rule['vf4_min']) &
    #                         (df.VF4 <= wafer_yield_rule['vf4_max'])&(df.IR[ (df.IR <= wafer_yield_rule['ir_max'])&(df.WLD1[(df.WLD1 >= wafer_yield_rule['wld_min']) & (df.WLD1 <= wafer_yield_rule['wld_max'])&(df.HW1[(df.HW1 >= wafer_yield_rule['hw_min']) &
    #                        (df.HW1 <= wafer_yield_rule['hw_max']&(df.LOP1[(df.LOP1 >= wafer_yield_rule['lop_min'])&(df.VZ1[(df.VZ1 >= wafer_yield_rule['vz_min'])]].count()/test_num),3)
    dic1={'LOP':avglop,'VF1':avgvf1,'WLD':avgwld,'VF3':avgvf3,'VF4':avgvf4,'VZ':avgvz,'HW':avghw,'测试数量':test_num,
          'VF1良率':yieldvf1,'LOP良率':yieldlop,'WLD良率':yieldwld,'IR良率':yieldir,'VF3良率':yieldvf3,'VF4良率':yieldvf4,'VZ良率':yieldvz,'HW良率':yieldhw}
    df1=pd.DataFrame(dic1,index=[waferid])
    return df1

if __name__ == '__main__':
    average_df=pd.DataFrame()
    path=input("请输入文件夹地址：")
    for file in glob.glob(os.path.join(path,"*.csv")):
        name=os.path.basename(file.upper().rstrip('.CSV'))
        #  表头读取csv
        # f=open(file)
        # header=pd.read_csv(f,nrows=13,header=None)
        # f.close()
        # test_machine=header.iloc[3,2]
        # test_machine=header.loc[3,2]
        # print(test_machine)
        f=open(file)
        df=pd.read_csv(file,skiprows=53)
        f.close()
        df=df.dropna(axis=1)
        df1=wafer_yield(name,df)
        average_df=average_df.append(df1)
    print(average_df)
    # print(header)
    outfile=path+"\\COT统计.xlsx"
    average_df.to_excel(outfile,sheet_name="良率&均值")
    print('良率与均值数据已经写入：',outfile)