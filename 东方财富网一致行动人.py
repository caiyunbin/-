# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:53:47 2019

@author: Caiyunbin
"""

import csv
import requests
from urllib.parse import urlencode
import re
import pymysql
import json
#from multiprocessing import Pool

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSLQ_PASSWORD = 'caiyunbin3344'
MYSQL_PORT = 3306

def get_one_page(page):
    print('正在读取第:%d页'%(page))
    try:
        params ={
                'pageindex':page,
                'pagesize':'50',
                'type':'NSHDDETAIL',
                'orderby':'noticedate',
                'order':'desc',
                }
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                }
        url = 'http://api.dataide.eastmoney.com/data/get_yzxdrindex?'+urlencode(params)
        response =requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
            return None
    except requests.exceptions:
        return None


def parse_json(html):
    js_data = json.loads(html)
    for item in js_data.get('data'):
        yield{
                '股票名称':item.get('securityshortname'),
                '持股比例':item.get('bl'),
                '股东顺序':item.get('concertedgroup'),
                '股票代码':item.get('dim_scode'),
                '股东名称':item.get('sharehdname'),
                '行业':item.get('publishname'),
                '合计数量':item.get('sl'),
                }
    

def save_to_csv(csvf):
    with open('E:\毕业论文\一致行动人.csv','a',encoding = 'utf-8',newline ='') as csvfile:
        fieldnames = ['股票名称','持股比例','股东顺序','股票代码','股东名称','行业','合计数量']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writerow(csvf)

def main(page):
    html = get_one_page(page)
    con = parse_json(html)
    for item in con:
        save_to_csv(item)
       
        
if __name__ =='__main__':
    for page in range(1,62):
        main(page)


