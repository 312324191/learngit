#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import sys
import os
import requests
import json

path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)

from common import common_tools,common_optOracle
from vop_Billing_TestCases import envVariables,OrderComplete

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

host = envVariables.api_host  # 环境不同更改环境配置

mvno_app = envVariables.mvno_app
service_type = 'basic_service'          # 'basic_service'  资源池， 'model_product' 模组
service_name = 'register_account'       # 'register_account'资源池 ，'register_account_model' 模组
apiname = "cu.vop." + service_type + "." + service_name

token = common_tools.getToken(mvno_app)
url = (host+'/OSN/vop/'+service_type+'/'+  service_name +'/v2?token='+token) # 资源池3G，4G用
#url = (host+'/OSN/vop/'+service_type+'/'+ service_name  +'/v3?token='+token) # 模组用

ten,iccid,imsi = common_tools.getIMSI10_8()
service_number = common_tools.getServcieNumber(str(ten) + "%")

params = common_tools.getCommonRequestContent(mvno_app,service_type,service_name,apiname)

data_params = {
                "order_id": params['serial_number'] + common_tools.getRandomString(4),
                "phone_number":int(service_number),
                "imsi": imsi, 
                "iccid": iccid,
                "service_class_code": "4G", # "3G" 资源池3G
                "user_property": "postpaid",
                "services": [
                                {
                                    "product_id": "V0001",
                                    "action_type": "order"
                                }
                            ],
                "customer": {
                            "cust_name": "PythonAutoTest",
                            "cert_address": "beijing-yizhuang",
                            "cert_type_code": "01",
                            "cert_code": "11010719860915000x"
                            }
                }
params["data"] = data_params


def register():
    res = requests.post(url=url,data=json.dumps(params), verify=False)
    print res.json()
    assert(res.json().get(u'data').get(u'status') == True)
    assert(res.json().get(u'data').get(u'message') == u'SUCCESS') # 接口成功状态检查点

    #竣工
    dbBSS_SERVICE_ORDER_NO = common_optOracle.QueryDB("SELECT BSS_SERVICE_ORDER_NO from SERVICE_ORDER where mvno_service_order_no = '%s'" % params.get('data').get('order_id'))
    # print dbBSS_SERVICE_ORDER_NO
    if OrderComplete.OrderComplete(params['serial_number'],dbBSS_SERVICE_ORDER_NO) > 0:
        print u'开户成功', service_number
    else:
        raise ValueError(u"竣工失败")


if __name__ == '__main__':
    register()