#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

from  hashlib import md5
import os 
import sys
import random
import string
import time
import common_optMysql,common_optOracle, common_optOracle_billing

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
    sql = "SELECT to_char(svc_number) FROM SVC_NUMBER WHERE svc_number_status = 10 and MVNO_BUSINESS_MARK = 'VOPI' and THOUSAND_SVC_SEG like '%s'" % seg
    return common_optOracle.QueryDB(sql)

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


def getIMSI10_8():
    '''
    同时满足IMSI第10位等于8
    @return 符合号段限制的IMSI
    '''
    return common_optOracle.GetDatas_QueryDB("select  im.TEN_THOUSAND_SEGMENT,icd.iccid, im.imsi from iccid icd,imsi im  where icd.iccid_id = im.iccid_id \
    and im.TEN_THOUSAND_SEGMENT in \
    ( SELECT substr(THOUSAND_SVC_SEG,0,7) FROM SVC_NUMBER WHERE svc_number_status = 10 and MVNO_BUSINESS_MARK = 'VOPI' and (THOUSAND_SVC_SEG like '170%' or THOUSAND_SVC_SEG like '171%')\
    ) and im.IMSI_STATUS = 20 and substr( im.imsi,10,1) = 8 and rownum = 1")[0]

def getUid_IMSI(svc_number):
    '''
    @param svc_number 需要查询用户ID的开户号码
    @return 符合传入开户号码的UID和IMSI元组  
    '''  
    svc_number = int(svc_number)
    return common_optOracle.GetDatas_QueryDB("select mvno_user_id,imsi from dbvop.mvno_user  where  mvno_user_status = 1 and mvno_user_type = 2  and svc_number = %d" %svc_number )[0]

def billing_intercept(dicts=None,Original=None):
    """
    Original 原始话单
    dicts 列表嵌套字典， 每个字典元素是一条话单，类型 key 要替换内容的列位置。 vales为替换内容 
    参数示例：[{0:"a"},{0:"b"}] 生成2条话单，分别修改第一位置元素内容
    """
    resOriginal = []
    if Original is None:
        Original = "20011004    143     23607858958    0100000GJYY0099089800201705090332124SZD.00.m.gz   2         1000000072                     xxx m 10020000000000    17151192569                       005521317184040481                                          17151192569                 201711061030472017110510194986        460091195800113                                                  21072 09535                                                                                                                       61418702220                     21                   0                     0   0 0                                                                                                                                                        0 0                                                                              "
    if type(dicts) != list:
        return Original
    for eachDisc in dicts:
        for eachKey in eachDisc.keys():
            Original = "20011004    143     23607858958    0100000GJYY0099089800201705090332124SZD.00.m.gz   2         1000000072                     xxx m 10020000000000    17151192569                       005521317184040481                                          17151192569                 201711061030472017110510194986        460091195800113                                                  21072 09535                                                                                                                       61418702220                     21                   0                     0   0 0                                                                                                                                                        0 0                                                                              "
            # sql 找到替换的开始位置与可用最大长度
            sql = "select a.factor1, a.factor2 from conf_src_record a where a.file_type = 'MBVC' and a.record_serial = '0' and a.field_serial='%s' order by a.field_serial" % eachKey
            start_position, end_position = common_optOracle_billing.GetDatas_QueryDB(sql)[0]
            rl_old = Original[int(start_position): int(start_position) + int(end_position)]
            #print rl_old ,eachDisc[eachKey].ljust(end_position)
            Front = Original[:int(start_position)]
            After = Original[int(start_position) + int(end_position):]
            Middle = Original[int(start_position): int(start_position) + int(end_position)].replace(rl_old, eachDisc[eachKey].ljust(end_position))
            Original = Front + Middle + After
        resOriginal.append(Original)
    return resOriginal

def billing_file(Original,file_name=None):
    """
    __author__ = 'XT'
    Original 文件内容必传
    file_name 文件名称 可以没有
    """
    if not file_name:
        nowTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        file_name = '93001800700000000GJYY0099089811201711060332124SZD.C0'
        file_name = file_name.replace('20171106033212',nowTime)
        file_name = nowTime + file_name[14:]

    parent_path = os.path.dirname(sys.path[0])
    with file(parent_path + '/vop_Billing_TestCases/files_in/'+file_name,'w') as fobj: # '/app/application_mode/data_in/1/MBVC/1/in/' +
        fobj.write(Original)
if __name__ == '__main__':
    billing_file(billing_intercept(dicts = [{15:"15010793333"}]))