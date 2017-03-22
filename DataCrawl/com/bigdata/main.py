#! coding:utf-8
import requests
import sys
from bs4 import BeautifulSoup
import csv
import urllib
import json
import time,datetime
import re
#from adsl import Adsl
import codecs

def data_Crawling(url):
    s = requests.Session()
    try:
        resp = s.post(url,timeout=60)
        return resp._content
    except requests.exceptions.ReadTimeout:
       print 'requests.exceptions.ReadTimeout'
    except requests.exceptions.ConnectionError:
        print 'requests.exceptions.ConnectionError'
#学校信息提取
def schoolinfos(datas):
    flag = False
    for data in datas:
        if flag == False:#第一行不解析
            flag=True
            continue
        #从第二开始数据抽取
        schooldatas = re.findall(r'<td .*?>(.*?)</td>',str(data),re.S|re.M)
        schooolname = re.findall(r'<a .*?>(.*?)</a>',str(schooldatas[0]),re.S|re.M)[0]
        schooolnameurl = "http://yz.chsi.com.cn"+re.findall(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')',str(schooldatas[0]),re.S|re.M)[0].replace("amp;","")
        address = schooldatas[1]
        schooltype = re.findall(r'<span .*?>(.*?)</span>',str(schooldatas[2]),re.S|re.M)
        if schooldatas[3] == "√":
            yjsy = "是"
        if schooldatas[4] == "√":
            zzline = "是"
        if schooldatas[5] == "√":
            boshidian = "是"
        professes = page(schooolnameurl,2)
        print schooolnameurl
#所属学校专业信息提取
def professes(professes):
    # print professes
    # soup1 = BeautifulSoup(professes.decode('utf-8'), "html.parser")
    # resultdata1 = soup1.find_all("div", id="sch_list")
    # datas1 = re.findall(r'<tr>(.*?)</tr>',str(resultdata1),re.S|re.M)
    flag = False
    for data in professes:
        if flag == False:#第一行不解析
            flag = True
            continue
            #从第二开始数据抽取
            professesinfos = re.findall(r'<td .*?>(.*?)</td>',str(data),re.S|re.M)
            Faculty = professesinfos[0]
            professioncode = professesinfos[1]
            research_direction = professesinfos[2]
            mentor = professesinfos[3]
            enrollednumber = professesinfos[4]
            testinfosurl = "http://yz.chsi.com.cn"+re.findall(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')',str(professesinfos[5]),re.S|re.M)[0].replace("amp;","")
            print testinfosurl

def DataExtraction(datas,type):
    soup = BeautifulSoup(datas.decode('utf-8'), "html.parser")
    resultdata = soup.find_all("div", id="sch_list")
    datas = re.findall(r'<tr>(.*?)</tr>',str(resultdata),re.S|re.M)
    if type == 1:
        schoolinfos(datas)
    if type == 2:
        professes(datas)



#多页翻页
def page(checkurl,type):
    pagecontent = data_Crawling(checkurl)
    pagecount = re.findall(r'<li class="lip" id="page_total">1/(.*?)</li>',pagecontent,re.S|re.M)[0]
    # print pagecount
    for i in range(1,int(pagecount)+1,1):
        url = checkurl+'&pageno='+str(i)
        datas = data_Crawling(url)
        DataExtraction(datas,type)


def main():
    firsturl = 'http://yz.chsi.com.cn/zsml/queryAction.do?ssdm=&mldm=&mlmc=--%E9%80%89%E6%8B%A9%E9%97%A8%E7%B1%BB--&yjxkdm=0808&dwmc=&zymc='
    page(firsturl,1)

if __name__ == '__main__':
    main()