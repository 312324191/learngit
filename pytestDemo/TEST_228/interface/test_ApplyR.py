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
from common_template import CSOST, FOST
from pubilc_methods import Format, files, Authentication, re_json, req_post, Url_Class

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

class testRegistAccount01(unittest.TestCase):
    def setUp(self):
        UC = Url_Class()
        # 拼装URL 调用报文方法
        self.url_Route_P = UC.url_P()
        self.url_Route_V = UC.url_V()
        self.url_Route_ZB = UC.url_ZB()

    def testNormal_001(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 普通票
        # 调用P接口
        global pid, mid, nc, callback
        payload = {'pid': pid, 'mid': mid, "nc": nc, "callback": callback}
        rsp = requests.get(url=self.url_Route_P, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            rsp_0vid = rsp_dict.get("result")[0].get("vid")
            self.assertEqual(rsp_dict.get("code"), 0)
        except Exception as e:
            raise e
                
        # 调用V接口
        payload = {'vid': rsp_0vid, 'nc': nc, "mid": mid, "callback": callback}
        rsp = requests.get(url=self.url_Route_V, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            status_list = [x.get("status") for x in rsp_dict.get("areas")]
            for i in range(len(status_list)):
                if rsp_dict.get("areas")[i].get("status") == 1:
                    # 获取status状态为1的区域ID
                    status_id = rsp_dict.get("areas")[i].get("id")
                    break
            # 获取所有票价信息
            prices = rsp_dict.get("prices")
            logging.debug("prices:%s"%  prices)
        except Exception as e:
            raise e

        # 调用zb接口
        payload = {'vid': rsp_0vid, 'aid': status_id, "nc": nc, "mid": mid, "callback": callback,\
        "type": "ri", "id": "","sid": rsp_0vid, "rid": status_id}
        rsp = requests.get(url=self.url_Route_ZB, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            status_list = [x.get("on_sale") for x in rsp_dict.get("result")]
            for i in range(len(status_list)):
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("symbol_name")== "普通票" and rsp_dict.get("result")[i].get("createOrderDate") is None:
                    # 获取on_sale状态为1的普通区域信息（包括区域id与票价id）
                    tp_type_message = rsp_dict.get("result")[i]
                    break
            # 座位id
            rsp_zb_id = tp_type_message.get("id")
            # 票价id
            rsp_zb_price_id = tp_type_message.get("price_id")
        except Exception as e:
            raise e

        # 票价信息
        for i in prices:
            if i.get('id')==rsp_zb_price_id:
                price = i.get("price")
                price_id = i.get("id")
                break
        # 拼装报文
        # 主办票锁座下单接口
        CSOSTtext = CSOST()
        CSOSTtext["body"]["priceAmount"] = price
        CSOSTtext["body"]["productId"] = pid
        CSOSTtext["body"]["sessionId"]= rsp_0vid
        CSOSTtext["body"]["requirement"][0]["priceId"] = price_id
        CSOSTtext["body"]["requirement"][0]["seatEntry"]["0000"] = [rsp_zb_id]

        rsp = req_post(CSOSTtext)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
        # 获取到云订单号传送给确定订单接口
        rsp_orderNo = rsp.get("body").get("orderNo")

        # 拼装报文
        # 确认订单订单接口
        FOSTtext = FOST()
        FOSTtext["body"]["orderNo"] = rsp_orderNo
        rsp = req_post(FOSTtext)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
    def testNormal_002(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 特殊票== 不是普通票
        # 调用P接口
        global pid, mid, nc, callback
        payload = {'pid': pid, 'mid': mid, "nc": nc, "callback": callback}
        rsp = requests.get(url=self.url_Route_P, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            rsp_0vid = rsp_dict.get("result")[0].get("vid")
            self.assertEqual(rsp_dict.get("code"), 0)
        except Exception as e:
            raise e
                
        # 调用V接口
        payload = {'vid': rsp_0vid, 'nc': nc, "mid": mid, "callback": callback}
        rsp = requests.get(url=self.url_Route_V, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            status_list = [x.get("status") for x in rsp_dict.get("areas")]
            for i in range(len(status_list)):
                if rsp_dict.get("areas")[i].get("status") == 1:
                    # 获取status状态为1的区域ID
                    status_id = rsp_dict.get("areas")[i].get("id")
                    break
            # 获取所有票价信息
            prices = rsp_dict.get("prices")
        except Exception as e:
            raise e

        # 调用zb接口
        payload = {'vid': rsp_0vid, 'aid': status_id, "nc": nc, "mid": mid, "callback": callback,\
        "type": "ri", "id": "","sid": rsp_0vid, "rid": status_id}
        rsp = requests.get(url=self.url_Route_ZB, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            # logging.debug("rsp_dict:%s" % rsp_dict)
            status_list = [x.get("on_sale") for x in rsp_dict.get("result")]
            for i in range(len(status_list)):
                if rsp_dict.get("result")[i].get("on_sale") == 0 and rsp_dict.get("result")[i].get("symbol_name")!= "普通票"and rsp_dict.get("result")[i].get("createOrderDate") is None:
                    # 获取on_sale状态为1的普通区域信息（包括区域id与票价id）
                    tp_type_message = rsp_dict.get("result")[i]
                    logging.debug("区域信息:%s" % tp_type_message)
                    break
            rsp_zb_id = tp_type_message.get("id")
            rsp_zb_price_id = tp_type_message.get("price_id")
        except Exception as e:
            raise e

        # 票价信息
        for i in prices:
            if i.get('id')==rsp_zb_price_id:
                price = i.get("price")
                price_id = i.get("id")
                break
        # 拼装报文
        # 主办票锁座下单接口
        CSOSTtext = CSOST()
        CSOSTtext["body"]["priceAmount"] = price
        CSOSTtext["body"]["productId"] = pid
        CSOSTtext["body"]["sessionId"]= rsp_0vid
        CSOSTtext["body"]["requirement"][0]["priceId"] = price_id
        CSOSTtext["body"]["requirement"][0]["seatEntry"]["1"] = [rsp_zb_id]

        rsp = req_post(CSOSTtext)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
        # 获取到云订单号传送给确定订单接口
        rsp_orderNo = rsp.get("body").get("orderNo")

        # 拼装报文
        # 确认订单订单接口
        FOSTtext = FOST()
        FOSTtext["body"]["orderNo"] = rsp_orderNo
        rsp = req_post(FOSTtext)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
    def testNormal_003(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 套票
        # 调用P接口
        global pid, mid, nc, callback
        payload = {'pid': pid, 'mid': mid, "nc": nc, "callback": callback}
        rsp = requests.get(url=self.url_Route_P, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            rsp_0vid = rsp_dict.get("result")[0].get("vid")
            self.assertEqual(rsp_dict.get("code"), 0)
        except Exception as e:
            raise e
                
        # 调用V接口
        payload = {'vid': rsp_0vid, 'nc': nc, "mid": mid, "callback": callback}
        rsp = requests.get(url=self.url_Route_V, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            status_list = [x.get("status") for x in rsp_dict.get("areas")]
            for i in range(len(status_list)):
                if rsp_dict.get("areas")[i].get("status") == 1:
                    # 获取status状态为1的区域ID
                    status_id = rsp_dict.get("areas")[i].get("id")
                    break
            # 获取区域内票价信息
            prices = rsp_dict.get("prices")
            logging.debug("票价信息:%s" % prices)
            # 获取区域内套票信息
            tp_prices = rsp_dict.get("tplist")
            logging.debug("套票信息:%s" % tp_prices)
        except Exception as e:
            raise e

        # 调用zb接口
        payload = {'vid': rsp_0vid, 'aid': status_id, "nc": nc, "mid": mid, "callback": callback,\
        "type": "ri", "id": "","sid": rsp_0vid, "rid": status_id}
        rsp = requests.get(url=self.url_Route_ZB, params=payload)
        try:
            rsp_str = re_json(rsp.text)
            rsp_dict = json.loads(rsp_str)
            # logging.debug("rsp_dict:%s" % rsp_dict)
            status_list = [x.get("on_sale") for x in rsp_dict.get("result")]
            for i in range(len(status_list)):
                # tp_id ！="0"  暂时默认为套票
                if rsp_dict.get("result")[i].get("tp_id") != "0" and rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("createOrderDate") is None:
                    # 获取on_sale状态为1的普通区域信息（包括区域id与票价id）
                    tp_type_message = rsp_dict.get("result")[i]
                    logging.debug("tp_type_message:%s" % tp_type_message)
                    break
            # rsp_zb_id = tp_type_message.get("id")
            # 固定套根据套票id反向找出所有套票id
            tp_id = tp_type_message.get("tp_id")
            rsp_zb_id = [x for x in rsp_dict.get("result") if x.get("tp_id")==tp_id]
            rsp_zb_id = [x.get("id") for x in rsp_zb_id]
            rsp_zb_price_id = tp_type_message.get("tp_type_id")
            # logging.debug("套票属性id：%s" % rsp_zb_price_id)
        except Exception as e:
            raise e


        # 票价信息
        # if tptype ==0:
        #     for i in prices:
        #         if i.get('id')==rsp_zb_price_id:
        #             price = i.get("price")
        #             price_id = i.get("id")
        #             break
        # elif tptype == 2:
        for i in tp_prices:
            if int(i.get('type_id'))==int(rsp_zb_price_id):
                price = i.get("price")
                price_id = i.get("type_id")
                break

        # for i in tp_prices:

        # 拼装报文
        # 主办票锁座下单接口
        CSOSTtext = CSOST()
        CSOSTtext["body"]["priceAmount"] = price
        CSOSTtext["body"]["productId"] = pid
        CSOSTtext["body"]["sessionId"] = rsp_0vid
        CSOSTtext["body"]["requirement"][0]["priceId"] = price_id
        CSOSTtext["body"]["requirement"][0]["seatEntry"][tp_type_message.get("tp_id")] = rsp_zb_id
        CSOSTtext["body"]["requirement"][0]["type"] = 2
        rsp = req_post(CSOSTtext)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
        # 获取到云订单号传送给确定订单接口
        rsp_orderNo = rsp.get("body").get("orderNo")

        # 拼装报文
        # 确认订单订单接口
        FOSTtext = FOST()
        FOSTtext["body"]["orderNo"] = rsp_orderNo
        rsp = req_post(FOSTtext)
        logging.debug("rsp:%s"% rsp)
        self.assertEqual(rsp.get("head").get("code"), "SUCCESS")
if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(testRegistAccount01("testNormal_002"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()