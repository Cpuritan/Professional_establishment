import os
import numpy as np
import pandas as pd
import pdfplumber

file_dir = 'C:\\Users\\鲍鱼展翅\\Desktop\\resource bank\\professional establishment'  # 也可以改成你自己需要遍历的文件夹，这里用的相对路径
file_list = []
for files in os.walk(file_dir):  # 遍历该文件夹及其里面的所有子文件夹
    for file in files[2]:
        if os.path.splitext(file)[1] == '.pdf' or os.path.splitext(file)[1] == '.PDF' or os.path.splitext(file)[1] == '.xlsx':
            file_list.append(file_dir + '\\' + file)

file_second = file_list[0] # 高校自设二级硕士专业名录
file_second21 = file_list[1] # 高校自设交叉硕士专业名录

# 分析高校自设二级硕士专业
def ABAB(file, professional, level):
    if ".pdf" in file:
        pdf1 = pdfplumber.open(file)
        pages = pdf1.pages
        table_all = []
        for page in pages:  # 遍历pages中每一页的信息
            table = page.extract_tables()
            table_all.append(table)

        table_all = [i for p in table_all for q in p for i in q]
        df_second = pd.DataFrame(table_all[1:], columns=table_all[0])
        df_second.fillna(method='ffill', inplace=True) # 用上一个填补缺失
        df_second = df_second.drop_duplicates()
    elif ".xlsx" in file:
        df_second = pd.read_excel(file,header=2)
        df_second.fillna(method='ffill', inplace=True)  # 用上一个填补缺失

    if level == "211":
        # 提取211院校名单
        name_211 = sum(pd.read_html('t20051223_82762.html')[1].values.tolist(), []) # 利用sum函数合并子列表
        # 筛选211院校自设二级硕士专业
        df_second211 = df_second[df_second["单位名称"].isin(name_211)]

    elif level == "双一流":
        # 双一流
        name_211 = ["北京大学","中国人民大学","清华大学","北京航空航天大学","北京理工大学","中国农业大学","北京师范大学",
                   "中央民族大学","南开大学","天津大学","大连理工大学","吉林大学","哈尔滨工业大学","复旦大学","同济大学",
                   "上海交通大学","华东师范大学","南京大学","东南大学","浙江大学",'中国科学技术大学','厦门大学',"山东大学",
                   "中国海洋大学","武汉大学","华中科技大学","中南大学","中山大学","华南理工大学","四川大学","重庆大学","电子科技大学",
                   "西安交通大学","西北工业大学","兰州大学","国防科技大学","东北大学","郑州大学","湖南大学","云南大学",
                "西北农林科技大学","新疆大学","北京交通大学","北京工业大学","北京科技大学","北京化工大学","北京邮电大学","北京林业大学",
                "北京协和医学院","北京中医药大学","首都师范大学","北京外国语大学","中国传媒大学","中央财经大学","对外经济贸易大学",
                "外交学院","中国人民公安大学","北京体育大学","中央音乐学院","中国音乐学院","中央美术学院","中央戏剧学院","中国政法大学",
                "天津工业大学","天津医科大学","天津中医药大学","华北电力大学","河北工业大学","太原理工大学","内蒙古大学","辽宁大学",
                "大连海事大学","延边大学","东北师范大学",'哈尔滨工程大学',"东北农业大学","东北林业大学","华东理工大学","东华大学",
                "上海海洋大学","上海中医药大学","上海外国语大学","上海财经大学","上海体育学院",'上海音乐学院',"上海大学","苏州大学",
                "南京航空航天大学","南京理工大学","中国矿业大学","南京邮电大学","河海大学","江南大学",'南京林业大学',"南京信息工程大学",
                "南京农业大学","南京中医药大学","中国药科大学","南京师范大学","中国美术学院","安徽大学","合肥工业大学","福州大学",
                "南昌大学","河南大学","中国地质大学","武汉理工大学","华中农业大学","华中师范大学","中南财经政法大学","湖南师范大学",
                "暨南大学","广州中医药大学","华南师范大学","海南大学","广西大学","西南交通大学","西南石油大学","成都理工大学",
                '四川农业大学',"成都中医药大学","西南大学","西南财经大学","贵州大学","西藏大学","西北大学","西安电子科技大学","长安大学",
                "陕西师范大学","青海大学","宁夏大学","石河子大学","中国石油大学",'宁波大学',"中国科学院大学","第二军医大学","第四军医大学"]

        # 筛选211院校自设二级硕士专业
        df_second211 = df_second[df_second["单位名称"].isin(name_211)]

    elif level == "all":
        df_second211 = df_second

    professional1 = '|'.join(professional)
    return df_second211[df_second211.iloc[:,2].str.contains(professional1)]

professional = ["计算机"]

df = ABAB(file_second21, professional, "双一流")




