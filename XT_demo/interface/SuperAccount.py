#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

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

def Res_Template(business_make, template, svc_number=None, imsi=None, iccid=None):
    try:
        rt = Requsts_template(business_make)
        # 模组订购样例
        # logging.debug('This is debug message template : %s' % template)

        """
        传参数 有效的号码、imsi、iccid
        资源池成卡： basic_service
        资源池白卡： extended_service
        模组成卡： model_product
        模组白卡： blankcard_model_product
        模组产品变更：modify_service_model
        """
        # 如果svc_number 是空的话就去查看配置文件中的万号段数据
        if svc_number is None or imsi is None or iccid is None:
            try:
                Sn =Standard_number()
                svc_number = int(Sn.Svc_num()[0][0])
                # imsi, iccid =  Sn.Im_Icd()[0]
                imsi, iccid = Sn.White_Im_Icd()
            finally:
                Sn.close()
        logging.debug('This is debug message svc_number : %s' % svc_number)
        # logging.info("svc_number is : %s " % svc_number, "imsi is : %s " % imsi)
        data, token, service_type, service_name = rt.blankcard_model_product(svc_number, imsi, iccid, template)

        global ip, Edition, order_host
        # 拼装API请求地址
        url = "https://%s:%s/OSN/vop/%s/%s/%s?token=%s" % (ip, host, service_type, service_name, Edition, token)
        # logging.debug('url :%s' % url)
        # 拼装竣工地址
        order_url = "http://%s:%s/OSN/services/VOPForOrderCompleteNotifySer" %(ip, order_host)
    except AttributeError:
        print u"请查看转企标识没有找到信息"
    json_data = json.dumps(data, indent=4)
    logging.debug('This is debug message json_data : %s' % json_data)
    resp = requests.post(url=url, data=json_data,verify=False)
    # logging.debug('This is debug message resp.content : %s' % resp.content)
    resp_json = resp.json()
    # {"data":{"status":true,"message":"SUCCESS"}}
    try:
        resp_json.get('data').get('message') != 'SUCCESS'
    except AttributeError:
        print json.dumps(resp_json.get('error'), encoding='utf-8', ensure_ascii=False)
    else:
        try:
            vp = Verifying_Point(data["timestamp"])
            ServiceOrder = vp.Service_Order(data["data"]["order_id"])
        finally:
            vp.close()
        # logging.debug(" BSS_number:%s" % ServiceOrder)
        # 竣工需要调用ServiceOrder返回参数用的bss_service_order_no 传入报文竣工方法中
        order_data = rt.For_Order_Complete_Notify_Ser(ServiceOrder[0][2])
        order_resp = requests.post(url=order_url, data=order_data,verify=False)
        # logging.debug('This is debug message order_resp.content : %s' % order_resp.content)
        try:
            vp = Verifying_Point(data["timestamp"])
            ServiceOrder = vp.Service_Order(data["data"]["order_id"])
        finally:
            vp.close()
        if ServiceOrder[0][1] is not None:return u"竣工成功：%i " % svc_number
        else:print u'竣工失败'

if __name__=='__main__':
    # 小bug mvnobusiness != None or VOPI 需要传号码等信息不能为空
    # services = [
    #     {
    #                     "product_id":"V0001",
    #                     "action_type":"order"
    #                 },
    #     {
    #                     "product_id":"V0003",
    #                     "action_type":"order"
    #                 },
    #     {
    #                     "product_id":"V0025",
    #                     "action_type":"order"
    #                 },
    #     {
    #                     "product_id":"V0019",
    #                     "action_type":"order"
    #                 },
    #     {
    #                     "product_id":"V0017",
    #                     "action_type":"order"
    #                 }
    #             ]

    services = [
        {
                        "mproduct_id": "PR_0005",
                        "action_type": "order",
                        "packages": [
        {
                                "package_id": "PK_0033",
                                "discnts": [
        {
                                        "discnt_id": "ZE_0111",
                                        "action_type": "order"
                                    }
                                ]
                            },
        {
                                "package_id": "PK_0035",
                                "discnts": [
        {
                                        "discnt_id": "PE_0119",
                                        "action_type": "order"
                                    }
                                ]
                            },
        {
                                "package_id": "PK_0043",
                                "discnts": [
                                    {
                                        "discnt_id": "PE_0129",
                                        "action_type": "order"
                                    }
                                ]
                            },
        {
                                "package_id": "PK_0042",
                                "discnts": [
                                    {
                                        "discnt_id": "PE_0126",
                                        "action_type": "order"
                                    }
                                ]
                            },
        {
                                "package_id": "PK_0040",
                                "discnts": [
                                    {
                                        "discnt_id": "PE_0124",
                                        "action_type": "order"
                                    }
                                ]
                            }
                ]
        }
        ]
    print Res_Template(None,services)
