# -*- coding:utf-8 -*-
__author__ = 'XT'

import sys
from pymysql import connect, cursors
import os
parentdir = os.path.dirname(__file__)
sys.path.insert(0, parentdir)

from time import ctime
import configparser as cparser

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf_billing", "host")
port = cf.get("mysqlconf_billing", "port")
db = cf.get("mysqlconf_billing", "db_name")
user = cf.get("mysqlconf_billing", "user")
password = cf.get("mysqlconf_billing", "password")

logPath = parentdir + "/error.log"

class DB():
    """docstring for DB"""
    def __init__(self):
        try:
            self.conn = connect(host = host, port=int(port), user = user, password = password, db = db, charset = 'utf8mb4', cursorclass = cursors.DictCursor)
        except OperationalError as e:
            print ('MySQL Error %d: %s' % (e.args[0], e.args[1]))
    def close(self):
        self.conn.close()
        
    def Select_one(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception,e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    Select_one     "+str(e)+"    %s    "%ctime()+os.linesep)

    def Update(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
        except Exception,e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    Update     "+str(e)+"    %s    "%ctime()+os.linesep)

    def Delete(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
        except Exception,e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    Delete     "+str(e)+"    %s    "%ctime()+os.linesep)

    def Select_All(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception,e:
            with open(logPath,"a") as obj:
                obj.writelines(__name__ + "    Select_All     "+str(e)+"    %s    "%ctime()+os.linesep)

if __name__ == "__main__":
    db=DB()
    print db.Select_All("SELECT * FROM `sms_file`")
    db.close()

