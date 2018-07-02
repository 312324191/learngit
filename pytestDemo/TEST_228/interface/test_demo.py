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
from common_template import CHANGE_TICKET_PHONE
from pubilc_methods import *

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)
pid = cf.get("API_SEAT_FSM", "pid")
mid = cf.get("API_SEAT_FSM", "mid")
nc = cf.get("API_SEAT_FSM", "nc")
callback = cf.get("API_SEAT_FSM", "callback")

def url_228():
    url = Url_Class()
    url_P = url.url_P()
    url_V = url.url_V()
    url_ZB = url.url_ZB()
    url_More = url.url_More()
    global pid, mid, nc, callback
    # rsp_0vid = req_P(url_P, pid, mid, nc, callback)
    # status_id, prices, tp_prices = req_V(url_V, rsp_0vid, nc, mid, callback)
    CHANGE_TICKET_PHONE_text = CHANGE_TICKET_PHONE()

    CHANGE_TICKET_PHONE_text["body"]["oldPhone"]='18701397232'
    CHANGE_TICKET_PHONE_text["body"]["newPhone"]='18701397231'
    CHANGE_TICKET_PHONE_text["body"]["ticketNo"]='P18070200051558098'
    logging.debug("CHANGE_TICKET_PHONE_text:%s" % CHANGE_TICKET_PHONE_text)
    rsp = req_post(CHANGE_TICKET_PHONE_text)
    return rsp
    
if __name__ == '__main__':
    print(url_228())
