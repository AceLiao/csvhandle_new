#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2019/5/10 16:02

备注：

"""
import xlrd
path=r'C:\Users\jianya_liao\Desktop\test_package\outdata.xlsx'
file =xlrd.open_workbook(path)
print(file)