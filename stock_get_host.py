# -*- coding: utf-8 -*-
"""
Basic idea of the program:
    Run it daily to get hot stock list according to research reports.
     1. Grab a few webpages from sina stock research website
     2. get stock name and calulate times, and finally sort.

TBD:
    1.Grab content of date of research report.
    2.Send out by email or by wechat
    
@author: Xin Wang
    	 shuilidymail@sina.com
"""
import matplotlib.pyplot as plt
import numpy as np
from os import path
import pandas as pd
import re
import requests
import time
from wordcloud import WordCloud
import sys

sys.path.append("..")
import pub.myutil as m

df = pd.DataFrame()
    
def get_hot_stock_list():
    #web page related settings
    PATTERN = re.compile('<a target="_blank" title="(.*?):')
    BASE_URL = "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/lastest/index.phtml?p="
    MAX_PAGE_NUM = 15
    
    listall = []
    d = pd.DataFrame()
    #open file
    with open('host_stocks.txt','w',encoding='utf-8') as f:
        #loop and get stock data from web page
        for i in range(1, MAX_PAGE_NUM):
            print('Getting page #{}'.format(i))
            r = requests.get(BASE_URL + str(i))
            r.encoding='gb2312'
            data = r.text
            
            p = re.findall(PATTERN, data)
            listall.extend(p)

            time.sleep(0.5)
        
        #get names
        d = pd.DataFrame(listall, columns=['name'])
        d['cnt'] = 1
        
        #calculate times
        gpd = d.groupby(['name']).count().reset_index()
    
        #filter and sort
        stocks = gpd[gpd.cnt>1].sort_values(by='cnt', ascending=False)
        
        #output the result
        print(stocks)
        f.write(stocks.to_string())
        #m.dk(stocks)
    
if __name__ == "__main__":
    get_hot_stock_list()

