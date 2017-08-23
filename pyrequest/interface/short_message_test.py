# -*- coding:utf-8 -*-
__author__ = 'XT'
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, parentdir)
# import test_data
import configparser as cparser
from requests_toolbelt import MultipartEncoder

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)
url = cf.get("short_message", "url")

class AddEventTest(unittest.TestCase):
    """短信发送接口"""
    def setUp(self):
        global url
        global base_dir
        self.base_url = url + "/sms/upload"
        self.data = MultipartEncoder(
        fields={ "fileName": u'短信发送.xlsx', 'sendType': '1', 'sendTime': '', 
        'file': ('d.xlsx', open(base_dir+u'/db_fixture/短信发送.xlsx', 'rb'))})
        self.headers={'Content-Type': self.data.content_type}

    def tearDown(self):
        pass

    def test_normal_01(self):
        ''' 所以参数为空'''
        res = requests.post(url=self.base_url, data=self.data, headers=self.headers)
        res = res.content
if __name__ == '__main__':
    unittest.main()
