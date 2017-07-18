#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

from  hashlib import md5
import os 
import random
import string
import time
import common_optMysql,common_optOracle

# def MD5String(str):
#   m = md5()
#   m.update(str)
#   return m.hexdigest()

def getRandomString(number):
    """
    @param: number 需要获得的位数.
    @return: 包含大小写字母、数字的随机字符串
    """
    rule = string.letters + string.digits
    str = random.sample(rule, number)
    return "".join(str)

def getTimeStamp():
    """
    @return: 返回当前时间戳的日期格式
    """
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def getCommonRequestContent(mvnokey,service_type,service_name,api_name):
    """
    @param: mvnokey       转企的mvnokey.
    @param: service_type  basic_service/extended_service/model_product
    @param: service_name  接口名称
    @param: api_name      接口分册中定义的接口名称
    @return: 包含大小写字母、数字的随机字符串
    """
    dict = {
              "mvnokey": mvnokey,
              "serial_number": getRandomString(30),
              "timestamp": getTimeStamp(), 
              "service_type": service_type,
              "service_name": service_name,
              "api_name": api_name
            }

    return dict

def getToken(mvnokey):
    '''
    @param mvnokey
    @return mvnokey对应的token
    '''
    return common_optMysql.QueryDB("SELECT `MVNO_TOKEN` FROM `esbcfgdb`.`mvno_app` WHERE `MVNO_KEY` = '%s';" % mvnokey)

def getServcieNumber(seg):
    '''
    @param seg 对应的万号段 号码前7位
    @return 符合号段限制的有效号码
    '''
    return common_optOracle.QueryDB("SELECT svc_number FROM SVC_NUMBER WHERE svc_number_status = 10 and MVNO_BUSINESS_MARK = 'VOPI' and THOUSAND_SVC_SEG like '%s'" % seg)

def getIMSI(seg):
    '''
    @param seg 对应的万号段 号码前7位
    @return 符合号段限制的IMSI
    '''
    return common_optOracle.QueryDB("SELECT IMSI FROM imsi WHERE TEN_THOUSAND_SEGMENT like '%s' and IMSI_STATUS = 20" % seg)

def getICCID(imsi):
    '''
    @param imsi 根据imsi找到绑定关系的iccid
    @return 符合对应的ICCID
    '''  
    return common_optOracle.QueryDB("SELECT iccid FROM iccid WHERE  iccid_id in (select iccid_id from imsi where imsi = '%s')" % imsi)


if __name__ == '__main__':
    # print getServcieNumber('1700040%')
    #print getIMSI('1700040')
    #print getICCID("119000000087579")
    print getRandomString(30)