#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

import unittest
import os
import sys
import requests
import json

path=str(os.path.dirname(os.path.dirname(__file__)))
base_dir = path.replace('\\', '/')
file_path = base_dir + "/common_method"
sys.path.append(file_path)
from time import sleep
from common_template import Requsts_template
from pubilc_methods import Verifying_Point, Standard_number

# 导入模组和资源池全量订购关系
from All_mproducts import mproducts, services, mini

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)

ip = cf.get("API_url_Edition", "ip")
host = cf.get("API_url_Edition", "host")
order_host = cf.get("API_url_Edition", "order_host")
Edition = cf.get("API_url_Edition", "Edition")

import logging

class testRegistAccount01(unittest.TestCase):
    def setUp(self):
        try:
            self.rt = Requsts_template()
            # 模组订购样例
            template = [
                {
                    "mproduct_id": "PR_0001",
                    "action_type": "order",
                    "packages": [
                     {
                            "package_id": "PK_0001",
                            "discnts": [
                                {
                                    "discnt_id": "PE_0001",
                                    "action_type": "order"
                                }
                            ]
                        },
                        {
                            "package_id": "PK_0002",
                            "discnts": [
                                {
                                    "discnt_id": "PE_0012",
                                    "action_type": "order"
                                }
                            ]
                        },
                        {
                            "package_id": "PK_0003",
                            "discnts": [
                                {
                                    "discnt_id": "PE_0023",
                                    "action_type": "order"
                                }
                            ]
                        },
                        {
                            "package_id": "PK_0048",
                            "discnts": [
                                {
                                    "discnt_id": "PE_0140",
                                    "action_type": "order"
                                }
                            ]
                        }
                    ]
                }
            ]
            """
            传参数 有效的号码、imsi、iccid
            资源池成卡： basic_service
            资源池白卡： extended_service
            模组成卡： model_product
            模组白卡： blankcard_model_product
            资源池变更：modify_service
            停开机：switch_status
            """
            global ip, Edition, order_host
            # 如果svc_number 是空的话就去查看配置文件中的万号段数据
            svc_number = None
            imsi = "119000000080461"
            iccid = "89860119900000804610"
            if svc_number is None:
                try:
                    Sn =Standard_number()
                    svc_number = int(Sn.Svc_num()[0][0])
                    # 成卡数据
                    # imsi, iccid =  Sn.Im_Icd()[0]
                    # 白卡数据
                    imsi, iccid = Sn.White_Im_Icd()
                finally:
                    Sn.close()
            logging.debug('This is debug message svc_number : %s' % svc_number)
            # 调用模板方法
            self.data, self.token, service_type, service_name = self.rt.blankcard_model_product(svc_number, imsi, iccid, template)
            # logging.debug('This is debug message self.data : %s' % self.data)
            # 拼装URL
            self.url = "https://%s:%s/OSN/vop/%s/%s/%s?token=%s" % (ip, host, service_type, service_name, Edition, self.token)
            self.order_url = "http://%s:%s/OSN/services/VOPForOrderCompleteNotifySer" %(ip, order_host)
        except AttributeError:
            print u"请查看转企标识没有找到信息"

    def testNormal_MODEL_003(self):
        json_data = json.dumps(self.data)
        resp = requests.post(url=self.url, data=json_data,verify=False)
        resp_json = resp.json()
        self.assertEqual(resp_json.get('error').get('status'), "B-PF-004")
        self.assertEqual(resp_json.get('error').get('message'), u"产品包PK_0048不合法")
        
if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(testRegistAccount01("testNormal_MODEL_003"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
