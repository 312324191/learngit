#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

import sys
import cx_Oracle
import os
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)

# from VOP_Api_unitTestScripts.vop_API_TestCases import envVariables
# from vop_API_TestCases import envVariables
from time import ctime

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)

usename_API = cf.get("DB_oracle_API", "user")
password_API = cf.get("DB_oracle_API", "password")
ip_port_servername_API = cf.get("DB_oracle_API", "ip_port_servername")

# ====== 日志打印 bebug级别 ======
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='DUBEG.log',
                filemode='w')
    
# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')
logPath = os.path.abspath(os.curdir) + "/error.log"

class BD_oracle_API(object):
    """属性链接数据库"""
    def __init__(self):
        global usename_API
        global password_API
        global ip_port_servername_API
        self.connection = cx_Oracle.connect(usename_API, password_API, ip_port_servername_API)
        # logging.debug('This is debug message connection : %s' % self.connection)
        self.cursor = self.connection.cursor()
        # logging.debug('This is debug message cursor : %s' % self.cursor)
    def close(self):
        self.cursor.close()
        self.connection.close()

    def QueryDB(self, sql):
        try:
            # logging.debug('This is debug message sql : %s' % sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            # logging.debug('This is debug message result : %s' % result)
            return result
        except Exception as e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)

    def UpdatDB(self, sql):
        try:
            # logging.debug('This is debug message sql : %s' % sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    UpdatDB     "+str(e)+"    %s    "%ctime()+os.linesep)

    def DeleteDB(self, sql):
        try:
            # logging.debug('This is debug message sql : %s' % sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    DeleteDB     "+str(e)+"    %s    "%ctime()+os.linesep)


    def GetDatas_QueryDB(self, sql):
        try:
            # logging.debug('This is debug message sql : %s' % sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            # logging.debug('This is debug message result : %s' % result)
            return result
        except Exception as e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    GetDatas_QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)

if __name__ == "__main__":
    try:
        DBora = BD_oracle_API()
        x = DBora.QueryDB("select s.SVC_NUMBER from dbvop.svc_number s        where  s.svc_number_status='10' and s.svc_number like '1709044%'        and rownum <=1")
        # print x
    finally:
        DBora.close()