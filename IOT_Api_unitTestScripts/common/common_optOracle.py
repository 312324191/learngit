#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import sys
import cx_Oracle
import os
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 解决oracle中文乱码
from KPI_API_TestCases import envVariables
from time import ctime

usename,password,ip_port_servername = envVariables.oracleConnect

   
logPath = os.path.abspath(os.curdir) + "/error.log"


def QueryDB(sql):  
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
    	
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        # cursor.close()
        return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        cursor.close()
        connection.close()

def UpdatDB(sql):
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.commit()
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    UpdatDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def DeleteDB(sql):
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    DeleteDB     "+str(e)+"    %s    "%ctime()+os.linesep)
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

if __name__ == "__main__":
	print GetDatas_QueryDB("select * from APEAL_SIGN_OUT_APPLICATION where province_code = '51' and sign_out_type = 0")[0]


