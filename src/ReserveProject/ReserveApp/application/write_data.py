import os
import csv

path = "C:\\Users\\kei3-\\Desktop\\python\\Management_Application\\ManagementAppEnv\\ManegementAppProject\\ManagementApp\\application\\data.txt"

# htmlからのデータをcsvファイルに記録
def write_csv(data):
    datas = [data]
    with open(path,mode='w', encoding='utf-8') as f:
        f.write(data)
        f.close()
        #writer.writerow(datas)
        
    