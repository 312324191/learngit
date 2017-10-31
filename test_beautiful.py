# -*- coding:utf-8 -*-
__author__ = 'XT'
import urllib 
import requests, sys, re
from bs4 import BeautifulSoup
def req():
    url = "http://tieba.baidu.com/p/2772656630"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    }
    rep = requests.get(url = url, headers = headers)
    return rep.content

def beautiful():
    soup = BeautifulSoup(req())
    # print soup.prettify()
    x = 0
    for so in soup.find_all('img', class_="BDE_Image"):
        image_name = "C:\\1\\%s.jpg" % x
        urllib.urlretrieve(so['src'], image_name)
        x+=1
if __name__ == '__main__':
    beautiful()
