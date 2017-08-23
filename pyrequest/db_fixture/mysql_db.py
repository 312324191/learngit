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

host = cf.get("mysqlconf_billing", "host")
port = cf.get("mysqlconf_billing", "port")
db = cf.get("mysqlconf_billing", "db_name")
user = cf.get("mysqlconf_billing", "user")
password = cf.get("mysqlconf_billing", "password")
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
    def clear(self, table_name):
        """
        table_name:表名字
        """
        real_sql = 'delete from '+ table_name + ';'
        with self.conn.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            cursor.execute(real_sql)
        self.conn.commit()
    def insert(self, table_name, table_data):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
    def delete(self,table_name,table_data):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        list_01 = []
        for key in table_data:
            strs =" and "+str(key) +"= "+ str(table_data[key])
            list_01.append(strs)
        real_sql = "delete from " + table_name + " where 1=1 " + ''.join(list_01)
        # print real_sql
        with self.conn.cursor() as cursor:
           cursor.execute(real_sql)
        self.conn.commit()
    def update(self,table_name,table_set,table_data):
        """
        table_name:表名字
        table_set:{字段:内容}
        table_data:{字段:内容}
        """
        data = []
        for key in table_data:
            strs =" and "+str(key) +"= '"+ str(table_data[key])+"'"
            data.append(strs)

        setu = []
        if len(table_set)!=1:
            for key in table_set:
                strs =" , "+str(key) +"= '"+ str(table_set[key])+"'"
                setu.append(strs)
        elif len(table_set)==1:
        	strs =str(''.join(table_set.keys())) +"= '"+ table_set[str(''.join(table_set.keys()))]+"'"
        	setu.append(strs)

        real_sql = "UPDATE " + table_name + " set " + ''.join(setu)[2:] + " where 1=1 " + ''.join(data)
        # print real_sql
        with self.conn.cursor() as cursor:
           cursor.execute(real_sql)
        self.conn.commit()
    def select_one(self,table_name,table_data):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        list_01 = []
        for key in table_data:
            strs =" and "+str(key) +"= '"+ str(table_data[key])+"'"
            list_01.append(strs)
        real_sql = "select * from " + table_name + " where 1=1 " + ''.join(list_01)
        print real_sql
        with self.conn.cursor() as cursor:
           cursor.execute(real_sql)
        return cursor.fetchone()
    def select_all(self,table_name,table_data):
        """
        table_name:表名字
        table_data:{字段:内容}
        """
        list_01 = []
        for key in table_data:
            strs =" and "+str(key) +"= '"+ str(table_data[key])+"'"
            list_01.append(strs)
        real_sql = "select * from " + table_name + " where 1=1 " + ''.join(list_01)
        # print real_sql
        with self.conn.cursor() as cursor:
           cursor.execute(real_sql)
        return cursor.fetchall()
    def close(self):
        self.conn.close()
if __name__ == '__main__':
    db = DB()
    table_name = "`sms_file`"
    data = {'`user_name`': 'ApiRoott'}
    # setu ={"`name`":'5'}
    # db.clear(table_name)
    # db.insert(table_name, data)
    print db.select_all(table_name=table_name, table_data=data)
    db.close()
