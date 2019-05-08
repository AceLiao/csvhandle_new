#encoding:utf-8
"""
@project=csvhandle
@author=jianya_liao
@creat_time=2018/10/19 14:10
"""
import xlwings as xw

wb=xw.Book(r'C:\Users\jianya_liao\Desktop\新建 Microsoft Excel 工作表 (3).xlsx')
sht2=wb.sheets['sheet2']
sht1=wb.sheets['sheet1']
#list1=sht1.value
#print(list1)
list=[[1,2,3],[5,6,7]]
rng=sht2.range('B1:AA33')
rng.value=list
wb.save()