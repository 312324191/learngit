# -*- coding:utf-8 -*-
__author__ = 'XT'
import unittest
import requests
import os, sys, json
parentdir = str(os.path.dirname(os.path.dirname(__file__)))
parentdir =parentdir.replace('\\', '/')
sys.path.append(parentdir+'/db_fixture')
import mysql_assert, test_data

import configparser as cparser
from requests_toolbelt import MultipartEncoder

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)
url = cf.get("short_message", "url")

class AddEventTest(unittest.TestCase):
    # 短信发送
    def setUp(self):
        global url
        global base_dir
        self.url = url + "/sms/upload"
        self.data = MultipartEncoder(
        fields={ "fileName": u'短信发送.xlsx', 'sendType': '1', 'sendTime': '', 
        'file': ('d.xlsx', open(base_dir+u'/db_fixture/短信发送.xlsx', 'rb'))})
        self.headers={'Content-Type': self.data.content_type}
        self.db = mysql_assert.DB()

    def tearDown(self):
        print self.req.content
        self.db.close()

    def test_normal_01(self):
        # 短信正常发送
        self.req = requests.post(url=self.url, data=self.data, headers=self.headers)
        self.rsp = self.req.json()
        self.assertEqual(self.rsp.get("respDesc"), u"执行成功")
        self.assertEqual(self.rsp.get("respCode"), u"0000")
        sql_01 = "select * from `sms_log`"
        sql_rsp = mysql_assert.Select_One(sql_01)

if __name__ == '__main__':
    # 需要调用test_data 初始化需要的数据
    # test_data.del_data(test_data.datas)
    # test_data.init_data(test_data.datas)
    unittest.main()
