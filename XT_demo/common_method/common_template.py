#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'XT'
from time import strftime
import os, sys
import random

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_fixture"

sys.path.append(file_path)

import oracle_db, mysql_db

# ====== 日志打印 bebug级别 ======
import logging

class Requsts_template():
    """docstring for Requsts_template"""
    def __init__(self, business_make=None):
        # 初始化判断是否有参数 如果有参数就去mysql查一个mvnokey与token 拼装信息 如果没有默认VOPI
        if business_make is None:
            self.mvnokey = "OJvWpmI"
            self.serial_number = self.mvnokey + strftime("%Y%m%d%H%M%S") + str(random.randint(100000000, 999999999))
            self.order_id = self.serial_number + '0000'
            self.token = 'hcOPBgJ4dB8WBy1V5nrpGaIqaP2INnrhRd0IZ4GflgtCPWsY'
        else:
            try:
                db = mysql_db.DB()
                sql = "select ma.MVNO_KEY as mvnokey,ma.MVNO_TOKEN as token \
                from esbcfgdb.mvno_app ma where ma.MVNO_BUSINESS_MARK='%s'" % business_make
                req_sql = db.select_one(sql)
                # logging.debug('This is debug message req_sql : %s' % req_sql)
                if req_sql is None:
                    print "请查看转企标识没有找到%s信息" % business_make
                else:
                    self.mvnokey = req_sql["mvnokey"]
                    self.serial_number = self.mvnokey + str(strftime("%Y%m%d%H%M%S")) + str(random.randint(100000000, 999999999))
                    self.order_id = self.serial_number + '0000'
                    self.token = req_sql["token"]    
            # except Exception as e:
            #     raise 'msyql报错:' + e
            finally:
                db.close()
        # 初始化一下timestamp 仅提供给开户接口 其他接口需要重新初始化时间
        self.timestamp = strftime("%Y-%m-%d %H:%M:%S")
    def For_Order_Complete_Notify_Ser(self, SO_NBR):
        # 竣工报文模板 so_NBR：bss流水号
        PROCESS_TIME = strftime("%Y%m%d%H%M%S")
        CUTOFFDAY = strftime("%Y%m%d")
        date = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
           <soapenv:Body>
              <SO_COMPLETE_INPUT xmlns="http://ws.chinaunicom.cn/VOPForOrderCompleteNotifySer/unibssBody">
                 <UNI_BSS_HEAD xmlns="http://ws.chinaunicom.cn/unibssHead">
                    <ORIG_DOMAIN>UCRM</ORIG_DOMAIN>
                    <SERVICE_NAME>VOPForOrderCompleteNotifySer</SERVICE_NAME>
                    <OPERATE_NAME>vopForSoComplete</OPERATE_NAME>
                    <ACTION_CODE>0</ACTION_CODE>
                    <ACTION_RELATION>0</ACTION_RELATION>
                    <ROUTING>
                       <ROUTE_TYPE>00</ROUTE_TYPE>
                       <ROUTE_VALUE>96</ROUTE_VALUE>
                    </ROUTING>
                    <PROC_ID>otb20259253114@1419563043328</PROC_ID>
                    <TRANS_IDO>VOPIOA%s1000002781</TRANS_IDO>
                    <PROCESS_TIME>%s</PROCESS_TIME>
                    <COM_BUS_INFO>
                       <OPER_ID>bo</OPER_ID>
                       <PROVINCE_CODE>99</PROVINCE_CODE>
                       <EPARCHY_CODE>910</EPARCHY_CODE>
                       <CITY_CODE>123</CITY_CODE>
                       <CHANNEL_ID>123</CHANNEL_ID>
                       <CHANNEL_TYPE>1234567</CHANNEL_TYPE>
                       <ACCESS_TYPE>07</ACCESS_TYPE>
                       <ORDER_TYPE>01</ORDER_TYPE>
                    </COM_BUS_INFO>
                    <SP_RESERVE>
                       <TRANS_IDC>VOPIOA%s1000002781</TRANS_IDC>
                       <CUTOFFDAY>%s</CUTOFFDAY>
                       <OSNDUNS>9100</OSNDUNS>
                       <HSNDUNS>xxxx</HSNDUNS>
                       <CONV_ID/>
                    </SP_RESERVE>
                    <TEST_FLAG>0</TEST_FLAG>
                    <MSG_SENDER>0400</MSG_SENDER>
                    <MSG_RECEIVER>1000</MSG_RECEIVER>
                 </UNI_BSS_HEAD>
                 <UNI_BSS_BODY>
                    <SO_COMPLETE_REQ xmlns="http://ws.chinaunicom.cn/VOPForOrderCompleteNotifySer/unibssBody/vopForSoCompleteReq">
                       <SERVICE_ORDER_RETURN>
                          <ORDER_INFO>
                             <LOCAL_NET_ID>0024</LOCAL_NET_ID>
                             <SO_NBR>%s</SO_NBR>
                             <RETURN_TYPE>C</RETURN_TYPE>
                             <RETURN_DATE>%s</RETURN_DATE>
                             <COMPLETE_DATE>%s</COMPLETE_DATE>
                          </ORDER_INFO>
                       </SERVICE_ORDER_RETURN>
                    </SO_COMPLETE_REQ>
                 </UNI_BSS_BODY>
                 <UNI_BSS_ATTACHED xmlns="http://ws.chinaunicom.cn/unibssAttached">
                    <MEDIA_INFO/>
                 </UNI_BSS_ATTACHED>
              </SO_COMPLETE_INPUT>
           </soapenv:Body>
        </soapenv:Envelope>
        """ % (PROCESS_TIME, PROCESS_TIME, PROCESS_TIME, CUTOFFDAY, SO_NBR, PROCESS_TIME, PROCESS_TIME)
        # logging.debug("This is date %s " % date)
        return date
    def basic_service(self, phone_number, imsi, iccid, services,service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 资源池成卡开户报文
        # 返回报文体，token，service_type，service_name
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "basic_service"
        service_name = "register_account"
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "user_property":"postpaid",
                "service_class_code": service_class_code,
                "imsi": imsi,
                "iccid": iccid,
                "services":services,
                 "customer": {
                    "cust_name": "王三",
                    "cert_address": "北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def extended_service(self, phone_number, imsi, iccid, services, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 资源池白卡开户报文
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "extended_service"
        service_name = "blankcard_register_account"
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "user_property":"postpaid",
                "service_class_code": service_class_code,
                "imsi": imsi,
                "iccid": iccid,
                "services":services,
                 "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def model_product(self, phone_number, imsi, iccid, mproducts, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 模组成卡开户报文
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "model_product"
        service_name = "register_account_model"
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name":service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "user_property":"postpaid",
                "service_class_code": service_class_code,
                "imsi": imsi,
                "iccid": iccid,
                "mproducts":mproducts,
                 "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def blankcard_model_product(self, phone_number, imsi, iccid, mproducts, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 模组白卡开户报文
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "model_product"
        service_name = "blankcard_register_account_model"
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "user_property":"postpaid",
                "service_class_code": service_class_code,
                "imsi": imsi,
                "iccid": iccid,
                "mproducts":mproducts,
                "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def modify_service_model(self, phone_number, imsi, mproducts, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 模组产品变更
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "model_product"
        service_name = "modify_service_model"
        self.serial_number = self.mvnokey + str(strftime("%Y%m%d%H%M%S")) + str(random.randint(100000000, 999999999))
        self.order_id = self.serial_number + '0000' 
        self.timestamp = strftime("%Y-%m-%d %H:%M:%S")
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "service_class_code": service_class_code,
                "imsi": imsi,
                "mproducts":mproducts,
                "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def modify_service(self, phone_number, imsi, services, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 资源池变更
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "basic_service"
        service_name = "modify_service"
        self.serial_number = self.mvnokey + str(strftime("%Y%m%d%H%M%S")) + str(random.randint(100000000, 999999999))
        self.order_id = self.serial_number + '0000' 
        self.timestamp = strftime("%Y-%m-%d %H:%M:%S")
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "service_class_code": service_class_code,
                "imsi": imsi,
                "services":services,
                "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
    def switch_status(self, phone_number, imsi, iccid, services, service_class_code=None):
        # 输入电话号码、网别（默认4G）、imsi、iccid、开户资源信息
        # 停开机
        if service_class_code is None:
            service_class_code ='4G'
        service_type = "basic_service"
        service_name = "switch_status"
        self.serial_number = self.mvnokey + str(strftime("%Y%m%d%H%M%S")) + str(random.randint(100000000, 999999999))
        self.order_id = self.serial_number + '0000' 
        self.timestamp = strftime("%Y-%m-%d %H:%M:%S")
        date={
            "mvnokey": self.mvnokey,
            "serial_number": self.serial_number,
            "timestamp": self.timestamp,
            "service_type": service_type,
            "service_name": service_name,
            "api_name":"cu.vop." + service_type + '.' + service_name,
            "data":{
                "order_id": self.order_id,
                "phone_number": phone_number,
                "service_class_code": service_class_code,
                "imsi": imsi,
                "iccid": iccid,
                "services":services,
                "customer": {
                    "cust_name": u"王三",
                    "cert_address": u"北京",
                    "cert_type_code": "01",
                    "cert_code": "220111198603010011"
                }
            }
        }
        return date, self.token, service_type, service_name
if __name__ == '__main__':
    import requests
    try:
        rt = Requsts_template("VOPI")
        a = rt.For_Order_Complete_Notify_Ser(9618041800027238)
        # print json.dumps(a, sort_keys=True, indent=4, encoding='utf-8', ensure_ascii=False)
        url = 'http://10.124.1.7:8000/OSN/services/VOPForOrderCompleteNotifySer'
        rep = requests.post(url=url ,data=a, verify=False)
        print rep.content
    except AttributeError:
        print "请查看转企标识没有找到信息"
    