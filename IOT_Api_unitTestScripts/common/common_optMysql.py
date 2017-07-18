#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import sys
import pymysql
import os
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)

from IOT_API_TestCases import envVariables
from time import ctime

host,port,user,passowrd = envVariables.mysqlConnect

logPath = os.path.abspath(os.curdir) + "/error.log"


def QueryDB(sql):
    connection = pymysql.connect(host=host,user=user,port=port,password=passowrd,charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def UpdatDB(sql):
    connection = pymysql.connect(host=host,user=user,port=port,password=passowrd,charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    UpdatDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def DeleteDB(sql):
    connection = pymysql.connect(host=host,user=user,port=port,password=passowrd,charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    DeleteDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()


def GetDatas_QueryDB(sql):
    connection = pymysql.connect(host=host,user=user,port=port,password=passowrd,charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    GetDatas_QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

if __name__ == "__main__":
    print GetDatas_QueryDB("""SELECT 
        b.account_Period_Mark, c.customer_Name,a.ability_Name,a.consumer_Mark,
        a.charge_Rule_Id,d.derate_amount,d.final_amount,(d.final_amount - d.derate_amount)
        FROM 
        billing.customer_app a,billing.account_period b,billing.bill_customer c,
        billing.customer_bill_item d,billing.customer_ccount_period e,billing.customer_bill f
        WHERE 
        a.billing_customer_id = c.billing_customer_id AND c.billing_customer_id = e.billing_customer_id
        AND e.customer_ccount_period_id = f.consumer_ccount_period_id AND f.customer_bill_id = d.customer_bill_id
        AND b.account_period_id = e.account_period_id 
        AND a.billing_customer_id = 1 AND e.account_period_id = 20170710""")

