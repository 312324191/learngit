#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WJH'

import requests
import json
import unittest
import sys
import os
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)
from common import common_optMysql
from IOT_API_TestCases import envVariables
class qryCustomerBills(unittest.TestCase):
    def setUp(self):
        self.url = envVariables.host+"/proxy/qryCustomerBills"                 #地址
        self.data = {
        "billingCustomerId":"3",                                               #企业ID
        "accountPeriodId": "20170527"                                          #账期
        }

    def tesrDown(self):
    	pass
    def testNormal_001(self):
        self.data = json.dumps(self.data)                                      #转换为json格式
        res = requests.post(url = self.url, data = self.data)                  #发送post请求
        res_json = res.json()
        self.assertEqual(res_json.get("respCode"), "0000")                     #断言
        self.assertEqual(res_json.get("respDesc"), "success")                  #断言
        data = json.loads(self.data)                                           #转换data为字典
        sql = """SELECT 
            b.account_Period_Mark, 
            c.customer_name,
            f.final_amount/1000
            FROM 
            billing.account_period b, 
            billing.bill_customer c,
            billing.customer_bill f, 
            billing.customer_ccount_period a
            WHERE 
            a.account_period_id = b.account_period_id
            AND c.billing_customer_id = a.billing_customer_id
            AND f.consumer_ccount_period_id = a.customer_ccount_period_id
            and c.billing_customer_id = %s
            AND a.account_period_id = %s""" % (data.get("billingCustomerId"), data.get("accountPeriodId")) 
            #获取账期表（account_period）账期、出账客户表（bill_customer）企业名称、客户账单表（customer_bill）总费用
            
        sql1 = common_optMysql.GetDatas_QueryDB(sql)                            #获取sql全部数据
        sql_01 = []                                                             #定义一个列表
        for i in sql1:                                                          #获取sql1里的数据                                                              
            sql_01.append(i[0])                                                 #循环放入list_01里
            sql_01.append(i[1])
            sql_01.append(float(i[2]))                                          #转换flost类型放入列表
        #tup = tuple(sql_01)
        self.assertEqual(len(res_json.get("customerBills")), len(sql1))         #断言返回数据与数据库数据长度是否一致
        list_01 = []                                                            #定义一个列表
        for i in res_json.get("customerBills"):                                 #获取返回customerBills里的数据
            list_01.append(i.get("accountPeriodMark"))                          #循环放入list_01里
            list_01.append(i.get("customerName"))
            list_01.append(i.get("finalAmount"))
        sql_01.sort()                                                           #排序
        list_01.sort()                                                          #排序
        self.assertEqual(sql_01,list_01)                                        #断言俩列表的值

    def testError_002(self):
        del self.data["accountPeriodId"]                                        #删除键
        self.data = json.dumps(self.data)                                       #转换为json格式
        res = requests.post(url = self.url, data = self.data)                   #发送post请求
        res_json = res.json()                                                   #将获取结果转换json格式
        self.assertEqual(res_json.get("respCode"), "C0001")                     #断言
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法|账期不能为空") #断言
        self.assertEqual(res_json.get("totalAmount"),0.0)                       #断言
        self.assertEqual(res_json.get("customerBills"),None)                    #断言

    def testError_003(self):
        del self.data["billingCustomerId"]                                      #删除键
        self.data = json.dumps(self.data)                                       #转换为json格式
        res = requests.post(url = self.url, data = self.data)                   #发送post请求
        res_json = res.json()                                                   #转换json格式
        self.assertEqual(res_json.get("respCode"), "C0002")                      #断言
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法（关联权限）|客户不能为空")
        self.assertEqual(res_json.get("totalAmount"), 0.0)
        self.assertEqual(res_json.get("customerBills"), None)                   #断言

    def testError_004(self):
        del self.data["accountPeriodId"]                                        #删除键
        del self.data["billingCustomerId"]                                      #删除键
        self.data = json.dumps(self.data)                                       #转换为json格式
        res = requests.post(url = self.url, data = self.data)                   #发送post请求
        res_json = res.json()                                                   #将获取结果转换json格式
        self.assertEqual(res_json.get("respCode"), "C0001")                     #断言
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法|账期不能为空") #断言
        self.assertEqual(res_json.get("totalAmount"),0.0)                       #断言
        self.assertEqual(res_json.get("customerBills"),None)                    #断言


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite() 
    #suite.addTest(qryCustomerBills("testNormal_001"))  # 按用例执行
    #suite.addTest(qryCustomerBills("testError_002"))
    #suite.addTest(qryCustomerBills("testError_003"))
    # suite.addTest(qryCustomerBills("testError_004"))
    # unittest.TextTestRunner(verbosity=2).run(suite)