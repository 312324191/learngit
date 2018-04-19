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
            template = mini
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

    def testNormal_MODEL_001(self):
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
            OrderServiceInst = vp.order_service_inst()
            for i in OrderServiceInst:
                self.assertEqual(i[2], self.data.get("timestamp"))
                self.assertEqual(i[1], 'order')
            list_ZL = ['V0001','V0003','V0004','V0010','V0014','V0017','V0018','V0019','V0023','V0024','V0025']
            self.assertEqual([i[0] for i in OrderServiceInst], list_ZL)
            BssOrderServiceInst = vp.bss_order_service_inst()
            for i in BssOrderServiceInst:
                self.assertEqual(i[5], self.data.get("timestamp"))
                self.assertEqual(i[4], 'A')
            list_SF = ['50000','50001','50003','50004','50006','50007','50008','50011','50015','50020','50021','50022','50100','50101','50102','50103','50105']
            self.assertEqual([i[3] for i in BssOrderServiceInst], list_SF)
            OrderProdSubscribe = vp.order_prod_subscribe()
            self.assertEqual(OrderProdSubscribe[0][0], 'PR_0005')
            self.assertEqual(OrderProdSubscribe[0][1], 'order')
            self.assertEqual(OrderProdSubscribe[0][2], 'VOPI')
            self.assertEqual(OrderProdSubscribe[0][3], self.data.get("timestamp"))
            OrderDiscntSubscribe = vp.order_discnt_subscribe() 
            for i in OrderDiscntSubscribe:
                self.assertEqual(i[0], "order")
                self.assertEqual(i[1], self.data.get("timestamp"))
            list_ZF = ['PE_0035','PE_0036','PE_0037','PE_0038','PE_0039','PE_0040','PE_0041','PE_0042','PE_0043','PE_0044','PE_0112','PE_0114','PE_0116','PE_0117','PE_0118','PE_0119','PE_0120','PE_0121','PE_0122','PE_0124','PE_0125','PE_0126','PE_0127','PE_0128','PE_0129','PE_0130','PE_0131']
            self.assertEqual([i[2] for i in OrderDiscntSubscribe], list_ZF)

            order_data = self.rt.For_Order_Complete_Notify_Ser(ServiceOrder[0][2])
            order_resp = requests.post(url=self.order_url, data=order_data,verify=False)
            ServiceOrder = vp.Service_Order(self.data["data"]["order_id"])
            self.assertEqual(ServiceOrder[0][3], '1')
            self.assertEqual(ServiceOrder[0][4], '13')
            # 订单反馈表
            ServiceOrderBack = vp.service_order_back()
            self.assertEqual(ServiceOrderBack[0][0], '22')
            self.assertEqual(ServiceOrderBack[0][1], 'C')
            # 用户表
            MvnoUser = vp.mvno_user()
            self.assertEqual(MvnoUser[0][1], '2')
            self.assertEqual(MvnoUser[0][2], '1')
            # 用户级别的转售企业指令表
            ServiceInstSubscribe = vp.service_inst_subscribe()
            for i in ServiceInstSubscribe:
                self.assertEqual(i[0], MvnoUser[0][0])
            self.assertEqual([i[4] for i in ServiceInstSubscribe], list_ZL)
            BssInstSubscribe = vp.bss_inst_subscribe()
            for i in BssInstSubscribe:
                self.assertEqual(i[3], MvnoUser[0][0])
            self.assertEqual([i[2] for i in BssInstSubscribe], list_SF)
            ProdSubscribe = vp.prod_subscribe()
            self.assertEqual(ProdSubscribe[0][0], 'PR_0005')
            self.assertEqual(ProdSubscribe[0][1], MvnoUser[0][0])

            DiscntSubscribe = vp.discnt_subscribe()
            self.assertEqual([i[0] for i in DiscntSubscribe], list_ZF)
            InfoUser = vp.Info_User()
            self.assertEqual(InfoUser[0][0], '20991231 235959')
            self.assertEqual(InfoUser[0][1], MvnoUser[0][0])
            self.assertEqual(InfoUser[0][2], '0')
            self.assertEqual(InfoUser[0][3], '1')
            self.assertEqual(InfoUser[0][4], '2')
            PayUserRel = vp.PAY_USER_REL()
            self.assertEqual(PayUserRel[0][0], '0')
            self.assertEqual(PayUserRel[0][1], MvnoUser[0][0])
            self.assertEqual(PayUserRel[0][2], '20990101 000000')
            lifeImsi = vp.life_Imsi()
            self.assertEqual(lifeImsi[0][1], MvnoUser[0][0])
            self.assertEqual(lifeImsi[0][4], "20990101 000000")
            LifeUserProduct = vp.Life_User_Product()
            for i in LifeUserProduct:
                self.assertEqual(i[0], '0')
                self.assertEqual(i[1], MvnoUser[0][0])
            LifeUserProductDisct = vp.LIFE_USER_PRODUCT_DISCT()
            for i in LifeUserProductDisct:
                self.assertEqual(i[0], '0')
                self.assertEqual(i[1], MvnoUser[0][0])
            LifeUserType = vp.Life_User_Type()
            self.assertEqual(LifeUserType[0][0], "2")
            self.assertEqual(LifeUserType[0][1], MvnoUser[0][0])
            self.assertEqual(LifeUserType[0][2], '20990101 000000')

        finally:
            vp.close()
if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(testRegistAccount01("testNormal_MODEL_001"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
