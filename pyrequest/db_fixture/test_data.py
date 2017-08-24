# -*- coding:utf-8 -*-
__author__ = 'XT'
import sys, os
path_db_fixture = os.path.dirname(__file__)
# print path_db_fixture
sys.path.append(path_db_fixture)
# print sys.path
from mysql_db import DB
datas = {
    '`t_user_function`':[
    {'`user_id`': '1', '`func_code`': '2000'},
    {'`user_id`': '2', '`func_code`': '2001'}
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
    datas = {
        '`t_user_function`':[
        {'`user_id`': '1', '`func_code`': '2000'},
        {'`user_id`': '2', '`func_code`': '2001'}
        ]
    }
    del_data(datas)
    init_data(datas)