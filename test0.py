
import pandas as pd
from os import path
import openp

file1=r'C:\Users\jianya_liao\Desktop\test_package\S066B001H0307002-S99139.csv'
file2=r'C:\Users\jianya_liao\Desktop\test_package\S99139.csv'
outfile = r'C:\Users\jianya_liao\Desktop\test_package\123.xlsx'
f=open(file1)
iron_name = path.basename(file1).rstrip('.csv').split('-')[1]
print(iron_name)
df1 = pd.read_csv(file1,header=None,skiprows=18)
f.close()
df1 =df1[0:14]
df1.dropna(how='all',axis=1,inplace=True)
df1.rename(columns={0:'序号', 1:'Wafer'}, inplace = True)
df1.insert(0,'iron_name',iron_name)
# print(df1.head())
f=open(file2)
df2 = pd.read_csv(f)

df2.insert(0,'iron_name',iron_name)
df2.dropna(how='all',axis=1,inplace=True)
print(df2.head())
f.close()
# alldata=[]
# alldata.append(df1)
# alldata.append(df2)
# out = pd.concat(alldata,axis=1,keys=['iron_name','序号'],join='outer')
# print(out.head())
out=pd.merge(df1,df2)
out.to_excel(outfile,sheet_name='123')
out.to_excel(outfile,sheet_name='1234',startrow=20)