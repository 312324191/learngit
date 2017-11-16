#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import sys
import pymysql
import os
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)

from vop_Billing_TestCases import envVariables
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
    print QueryDB("SELECT `MVNO_TOKEN` FROM `esbcfgdb`.`mvno_app` WHERE `MVNO_KEY` = 'OJvWpmI';")

