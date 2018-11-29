# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time


#1. 网页下载
def scrapeweb(appid):
    #1.1构造网址
    url = 'http://mi.talkingdata.com/app/trend/{}.html'.format(appid)
    #1.2下载网页
    response = requests.get(url)
    html = response.text
    #1.3 解析网页
    soup = BeautifulSoup(html,'html.parser')
    tagli = soup.find_all('li',{'class': 'ellipsis trans'})
    tags ='、'.join( [i.get_text() for i in tagli])
    recommend_block = soup.find('div',{'class': 'dataLine-content recommend'})
    recommend_app = recommend_block.find_all('a')
    rec_appid = ';'.join([i['href'].replace('http://mi.talkingdata.com/app/trend/','').replace('.html','') for i in recommend_app])
    rec_appname = ';'.join([i['alt'].replace('-{rankStr}','') for i in recommend_app])
    #1.4 将数据转化为列表字段
    data = [appid, tags,rec_appid,rec_appname]

    return data


#2. 数据存储
def savedata(data):
    with open('data/output/tags.csv','a+', newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(data)


#3. 主程序
def main(appidlist,appidused):
    for appid in appidlist:
        if appid in appidused:
            print('already {}'.format(appid))
            continue
        try:
            savedata(scrapeweb(appid))
        except:
            print('error {}'.format(appid))
            time.sleep(5)
            continue
        print('{} successful download'.format(appid))
        with open('data/output/appidused.txt', 'a+') as f:
            f.write('\n{}\n'.format(appid))
        time.sleep(5)



if __name__ == '__main__':
    with open('data/input/200000.txt', 'r') as f:
        appidlist = [id.replace('\n','') for id in f.readlines()]
    with open('data/output/appidused.txt','r') as f2:
        appidused = [id.replace('\n','') for id in f2.readlines()]

    main(appidlist,appidused)
