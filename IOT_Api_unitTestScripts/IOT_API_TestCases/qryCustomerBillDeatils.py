#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'XT'

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
# 账单详情列表查询
# 暂时不支持企业id为空 查询全部
class qryCustomerBillDeatils(unittest.TestCase):
    def setUp(self):
        self.url = envVariables.host + "/proxy/qryCustomerBillDeatils"
        self.data = {"billingCustomerId":"3", "accountPeriodId": "20170527"}# 出账客户ID, 账期ID
        
    def tesrDown(self):
        pass
    def testNormal_001(self):
        self.data = json.dumps(self.data)
        res = requests.post(url = self.url, data = self.data)# post请求
        res_json = res.json()# json格式转化
        self.assertEqual(res_json.get("respCode"), "0000") # 断言返回结果
        self.assertEqual(res_json.get("respDesc"), "success")
        self.assertEqual(res_json.get("totalAmount"), 0.0)
        data = json.loads(self.data)# 字符串转化
        # 查询sql
        sql = """SELECT 
              d.account_period_mark,b.customer_name,a.ability_ch_name,
              a.consumer_name,a.charge_rule_id,f.derate_amount / 1000,f.final_amount / 1000,
              (f.final_amount - f.derate_amount) / 1000 
            FROM
              billing.customer_app a,billing.bill_customer b,billing.customer_ccount_period c,billing.account_period d,
              billing.ability_account_period_charge_rule e,billing.customer_bill_item f 
            WHERE a.billing_customer_id = b.billing_customer_id 
              AND a.billing_customer_id = c.billing_customer_id 
              AND c.account_period_id = d.account_period_id 
              AND c.customer_ccount_period_id = e.consumer_ccount_period_id 
              AND e.ability_account_period_charge_rule_id = f.ability_account_period_charge_rule_id 
              AND a.ability_name = e.ability_name AND a.consumer_mark = e.consumer_mark 
              AND c.billing_customer_id = %s
              AND c.account_period_id = %s """ % (data.get("billingCustomerId"), data.get("accountPeriodId"))
        res_sql = common_optMysql.GetDatas_QueryDB(sql) # sql返回结果
        print res_sql
        self.assertEqual(len(res_json.get("customerBillDetails")), len(res_sql))# 断言接口返回结果与sql返回结果长度
        sql_01 = []                                                             #定义一个列表
        for i in res_sql:                                                       #获取sql1里的数据                                                              
            sql_01.append(i[0])                                                 #循环放入list_01里
            sql_01.append(i[1])
            sql_01.append(i[2])
            sql_01.append(i[3])
            sql_01.append(i[4])
            sql_01.append(float(i[5]))
            sql_01.append(float(i[6]))
            sql_01.append(float(i[7]))                                          #转换flost类型放入列表
        #tup = tuple(sql_01)
        list_01 = []                                                            #定义一个列表
        for i in res_json.get("customerBillDetails"):                                 #获取返回customerBills里的数据
            list_01.append(i.get("accountPeriodMark"))                          #循环放入list_01里
            list_01.append(i.get("customerName"))
            list_01.append(i.get("abilityChName"))
            list_01.append(i.get("consumerName"))
            list_01.append(i.get("chargeRuleId"))
            list_01.append(i.get("costDerate"))
            list_01.append(i.get("finalAmount"))
            list_01.append(i.get("totalAmount"))
        sql_01.sort()                                                           #排序
        list_01.sort()                                                          #排序
        self.assertEqual(sql_01,list_01)                                        #断言俩列表的值

        # x = True# 初始化x值
        # for i in res_json.get("customerBillDetails"):# 循环获取返回的值
        #     list_01 = []# 初始化列表
        #     list_01.append(i.get("accountPeriodMark"))# 添加到列表中
        #     list_01.append(i.get("customerName"))
        #     list_01.append(i.get("abilityName"))
        #     list_01.append(i.get("consumerMark"))
        #     list_01.append(i.get("chargeRuleId"))
        #     list_01.append(int(i.get("costDerate")))
        #     list_01.append(int(i.get("finalAmount")))
        #     list_01.append(int(i.get("totalAmount")))
        #     tup = tuple(list_01)
        #     if tup not in res_sql:
        #         x = False
        # self.assertTrue(x)
    def testError_002(self):
        del self.data["billingCustomerId"]
        self.data = json.dumps(self.data)
        res = requests.post(url = self.url, data = self.data)# post请求
        res_json = res.json()# json格式转化
        # print res.text
        self.assertEqual(res_json.get("respCode"), "C0002") # 断言返回结果
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法（关联权限）|客户不能为空")
        self.assertEqual(res_json.get("totalAmount"), 0.0)
        self.assertEqual(res_json.get("customerBillDetails"), None)
    def testError_003(self):
        del self.data["accountPeriodId"]
        self.data = json.dumps(self.data)
        res = requests.post(url = self.url, data = self.data)# post请求
        res_json = res.json()# json格式转化
        self.assertEqual(res_json.get("respCode"), "C0001") # 断言返回结果
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法|账期不能为空")
        self.assertEqual(res_json.get("totalAmount"), 0.0)
        self.assertEqual(res_json.get("customerBillDetails"), None)
    def testError_004(self):
        del self.data["accountPeriodId"]
        del self.data["billingCustomerId"]
        self.data = json.dumps(self.data)
        res = requests.post(url = self.url, data = self.data)# post请求
        res_json = res.json()# json格式转化
        self.assertEqual(res_json.get("respCode"), "C0001") # 断言返回结果
        self.assertEqual(res_json.get("respDesc"), u"请求参数校验不合法|账期不能为空")
        self.assertEqual(res_json.get("totalAmount"), 0.0)
        self.assertEqual(res_json.get("customerBillDetails"), None)
if __name__ == '__main__':
    # suite = unittest.TestSuite() 
    # suite.addTest(qryCustomerBillDeatils("testError_002"))  # 按用例执行
    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()