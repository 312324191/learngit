#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

import sys
import cx_Oracle
import os
import time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 解决oracle中文乱码

from time import ctime

usename,password,ip_port_servername = ('dbvop', 'tydicxdrqaz', '10.124.1.11:1521/sod')

logPath = os.path.abspath(os.curdir) + "/error.log"

def QueryOperationDB(sql):  
    connection = cx_Oracle.connect(usename, password, '10.124.1.11:1521/sod') 
    try:
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryOperationDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def QueryDB(sql):  
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def GetDatas_QueryDB(sql):
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    GetDatas_QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def main(x):
    iccidList = []

    maxIccid_id = int(QueryDB("SELECT max(iccid_id) FROM iccid")) + 1
    max_iccid = GetDatas_QueryDB("select max(iccid) from dbvop.ICCID where length(ICCID)='20'")
    max_iccid = int(max_iccid[0][0]) + 10 
    for eachTuple in range(x):
        iccidList.append(int(max_iccid) + (eachTuple*10)) 
    print maxIccid_id,  iccidList

    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        cursor = connection.cursor()
        for eachIccid,index in zip(iccidList,range(1,len(iccidList)+1)):
            # imsi =QueryDB("select imsi from test_svc_number where iccid ='%s'" % eachIccid[:-1])
            Insert_sql = '''INSERT INTO DBVOP.ICCID (ICCID_ID, MVNO_BUSINESS_ID, 
            MVNO_USER_ID, ICCID, USIM_MAKE_APPLY_NO, USIM_MAKE_APPLY_ITEM_ID, 
            MVNO_BUSINESS_MARK, PROV_CODE, EPARCHY_CODE, AVAILABLE_TIME, ENABLE_TIME, 
            END_TIME, IMSI, MSIN, PUK1, PUK2, PIN1, PIN2, AMD1, KEY, A4, OP, 
            TERMINATE_ACT, ICCID_STATUS, USIM_TYPE, KI, OLD_KEY) 
            VALUES (%s, 15, null, %s, 'ZS4990140001', 
            'A001', 'VOPI', null, null, TO_TIMESTAMP('2016-08-30 00:00:00.000000', 
            'YYYY-MM-DD HH24:MI:SS.FF6'), null, null, 'FFFFFFFFFFFFFFF', null, 
            '22222222', '22222222', '1111', '11111111', '33333333', null, '1 ', 
            '1 ', null, '10', '1', null, null)''' % (maxIccid_id,int(eachIccid))
            
            cursor.execute(Insert_sql)
            maxIccid_id += 1
            if index % 50 == 0:
                connection.commit()  # 每100笔事务，提交一次
        cursor.close()
        connection.commit() # 剩余记录最终提交
        print "Finished."
    except Exception,e:
        print e
    finally:
        connection.close()

if __name__ == '__main__':
    # 输入生成次数，修改数据库连接就可以了
    main(5000)
