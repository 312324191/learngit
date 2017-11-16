#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import time
import requests
import envVariables

def getOrderCompleteTime():
	timeFormat = '%Y%m%d%H%M%S'
	return 	time.strftime(timeFormat,time.localtime(time.time()))

def OrderComplete(TRANS_IDO,SO_NBR):
	"""
	 @param: TRANS_IDO  30位的serial_number  例如：OJvWpm2017030316353312lxy
    @param: SO_NBR     BSS系统的定单号  例如：96VO030974086294
    @return: 竣工结果，大于0为成功，小于0为失败
    """
	xmlString = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
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
            <TRANS_IDO>%s</TRANS_IDO>
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
               <TRANS_IDC>201412261104034562233102608101</TRANS_IDC>
               <CUTOFFDAY>20141226</CUTOFFDAY>
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
</soapenv:Envelope>'''  %(TRANS_IDO,getOrderCompleteTime(),SO_NBR,getOrderCompleteTime(),getOrderCompleteTime())
	
	headers={"Accept-Encoding":"gzip,deflate","Content-Type": "text/xml;charset=UTF-8"}

	res = requests.post(url=envVariables.OrderCompleteURL,data=xmlString,headers=headers).content
	return str(res).find("<RSP_CODE>0000</RSP_CODE>")


if __name__ == '__main__':
	print OrderComplete('ZpxM7yBPdoA0SH3qQtjDvEGklgOeLJ','96VO031574086827')
