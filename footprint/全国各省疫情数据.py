# -*- coding: utf-8 -*-
"""

Created on Tue Apr 21 14:53:39 2020

@author: Administrator
"""

# 全国各省疫情数据
import requests
import pandas as pd
import time
import json

pd.set_option('max_rows', 500)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}  # 设置请求头，伪装为浏览器

url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'  # 定义要访问的地址
r = requests.get(url, headers=headers)  # 使用requests发起请求

data_json = json.loads(r.text)
data = data_json['data']  # 取出json中的数据

url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=420000'  # 定义数据地址
r = requests.get(url, headers=headers)  # 进行请求
data_json = json.loads(r.text)  # 获取json数据


# 将提取数据的方法封装为函数
def get_data(data, info_list):
    info = pd.DataFrame(data)[info_list]  # 主要信息
    today_data = pd.DataFrame([i['today'] for i in data])  # 生成today的数据
    today_data.columns = ['today_' + i for i in today_data.columns]  # 修改列名
    total_data = pd.DataFrame([i['total'] for i in data])  # 生成total的数据
    total_data.columns = ['total_' + i for i in total_data.columns]  # 修改列名
    return pd.concat([info, total_data, today_data], axis=1)  # info、today和total横向合并最终得到汇总的数据


def save_data(data, name):  # 定义保存数据方法
    file_name = name + '_' + time.strftime('%Y_%m_%d', time.localtime(time.time())) + '.csv'
    data.to_csv(file_name, index=None, encoding='utf_8_sig')
    print(file_name + ' 保存成功！')


data_test = get_data(data_json['data']['list'], ['date'])
data_test['name'] = '湖北省'
# print(data_test.head())

data_province = data['areaTree'][2]['children']  # 取出中国各省的实时数据
today_province = get_data(data_province, ['id', 'lastUpdateTime', 'name'])
# print(today_province.head())
# print(today_province[['id', 'name']].head())

# {i: j for i, j in zip(a, b)}
province_dict = {num: name for num, name in zip(today_province['id'], today_province['name'])}
# 查看前五个内容
count = 0
for i in province_dict:
    print(i, province_dict[i])
    count += 1
    if count == 5:
        break

df1 = pd.DataFrame([{'a': 1, 'b': 2, 'c': 3, }, {'a': 111, 'b': 222}])

df2 = pd.DataFrame([{'a': 9, 'b': 8, 'c': 7, }, {'a': 345, 'c': 789}])

df1 = pd.concat([df1, df2], axis=0)

start = time.time()
for province_id in province_dict:  # 遍历各省编号

    try:
        # 按照省编号访问每个省的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + province_id
        r = requests.get(url, headers=headers)
        data_json = json.loads(r.text)

        # 提取各省数据，然后写入各省名称
        province_data = get_data(data_json['data']['list'], ['date'])
        province_data['name'] = province_dict[province_id]

        # 合并数据
        if province_id == '420000':
            alltime_province = province_data
        else:
            alltime_province = pd.concat([alltime_province, province_data])

        print('-' * 20, province_dict[province_id], '成功',
              province_data.shape, alltime_province.shape,
              ',累计耗时:', round(time.time() - start), '-' * 20)

        # 设置延迟等待
        time.sleep(2)

    except:
        print('-' * 20, province_dict[province_id], 'wrong', '-' * 20)

alltime_province.info()
save_data(alltime_province, 'alltime_province')
