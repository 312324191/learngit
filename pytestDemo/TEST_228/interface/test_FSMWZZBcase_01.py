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
from common_template import CPOST, FOST
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
        # Ptype：1自由套 2组合套 0普通票 4特殊票
        # 无座只有自由套与普通票
        # Ptype = 0
        # global pid, mid, nc, callback
        # rsp_0vid = req_P(self.url_Route_P, pid, mid, nc, callback)
        # # 调用V接口
        # status_id, prices, tp_prices = req_V(self.url_Route_V, rsp_0vid, nc, mid, callback)

        # # 暂时仅取第一个套票信息:
        # num = tp_prices[0].get("num")
        # price_id = tp_prices[0].get("price_id")
        # rsp_zb_id, rsp_zb_price_id, tp_id = req_ZB(self.url_Route_ZB, rsp_0vid, status_id, nc, mid, callback,Ptype=Ptype, num=num, price_id=price_id)
        # self.assertIsNotNone(rsp_zb_id)
        # self.assertIsNotNone(rsp_zb_price_id)
        # self.assertIsNotNone(tp_id)
        # if Ptype==0 or Ptype==4: 
        #     prices=prices
        #     Ptype = 0
        # elif Ptype==2: 
        #     prices=tp_prices
        # elif Ptype==1:
        #     prices=tp_prices
        #     rsp_zb_price_id = price_id
        # price, price_id = price_messages(prices, rsp_zb_price_id, Ptype=Ptype)
        b_product_session_price = sql_b_product_session_price(0, pid)
        logging.debug("b_product_session_price:%s" % b_product_session_price) 
        CPOSTtext = CPOST()
        # 默认tickettype为1  1：纸质票  2：电子票
        # CSOSTtext["body"]["ticketType"] = 2
        del CPOSTtext["body"]['mchntOrderNo']
        del CPOSTtext["body"]['priceRealIDMap']
        CPOSTtext["body"]["priceAmount"] = int(b_product_session_price["price"])
        CPOSTtext["body"]["productId"] = b_product_session_price["product_id"] 
        CPOSTtext["body"]["sessionId"] = b_product_session_price["product_session_id"] 
        CPOSTtext["body"]["requirement"][0]["priceId"] = b_product_session_price["price_id"] 
        # del CPOSTtext["body"]["seatRealIDMap"]
        rsp = req_post(CPOSTtext)
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

    def testNormal_004(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 自由套 （同相同价格套票）
        # 调用P接口
        # Ptype：1自由套 2组合套 0普通票 4特殊票
        # 无座只有自由套与普通票
        # Ptype = 1
        # global pid, mid, nc, callback

        # rsp_0vid = req_P(self.url_Route_P, pid, mid, nc, callback)
        # # 调用V接口
        # status_id, prices, tp_prices = req_V(self.url_Route_V, rsp_0vid, nc, mid, callback)

        # # 暂时仅取第一个套票信息:
        # num = tp_prices[0].get("num")
        # price_id = tp_prices[0].get("price_id")
        # rsp_zb_id, rsp_zb_price_id, tp_id = req_ZB(self.url_Route_ZB, rsp_0vid, status_id, nc, mid, callback,Ptype=Ptype, num=num, price_id=price_id)
        # self.assertIsNotNone(rsp_zb_id)
        # self.assertIsNotNone(rsp_zb_price_id)
        # self.assertIsNotNone(tp_id)
        # if Ptype==0 or Ptype==4: 
        #     prices=prices
        #     Ptype = 0
        # elif Ptype == 2: 
        #     prices = tp_prices
        # elif Ptype == 1:
        #     prices = tp_prices
        #     rsp_zb_price_id = price_id
        # price, price_id = price_messages(prices, rsp_zb_price_id, Ptype=Ptype)
        b_product_session_price = sql_b_product_session_price(1, pid)
        logging.debug("b_product_session_price:%s" % b_product_session_price)       
        CPOSTtext = CPOST()
        del CPOSTtext["body"]['mchntOrderNo']
        del CPOSTtext["body"]['priceRealIDMap']
        CPOSTtext["body"]["priceAmount"] = int(b_product_session_price["price"])
        CPOSTtext["body"]["productId"] = b_product_session_price["product_id"] 
        CPOSTtext["body"]["sessionId"] = b_product_session_price["product_session_id"] 
        CPOSTtext["body"]["requirement"][0]["priceId"] = b_product_session_price["price_id"] 
        # del CSOSTtext["body"]["seatRealIDMap"]
        logging.debug("CPOSTtext:%s" % CPOSTtext)
        rsp = req_post(CPOSTtext)
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

    def testNormal_005(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 普通票
        # 调用P接口
        # Ptype：1自由套 2组合套 0普通票 4特殊票
        # Ptype = 0
        # global pid, mid, nc, callback
        # rsp_0vid = req_P(self.url_Route_P, pid, mid, nc, callback)
        # # 调用V接口
        # status_id, prices, tp_prices = req_V(self.url_Route_V, rsp_0vid, nc, mid, callback)

        # # 暂时仅取第一个套票信息:
        # num = tp_prices[0].get("num")
        # price_id = tp_prices[0].get("price_id")
        # rsp_zb_id, rsp_zb_price_id, tp_id = req_ZB(self.url_Route_ZB, rsp_0vid, status_id, nc, mid, callback,Ptype=Ptype, num=num, price_id=price_id)
        # self.assertIsNotNone(rsp_zb_id)
        # self.assertIsNotNone(rsp_zb_price_id)
        # self.assertIsNotNone(tp_id)
        # if Ptype==0 or Ptype==4: 
        #     prices=prices
        #     Ptype = 0
        # elif Ptype==2: 
        #     prices=tp_prices
        # elif Ptype==1:
        #     prices=tp_prices
        #     rsp_zb_price_id = price_id
        # price, price_id = price_messages(prices, rsp_zb_price_id, Ptype=Ptype)

        b_product_session_price = sql_b_product_session_price(0, pid)
        logging.debug("b_product_session_price:%s" % b_product_session_price) 
        CPOSTtext = CPOST()
        # 默认tickettype为1  1：纸质票  2：电子票
        CSOSTtext["body"]["ticketType"] = 2
        del CPOSTtext["body"]['mchntOrderNo']
        del CPOSTtext["body"]['priceRealIDMap']
        CPOSTtext["body"]["priceAmount"] = int(b_product_session_price["price"])
        CPOSTtext["body"]["productId"] = b_product_session_price["product_id"] 
        CPOSTtext["body"]["sessionId"] = b_product_session_price["product_session_id"] 
        CPOSTtext["body"]["requirement"][0]["priceId"] = b_product_session_price["price_id"]
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

    def testNormal_008(self):
        """
        调用P接口获取vid 作为V接口参数vid参数 
        获取V接口中票价全部信息与区域id信息
        调用ZP接口用vid与区域id修改参数  获取想要的座位id与票价id
        根据票价id获取票价 根据座位id与票价核算总价
        """
        # pid：商品id， mid：商户角色id，vid：场次id，prices：票价信息列表，prices_id：票价id
        # 自由套 （同相同价格套票）
        # 调用P接口
        # Ptype：1自由套 2组合套 0普通票 4特殊票
        # Ptype = 1
        # global pid, mid, nc, callback

        # rsp_0vid = req_P(self.url_Route_P, pid, mid, nc, callback)
        # # 调用V接口
        # status_id, prices, tp_prices = req_V(self.url_Route_V, rsp_0vid, nc, mid, callback)

        # # 暂时仅取第一个套票信息:
        # num = tp_prices[0].get("num")
        # price_id = tp_prices[0].get("price_id")
        # rsp_zb_id, rsp_zb_price_id, tp_id = req_ZB(self.url_Route_ZB, rsp_0vid, status_id, nc, mid, callback,Ptype=Ptype, num=num, price_id=price_id)
        # self.assertIsNotNone(rsp_zb_id)
        # self.assertIsNotNone(rsp_zb_price_id)
        # self.assertIsNotNone(tp_id)
        # if Ptype==0 or Ptype==4: 
        #     prices=prices
        #     Ptype = 0
        # elif Ptype == 2: 
        #     prices = tp_prices
        # elif Ptype == 1:
        #     prices = tp_prices
        #     rsp_zb_price_id = price_id
        # price, price_id = price_messages(prices, rsp_zb_price_id, Ptype=Ptype)

        b_product_session_price = sql_b_product_session_price(1, pid)
        logging.debug("b_product_session_price:%s" % b_product_session_price)       
        CPOSTtext = CPOST()
        # 默认tickettype为1  1：纸质票  2：电子票
        CSOSTtext["body"]["ticketType"] = 2
        del CPOSTtext["body"]['mchntOrderNo']
        del CPOSTtext["body"]['priceRealIDMap']
        CPOSTtext["body"]["priceAmount"] = int(b_product_session_price["price"])
        CPOSTtext["body"]["productId"] = b_product_session_price["product_id"] 
        CPOSTtext["body"]["sessionId"] = b_product_session_price["product_session_id"] 
        CPOSTtext["body"]["requirement"][0]["priceId"] = b_product_session_price["price_id"] 
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
    suite.addTest(testRegistAccount01("testNormal_004"))  # 按用例执行
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()