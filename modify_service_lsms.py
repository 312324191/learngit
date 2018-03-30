#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'XT'

import requests
import json
from time import strftime
from time import sleep
import random
import cx_Oracle
import os
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
requests.packages.urllib3.disable_warnings()  
path=str(os.path.dirname(__file__))
base_dir = path.replace('\\', '/')

# ip_port_servername = "10.124.5.209:1530/TDB" # 性能环境
ip_port_servername = "10.161.50.87:1530/TDB"  # 云化环境
# ip_port_servername = "10.124.1.11:1521/sod"  # 准生产环境
user = "dbvop"
password = "dbvop"

# user = "query"
# password = "1qaz2wsx"
# API_ID = "10.124.5.208"  # 性能环境
API_ID = "10.161.50.86"  # 云化环境
# API_ID = "10.124.1.7"  # 准生产环境

# ====== 日志打印 bebug级别 ======
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='API_DUBEG.log',
                filemode='w')
    
# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')

def ocl_data(sql):
    try:
        global ip_port_servername, user, password
        connection = cx_Oracle.connect(user, password, ip_port_servername)
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()
def modify_service_lsms(svc_number, mvonmark):
    allmark = {
    "VOPI" : ("OJvWpmI",   "hcOPBgJ4dB8WBy1V5nrpGaIqaP2INnrhRd0IZ4GflgtCPWsY"),
    "HODO" : ("5hdoc0g",   "WFykRKbDPMiTZRnU1pw7296Pl8zgrbM4hV7I16jGAAyNxEgu"),
    "HJSJ" : ("6jj4HEs",   "LCJaN1WeTNzbmsRPjWvNCEpbOryXe9eNOi9JC5JqP37WmdiK"),
    "ALBB" : ("6pLN9ab",   "g8NXJLcpqLXFigYmePNVGX3B7PEEEJvwBbyhF4HToEieurae"),
    "MSEC" : ("C8eSMCR",   "ysF9fIlUpwFM9VVwchbuC6eDI0LLSptozoNIWIgcjpLnyWfs"),
    "EKTE" : ("Ek2eAT5",   "1zNCfmNBwwi53p5v6LCToiL0FHQK4MUEvg9XBUBmM6c2n4tw"),
    "WONI" : ("GyIwOen",   "hVX2qnLoyUqKMZVIs2rfVnBGx6umDA79Bfzq7SjhggUzfYc9"),
    "JIDO" : ("JE0ijPd",   "ExqxqVljCCkcLvSomqrPD2ty2VFgWF6GZZ6nQblwLJwoxRnr"),
    "ERLS" : ("LEWr7s0",   "GA2bKApHnmvqAYEFPOIpQNS4GsWeckbtFH9mCbCoFe876Kne"),
    "PIAN" : ("LaTnIqp",   "gvT389dB9rZmjq236TaMoZIZjk7mPtpx0Hl1g8vAQDowzlQk"),
    "FTLK" : ("N7T1XKf" ,  "K5W3lWKnY5aaysrN5eKpZTlMUbfanFwdqiRVOYXTUySHIDx2"),
    "VOPI" : ("OJvWpmI" ,  "hcOPBgJ4dB8WBy1V5nrpGaIqaP2INnrhRd0IZ4GflgtCPWsY"),
    "DPHO" : ("PW6odE8" ,  "LIEwRvk5il8KIDvFDICqghnnWJ9hPTxlXe7xu09bBJNDEjLh"),
    "QNTE" : ("TIq0bEn" ,  "uJlqmbaxT7d12qskZPVYXu34oiASPItzSOOIRCKxcJ0jtA8x"),
    "BUSP" : ("UpKbprs" ,  "rwuoBPT5z2bzAV4l5MMNkr7x4Bjyucp1eTcaOeqlyquNEeHp"),
    "BOYU" : ("YLouG9b" ,  "2EavgJ2DYKqjMqDboodRViEb3Fhd4TgJKNsZAaEdtCZGaLVX"),
    "CFCO" : ("cbCiFjo" ,  "scIPeaXTER8per864IP5NxZ4N262OVSVz8lhkZ1iAK5E3BsU"),
    "ASDI" : ("dATIEsv" ,  "roNrRgjV4qvYjqWjKluYaIFD3A1HsINmK1y6SECr2JE4eNzf"),
    "YTEL" : ("dte1mYr" ,  "ebHyquN3M6SjMHrE42dFwl4zNddDhDxG73JA6LygQbuYBhpB"),
    "HEDH" : ("efYHdHL" ,  "pcDucwqaraACZxMP5bKFLi1SjXFRxwRGolG8R9pvf5QmADT0"),
    "MITE" : ("mHyt1Pe" ,  "c6QtMpYGx1wlpQef1MLoJ15dkJCXaTOJx5tLHaQLfxpC4bYI"),
    "HTNE" : ("nxmHTej" ,  "p9bagVEEPpc6JeufeIfHUeL51FfGc3GI03Ib4UCTTnGHdykb"),
    "GOME" : ("pmo9hGe" ,  "gI3ediY1Qe3cHY0JeqIP1gn0cioEY3KiG9ATp4xTpf9xTDqi"),
    "SOSH" : ("shGSx0C" ,  "jn7bCk2tUsoVkpHC9sIBP3YxC5ei1yDBIWDVazVGZIzmfSu9"),
    "KTCH" : ("thwc59K" ,  "o9Di5BufVwYpydgvgbu4MseZjkm8S0XMFYCLoaeBqiYP1nl1"),
    "YOKU" : ("uOboK4y" ,  "UX8TflCYczm79OBkbLvEeHAALSyCYIf88U6l6g3wUMLloMDt"),
    "SUNI" : ("wIMUPsN" ,  "TA7xgqKNe3l54aqYds5Yhyg0ABBpUHpTquz3RexN2FwKkAFO")
    }
    mvnokey, token = allmark.get(mvonmark)

    serial_number = "LDBGAPI" + strftime("%Y%m%d%H%M%S") + str(random.randint(100000000, 999999999))
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    service = {
        "mvnokey": mvnokey, 
        "serial_number": serial_number, 
        "timestamp": timestamp, 
        "service_type": "basic_service", 
        "service_name": "modify_service_lsms", 
        "api_name": "cu.vop.basic_service.modify_service_lsms", 
        "data": {
            "order_id": serial_number + "0000", 
            "phone_number": svc_number
          
        }
    }
    global API_ID
    url = 'https://%s:8006/OSN/vop/basic_service/modify_service_lsms/v6?token=%s' % (API_ID, token)

    return url, service

if __name__ == '__main__':
    logging.debug(u'开始脚本执行')
    sql ='select svcnumber, mvnomark from dbvop.modify_lsms where flag=0 order by svcnumber'
    res_sql = ocl_data(sql)
    # print len(res_sql)
    if len(res_sql)==0:
        logging.debug(u'没有号码了 干毛线呢！')
    for i in res_sql:
        url, data = modify_service_lsms(int(i[0]),i[1])
        data = json.dumps(data, indent=4)
        rsp = requests.post(url=url, data=data, verify=False)
        rsp_json = rsp.json()
        # print json.dumps(rsp_json, encoding='utf-8', ensure_ascii=False, indent=4)
        try:
            rsp_json.get('data').get('message') == 'SUCCESS'
        except AttributeError:
            logging.debug('Error：%s' % rsp_json)
            with open(base_dir + "False_number.txt", 'w') as file :
                file.write(i[0])
    logging.debug(u'结束脚本执行')