# -*- coding:utf-8 -*-
__author__ = 'XT'
import sys, os
path_db_fixture = os.path.dirname(__file__)
# print path_db_fixture
sys.path.append(path_db_fixture)
# print sys.path
from mysql_db import DB
datas = {
    '`gateway`.`ability_package`':[
            {'`ability_package_id`': '80', '`ability_package_name`': '自动化测试能力包', 'ability_package_icon': '81', '`subscribe_type`':'2','`status`':'1','`describes`':'描述','`crt_uid`':'1','`crt_time`':"2017-08-31 14:47:58",'`remark`':'备注'},
            {'`ability_package_id`': '81', '`ability_package_name`': '自动化测试能力包', 'ability_package_icon': '81', '`subscribe_type`':'2','`status`':'0','`describes`':'描述','`crt_uid`':'1','`crt_time`':"2017-08-31 14:47:58",'`remark`':'备注'}
            ]
}
def init_data(datas):
    db = DB()
    for table,data in datas.items():
        for d in data:
            db.insert(table, d)
    db.close()

def del_data(datas):
    db=DB()
    for table,data in datas.items():
        for d in data:
            db.delete(table, d)
    db.close()
if __name__ == '__main__':
    init_data(datas)
    del_data(datas)