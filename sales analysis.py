# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:15:30 2017
analysing projector data on Taobao.com
@author: talen
"""
import os,jieba,itertools
import pandas as pd
import collections as cc
jieba.load_userdict('C:/WinPython-64bit-3.6.1.0Qt5/python-3.6.1.amd64/Lib/site-packages/jieba/projectornames.txt')
os.chdir('C:/Users/talen/Desktop/data/')
data = pd.read_excel('淘宝网-商品列表页采集.xlsx')
sales_amount = [int(term[:-3]) for term in data['付款人数']]
data['销量'] = pd.Series(sales_amount)
store_names = data['店铺名称'].unique()
col_prod_names = data['产品名称']
tmp_word_seg = [list(jieba.cut(term)) for term in col_prod_names]
stat_prod_names = cc.Counter(list(itertools.chain.from_iterable(tmp_word_seg)))
stop_words_projector = ['投影仪',' ','投影机','高清','家用','办公','无线','3D','-','微型','手机','1080P','KTV','原装']
tmp1 = ['智能','/','wifi','商务','1080p','迷你','便携','家庭影院','教学','电视','无屏','培训','流明','升级','现货','行货','U盘','全国']
tmp2 = ['安卓','二手','投影','短焦','蓝光','WIFI','WiFi','教育','商用','影院','高','高亮','用','办公会议','替代','高端','电脑','Wifi',\
        '直投','婚庆','全新','4k','1080','720P','激光','4K','led','宽屏','新品','升级版',\
        '送','娱乐','随身','户外','寸','触控','小','幕布','儿童','高亮度','2017',\
        '电视机','接口','大屏','电影','系统','宏基','清','卧室','家用机','好','进口','两用','通用','款',\
        '会议室','移动','内置','特价','日本','互动','带','短','效果','版',\
        'USB','4G','教室']
tmp3 = ['家庭','LED','会议','焦','便携式','超短','3d','机','白天','支持','正品','工程','商务会议','智能手机','全高清','新款','同屏']
symb = ['+','（','）','(',')','【','】']
eng_names = ['Benq','EPSON','BenQ','Epson','BENQ','SONY','sony','Acer',\
             'Rigal','benq','JMGO','SHARP','JmGo','Panasonic','Vivitek','VIVITEK']
stop_words_projector.extend(tmp1)
stop_words_projector.extend(tmp2)
stop_words_projector.extend(tmp3)
stop_words_projector.extend(symb)
stop_words_projector.extend(eng_names)
for term in stop_words_projector:
    del stat_prod_names[term]
for i in list(stat_prod_names.keys()):
    if i.isdigit():
        del stat_prod_names[i]
'''
品牌统计，先统计有多少品牌，每个品牌的销量
'''
brand_list = ['爱普生','明基','索尼','松下','轰天炮','奥图码','坚果','日立',\
              '极米','NEC','光米','瑞格','微麦','优丽','宏碁','夏普','极光',\
              '酷乐视','图美','三洋','优派','美高','神画','澳典','理光','飞利浦',\
              '小帅','丽讯','鸿合','LG','松普','小明','创芝','福满门','冠诺',\
              'Robotgo','奥普达','蒂彤','万德成','优可晟','凯阅','rigal','中宝','优丽可',\
              '汇趣','UKCSIS','THE ONE','VEZ','欧擎','美迅','FINEWELL','l-mix','业王','康佳',\
              '优酷','万播','芒果云','九影','海微','乐佳达','艾洛维','先奇','Touchjet Pond',\
              '爱必酷','富士通','魅乐士']
brand_name_indi = []
brand_sales_indi = []
for brand_ in brand_list:
    data1 = [i for i,e in enumerate(list(data['产品名称'])) if brand_ in e]
    data2 = data.iloc[data1,]
    data3 = sum([int(term[:-3]) for term in data2['付款人数']])
    brand_name_indi.append(brand_)
    brand_sales_indi.append(data3)
brand_sales = list(zip(brand_name_indi,brand_sales_indi))
del brand_name_indi,brand_sales_indi,data1,data2,data3,\
tmp1,tmp2,tmp3,term,brand_,eng_names
brand_sales_sorted = sorted(brand_sales,key = lambda a:a[1],reverse=True)
# calculated ratio of the sales of top n brands in all sales
sales_brands_selected = sum([e for i,e in brand_sales_sorted])
sales_total = data['销量'].sum()
ratio_of_sales = sales_brands_selected / sales_total

'''
extend a list of list 展开列表
方法1
import itertools
b = list(itertools.chain.from_iterable(a))
方法2
b = [term for e in a for term in e]
'''
# 二手销量占比
preowned_index = [i for i,e in enumerate(list(data['产品名称'])) if '二手' in e]
data_preowned = data.loc[preowned_index,]
ratio_of_preowned = data_preowned['销量'].sum()/data['销量'].sum() # 1.425% 占总销量

