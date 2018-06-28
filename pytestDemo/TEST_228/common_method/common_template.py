#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'XT'
from time import strftime
import os, sys
from random import randint

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_fixture"

sys.path.append(file_path)

# from pubilc_methods import  files, Format

# ====== 日志打印 bebug级别 ======
import logging

def token():
    # token随机生成 %Y%m%d%H%M%S * 2 +五位随机数据
    token = str(randint(10000, 99999))
    time_token =  str(strftime("%Y%m%d%H%M%S"))
    token = str(time_token*2 + token)
    return token
def name():
    # token随机生成 %Y%m%d%H%M%S +三位随机数据
    name = str(randint(100, 999))
    time_name =  str(strftime("%Y%m%d%H%M%S"))
    name = str(time_name + name)
    return name
def QUERY_REALID_CHANCE():
    # 拼装报文格式化报文
    # 实名信息可购票数查询接口
    header={
            "body":{
                "realIDs":[{
                    "id":"370103199210137523",
                    "name":"徐涛",
                    "phone":"18906404663",
                    "type":1
                }],
                "sessionId":1292
            },
            "head":{
                "apiId":"QUERY_REALID_CHANCE",
                "appId": 6,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CPOST():
    # 拼装报文格式化报文
    # 主办票票价下单接口
    header={
            "body":{
                "mchntOrderNo": "45139549",
                "priceAmount": 496,
                "priceRealIDMap":{
                    "23553": [
                        {
                            "approved": 0,
                            "id": "320113199209122424",
                            "name": "a",
                            "phone": "15901194021",
                            "type": 1
                        }
                    ]
                },
                "productId":702,
                "requirement":[
                    {"amount": 1, "priceId":23556}
                    ],
                "sessionId":4196,
                "ticketType":1
            },
            "head":{
                "apiId":"CPOST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CSOST():
    # 拼装报文格式化报文
    # 主办票锁座下单接口
    header={
            "body":{
                "mchntOrderNo": "0000130000002033",
                "priceAmount": 4,
                "productId": 630,
                "requirement": [
                    {
                        "priceId": 22875,
                        "seatEntry": {
                            
                        },
                        "type": 0
                    }
                ],
                "seatRealIDMap": {
                },
                "sessionId": 4034,
                # "takeTicketVoucher": {
                #     "type": 2
                # },
                "ticketType": 1
            },
            "head":{
                "apiId":"CSOST",
                "appId":5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def FOST():
    # 拼装报文格式化报文
    # 确认订单订单接口
    header={
            "body":{
                "orderNo": 18060800141557155
            },
            "head":{
                "apiId":"FOST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def FOST_228():
    # 拼装报文格式化报文
    # 228专用-确认订单接口
    header={
            "body":{
                "orderNo": 18060800141557155
            },
            "head":{
                "apiId":"FOST_228",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CLOST():
    # 拼装报文格式化报文
    # 取消订单接口
    header={
            "body":{
                "orderNo": 18060800091557183
            },
            "head":{
                "apiId":"CLOST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header 

def ORDER_QUERY_TICKET():
    # 拼装报文格式化报文
    # 云订单批量查云票品接口
    header={
            "body":{
                "orderNoList": [ 18060700131557125 ]
            },
            "head":{
                "apiId":"ORDER_QUERY_TICKET",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header 

def REALID_PHONE_QUERY_TICKET():
    # 拼装报文格式化报文
    # 实名手机信息查云票品接口
    header={
            "body":{
                "realIDPhone": {
                "approved": 0,
                "id": "370103199210137523",
                "name": "赵荣华",
                "phone": "18906404663",
                "type": 1
                }
            },
            "head":{
                "apiId":"ORDER_QUERY_TICKET",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def APPLY_REFUND():
    # 拼装报文格式化报文
    # 申请退票接口
    header={
            "body":{
                "orderNo": "P18060700141557119",
                "reasonDesc": "退>票申请中",
                "ticketNoList": [
                    "T0042230002281190",
                    "T0042230002281189"
                ]
            },
            "head":{
                "apiId":"APPLY_REFUND",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def PRODUCT_LIST():
    # 拼装报文格式化报文
    # 商品列表接口
    header={
            "body":{
                "productId": 1
            },
            "head":{
                "apiId":"PRODUCT_LIST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def SESSION_LIST():
    # 拼装报文格式化报文
    # 场次列表接口
    header={
            "body":{
                "productId": 1,
                "sessionId":4629
            },
            "head":{
                "apiId":"SESSION_LIST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def TICKET_PRICE_LIST():
    # 拼装报文格式化报文
    # 票价列表接口
    header={
            "body":{
                "sessionId": 4034
            },
            "head":{
                "apiId":"TICKET_PRICE_LIST",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CHANGE_TICKET_PHONE():
    # 拼装报文格式化报文
    # 云票品手机号码修改接口
    header={
            "body":{
                # "oldPhone": "1223123",
                "newPhone": "1231313",
                "ticketNo": "T0042230002281181"
            },
            "head":{
                "apiId":"CHANGE_TICKET_PHONE",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CHANGE_TICKET_REALID():
    # 拼装报文格式化报文
    # 云票品入场实名信息换绑接口
    header={
            "body": {
                "newRealID": {
                    "approved": 0,
                    "id": "110101201406012377",
                    "name": "七七",
                    "phone": "18911187892",
                    "type": 1
                },
                "ticketNo": "T0042750002283721"
            },
            "head":{
                "apiId":"CHANGE_TICKET_REALID",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def ORDER_NOTIFY():
    # 拼装报文格式化报文
    # 订单票品推送更新接口
    header={
            "body":{
                "cloudOrder": {"aasasa":"asaas"}
            },
            "head":{
                "apiId":"ORDER_NOTIFY",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def REALID_QUERY_REALID_CHANGE_TICKET():
    # 拼装报文格式化报文
    # 实名查参与过变更的云票品接口
    header={
            "body":{
                "REALID": [{
                    "id":"370103199210137523",
                    "name":"徐涛",
                    "phone":"18906404663",
                    "type":1
                }]
            },
            "head":{
                "apiId":"REALID_QUERY_REALID_CHANGE_TICKET",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def CHECK_MOBILE():
    # 拼装报文格式化报文
    # 验证主办订单表手机号码是否存在
    header={
            "body":{
                "mobile": "18906404663"
            },
            "head":{
                "apiId":"CHECK_MOBILE",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def SPONSOR_ORDER_FOR_MOBILE():
    # 拼装报文格式化报文
    # 获取手机号码对应的订单列表
    header={
            "body":{
                "mobile": "18906404663"
            },
            "head":{
                "apiId":"SPONSOR_ORDER_FOR_MOBILE",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def BIND_INFO_FOR_ORDER():
    # 拼装报文格式化报文
    # 获取订单下全部票种绑定信息
    header={
            "body":{
                "pageNo": 1,
                "pageSize": 20,
                "platFormId": "1557314"
            },
            "head":{
                "apiId":"BIND_INFO_FOR_ORDER",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def BIND_INFO_FOR_TICKET():
    # 拼装报文格式化报文
    # 获取座位全部绑定记录
    header={
            "body":{
                "platformOrderId": "1557221",
                "platformSeatId": "2283155"
            },
            "head":{
                "apiId":"BIND_INFO_FOR_TICKET",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header

def VALIDATE_IDENT_BY_CODE():
    # 拼装报文格式化报文
    # 根据绑定码获取订单信息
    header={
            "body":{
                "bindCode": "Y1NB2@79@HBA1A197",
                "ticketType": 1
            },
            "head":{
                "apiId":"VALIDATE_IDENT_BY_CODE",
                "appId": 5,
                "appUserName":"yleAI",
                "sdkVersion":"2.0.0-beta09",
                "sign":"a8b134be61bd4f00b8fa0ffaf0762b4d",
                "token":token()
            }
        }
    return header



if __name__ == '__main__':
    print(VALIDATE_IDENT_BY_CODE())