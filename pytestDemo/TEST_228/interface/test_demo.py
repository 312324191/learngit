#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

import unittest
import os, logging
import sys
import requests
import json

path=str(os.path.dirname(os.path.dirname(__file__)))
base_dir = path.replace('\\', '/')
file_path = base_dir + "/common_method"
sys.path.append(file_path)
from time import sleep
from common_template import CSOST
from pubilc_methods import *

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)
pid = cf.get("API_SEAT_P", "pid")
mid = cf.get("API_SEAT_P", "mid")
nc = cf.get("API_SEAT_P", "nc")
callback = cf.get("API_SEAT_P", "callback")

def url_228():
    url = Url_Class()
    url_P = url.url_P()
    url_V = url.url_V()
    url_ZB = url.url_ZB()
    url_More = url.url_More()
    global pid, mid, nc, callback
    rsp_0vid = req_P(url_P, pid, mid, nc, callback)
    status_id, prices, tp_prices = req_V(url_V, rsp_0vid, nc, mid, callback)
    Ptype = 2
    rsp_zb_id, rsp_zb_price_id, tp_id = req_ZB(url_ZB, rsp_0vid, status_id, nc, mid, callback,Ptype=Ptype)
    if Ptype==0: prices=prices
    elif Ptype==2: prices=tp_prices
    price, price_id = price_messages(prices, rsp_zb_price_id, Ptype=Ptype)

    CSOSTtext = CSOST()
    CSOSTtext["body"]["priceAmount"] = price
    CSOSTtext["body"]["productId"] = pid
    CSOSTtext["body"]["sessionId"] = rsp_0vid
    CSOSTtext["body"]["requirement"][0]["priceId"] = price_id
    CSOSTtext["body"]["requirement"][0]["seatEntry"][tp_id] = rsp_zb_id
    CSOSTtext["body"]["requirement"][0]["type"] = Ptype
    rsp = req_post(CSOSTtext)
    return rsp
    
if __name__ == '__main__':
    print(url_228())
