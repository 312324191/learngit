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

from common_template import Requsts_template
from pubilc_methods import Verifying_Point, Standard_number

# 导入模组和资源池全量订购关系
from All_mproducts import mproducts, services

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
            template =  [
            {"mproduct_id": "PR_0001",
            "action_type": "order",
            "packages": [
                {"package_id": "PK_0001",
                "discnts": [
                    {"discnt_id": "PE_0001",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0002",
                "discnts": [
                    {"discnt_id": "PE_0012",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0003",
                "discnts": [
                    {"discnt_id": "PE_0023",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0004",
                "discnts": [
                    {"discnt_id": "PE_0028",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0015",
                "discnts": [
                    {"discnt_id": "PE_0070",
                    "action_type": "order"}
                            ]
                }
                        ]
            }
            ]
            # 资源池订购样例
            # [
            #         {"product_id":"V0001", "action_type":"order"},
            #         {"product_id":"V0025", "action_type":"order"},
            #         {"product_id":"V0003", "action_type":"order"}
            #                 ]
            """
            传参数 有效的号码、imsi、iccid
            资源池成卡： basic_service
            资源池白卡： extended_service
            模组成卡： model_product
            模组白卡： blankcard_model_product
            """
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
            self.data, self.token, service_type, service_name = self.rt.blankcard_model_product(svc_number, imsi, iccid, template)
            global ip, Edition, order_host
            self.url = "https://%s:%s/OSN/vop/%s/%s/%s?token=%s" % (ip, host, service_type, service_name, Edition, self.token)
            logging.debug('This is debug message self.data : %s' % self.data)
            logging.debug('This is debug message self.url : %s' % self.url)

            self.order_url = "http://%s:%s/OSN/services/VOPForOrderCompleteNotifySer" %(ip, order_host)
        except AttributeError:
            print u"请查看转企标识没有找到信息"

    def testNormal(self):
        json_data = json.dumps(self.data)
        logging.debug('This is debug message order_id : %s' % self.data["data"]["order_id"])
        resp = requests.post(url=self.url, data=json_data,verify=False)
        logging.debug('This is debug message resp.content : %s' % resp.content)
        resp_json = resp.json()
        self.assertEqual(resp_json.get(u'data').get(u'status'), True) #验证返回结果与仪器是否一致
        self.assertEqual(resp_json.get(u'data').get(u'message'),'SUCCESS')#验证返回结果与仪器是否一致
        # 一次性查询校验数据
        try:
            vp = Verifying_Point(self.data["timestamp"])
            ServiceOrder = vp.Service_Order(self.data["data"]["order_id"])
            # 竣工需要调用ServiceOrder返回参数用的bss_service_order_no 传入报文竣工方法中
            order_data = self.rt.For_Order_Complete_Notify_Ser(ServiceOrder[0][1])
            order_resp = requests.post(url=self.order_url, data=order_data,verify=False)
            logging.debug('This is debug message order_resp.content : %s' % order_resp.content)
            Change_Url = "http://10.124.5.208:8000/OSN/vop/model_product/modify_service_model/v3?token=hcOPBgJ4dB8WBy1V5nrpGaIqaP2INnrhRd0IZ4GflgtCPWsY"
            Change_data = [
            {"mproduct_id": "PR_0001",
            "action_type": "unsubscribe",
            "packages": [
                {"package_id": "PK_0001",
                "discnts": [
                    {"discnt_id": "PE_0001",
                    "action_type": "unsubscribe"}
                            ]
                },
                {"package_id": "PK_0002",
                "discnts": [
                    {"discnt_id": "PE_0012",
                    "action_type": "unsubscribe"}
                            ]
                },
                {"package_id": "PK_0003",
                "discnts": [
                    {"discnt_id": "PE_0023",
                    "action_type": "unsubscribe"}
                            ]
                },
                {"package_id": "PK_0004",
                "discnts": [
                    {"discnt_id": "PE_0028",
                    "action_type": "unsubscribe"}
                            ]
                },
                {"package_id": "PK_0015",
                "discnts": [
                    {"discnt_id": "PE_0070",
                    "action_type": "unsubscribe"}
                            ]
                }
                        ]
            },
            {"mproduct_id": "PR_0001",
            "action_type": "order",
            "packages": [
                {"package_id": "PK_0001",
                "discnts": [
                    {"discnt_id": "PE_0001",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0002",
                "discnts": [
                    {"discnt_id": "PE_0012",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0003",
                "discnts": [
                    {"discnt_id": "PE_0023",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0004",
                "discnts": [
                    {"discnt_id": "PE_0028",
                    "action_type": "order"}
                            ]
                },
                {"package_id": "PK_0015",
                "discnts": [
                    {"discnt_id": "PE_0070",
                    "action_type": "order"}
                            ]
                }
                        ]
            }
            ]
            resp = requests.post(url=Change_Url, data=Change_data,verify=False)
            logging.debug('This is debug message resp.content : %s' % resp.content)
        finally:
            vp.close()
        

if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(testRegistAccount01("testNormal"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
