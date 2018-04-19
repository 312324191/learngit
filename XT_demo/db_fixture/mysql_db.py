# -*- coding:utf-8 -*-
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser as cparser
__author__ = 'XT'

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf_esbcfgdb", "host")
port = cf.get("mysqlconf_esbcfgdb", "port")
db = cf.get("mysqlconf_esbcfgdb", "db_name")
user = cf.get("mysqlconf_esbcfgdb", "user")
password = cf.get("mysqlconf_esbcfgdb", "password")
# print host,port,db,user,password
#==== 封装mysql基本操作 ====
class DB:
    """docstring for DB"""
    def __init__(self):
        try:
            self.conn = connect(host = host, port=int(port), user = user, password = password, db = db, charset = 'utf8mb4', cursorclass = cursors.DictCursor)
            # print self.conn
        except OperationalError as e:
            print ('MySQL Error %d: %s' % (e.args[0], e.args[1]))
    def select_one(self,sql):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        with self.conn.cursor() as cursor:
           cursor.execute(sql)
        return cursor.fetchone()
    def select_all(self,sql):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        with self.conn.cursor() as cursor:
           cursor.execute(sql)
        return cursor.fetchall()
    def close(self):
        self.conn.close()
if __name__ == '__main__':
    try:
        db = DB()
        sql = "select ma.MVNO_KEY as mvnokey from esbcfgdb.mvno_app ma where ma.MVNO_BUSINESS_MARK='%s'" % 'VOPI'
        print db.select_one(sql)
    except Exception as e:
        raise e
    finally:
        db.close()
    
    

