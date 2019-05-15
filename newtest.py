#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/4/18 9:57

备注：

"""

import pandas as pd
import numpy as np
#
inp = [{'c1':10, 'c2':100}, {'c1':11,'c2':110}, {'c1':12,'c2':120}]
df = pd.DataFrame(inp)
# print(df)
# for index,row in df.iterrows():
#     print(type(row),row['c1'])
#     row['c3']+=1
#     print(row['c3'])

a=[1,2,3,4,5,100,12]
midnum =np.median(a)
mid_df =np.median(df['c2'])
print(df)
print(midnum)
print(mid_df)