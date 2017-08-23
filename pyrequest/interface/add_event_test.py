# -*- coding:utf-8 -*-
__author__ = 'XT'
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# print parentdir
sys.path.insert(0, parentdir)
from db_fixture import test_data
class AddEventTest(unittest.TestCase):
    """添加发布会"""
    def setUp(self):
        self.base_url = "http:127.0.0.1:8000/api/add_event/"

    def tearDown(self):
        print self.result

    def test_add_event_all_null(self):
        ''' 所以参数为空'''
        payload = {'eid': '',"limit": '', 'address': '', 'start_time': ''}
        res = requests.post(url=self.url, data=payload)
        self.result = res.json()
        self.assertEqual(self.result["staus"], 10021)
        self.assertEqual(self.result["message"], "parameter error")
if __name__ == '__main__':
    main()
