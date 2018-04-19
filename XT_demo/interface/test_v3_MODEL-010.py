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
                    "mproduct_id": "PR_0005",
                    "action_type": "order",
                    "packages": [
                        {
                            "package_id": "PK_0034",
                            "discnts": [
                                {
                                    "action_type": "order",
                                    "discnt_id": "PE_0114"
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
            模组产品变更：modify_service_model
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

            template = [
                {
                    "mproduct_id": "PR_0005",
                    "action_type": "keep",
                    "packages": [
                        {
                            "package_id": "PK_0034",
                            "discnts": [
                                {
                                    "action_type": "keep",
                                    "discnt_id": "PE_0114"
                                }
                            ]
                        },
                        {   
                            "package_id": "PK_0048",
                            "discnts": [
                                {
                                    "action_type": "order",
                                    "discnt_id": "PE_0140"
                                }
                            ]
                        }
                    ]
                }
            ]
            # 调用模板方法
            self.change_data, self.change_token, change_service_type, change_service_name = self.rt.modify_service_model(svc_number, imsi, template)
            # logging.debug('This is debug message self.data : %s' % self.data)
            # 拼装URL
            self.change_url = "https://%s:%s/OSN/vop/%s/%s/%s?token=%s" % (ip, host, change_service_type, change_service_name, Edition, self.change_token) 
        except AttributeError:
            print u"请查看转企标识没有找到信息"

    def testNormal_MODEL_010(self):
        json_data = json.dumps(self.data)
        resp = requests.post(url=self.url, data=json_data,verify=False)
        resp_json = resp.json()
        try:
            resp_json.get('data').get('message')
        except AttributeError:
            print json.dumps(resp_json.get('error'), encoding='utf-8', ensure_ascii=False, indent=4)
        else:
            self.assertEqual(resp_json.get(u'data').get(u'status'), True)
            self.assertEqual(resp_json.get(u'data').get(u'message'),'SUCCESS')
        # 一次性查询校验数据
        try:
            vp = Verifying_Point(self.data["timestamp"])
            ServiceOrder = vp.Service_Order(self.data["data"]["order_id"])
            # 竣工需要调用ServiceOrder返回参数用的bss_service_order_no 传入报文竣工方法中
            self.assertEqual(ServiceOrder[0][3], '0')
            self.assertEqual(ServiceOrder[0][4], '13')
            order_data = self.rt.For_Order_Complete_Notify_Ser(ServiceOrder[0][2])
            order_resp = requests.post(url=self.order_url, data=order_data,verify=False)
            ServiceOrder = vp.Service_Order(self.data["data"]["order_id"])
            self.assertEqual(ServiceOrder[0][3], '1')
            self.assertEqual(ServiceOrder[0][4], '13')
            ServiceOrderBack = vp.service_order_back()
            self.assertEqual(ServiceOrderBack[0][0], '22')
            self.assertEqual(ServiceOrderBack[0][1], 'C')
        finally:
            vp.close()
        sleep(60)
        json_data = json.dumps(self.change_data)
        resp = requests.post(url=self.change_url, data=json_data,verify=False)
        resp_json = resp.json()
        self.assertEqual(resp_json.get('error').get('status'), "B-PF-004")
        self.assertEqual(resp_json.get('error').get('message'), u"产品包PK_0048不合法")
if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(testRegistAccount01("testNormal_MODEL_010"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
