#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/4/16 16:38

备注：

"""
DF_Header={'LOP1':[20,1000],"VF1":[2,5],'HW1':[15,27]}
for i in DF_Header.keys():
    print(i,':',DF_Header[i][0],',',DF_Header[i][1])