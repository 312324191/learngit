# -*- coding:utf-8 -*-
__author__ = 'XT'
import sys, os
path_db_fixture = os.path.dirname(__file__)
# print path_db_fixture
sys.path.append(path_db_fixture)
# print sys.path
from mysql_db import DB
datas = {
    'sign_event':[
    {'`name`': '1', '`limit`': '2000', '`status`': '1', '`address`': '1', '`start_time`': '2017-8-24 22:34:59','`create_time`': '2017-8-24 22:34:59'},
    {'`name`': '2', '`limit`': '2000', '`status`': '1', '`address`': '1', '`start_time`': '2017-8-24 22:34:59','`create_time`': '2017-8-24 22:34:59'},
    {'`name`': '3', '`limit`': '2000', '`status`': '1', '`address`': '1', '`start_time`': '2017-8-24 22:34:59','`create_time`': '2017-8-24 22:34:59'},
    {'`name`': '4', '`limit`': '2000', '`status`': '1', '`address`': '1', '`start_time`': '2017-8-24 22:34:59','`create_time`': '2017-8-24 22:34:59'},
    {'`name`': '5', '`limit`': '2000', '`status`': '1', '`address`': '1', '`start_time`': '2017-8-24 22:34:59','`create_time`': '2017-8-24 22:34:59'}
    ],
    'sign_guest':[
    {'`realname`': '2000', '`phone`': '1', '`email`': '1', '`sign`': '1','`event`': '1'},
    {'`realname`': '2000', '`phone`': '1', '`email`': '1', '`sign`': '1','`event`': '1'},
    {'`realname`': '2000', '`phone`': '1', '`email`': '1', '`sign`': '1','`event`': '1'},
    {'`realname`': '2000', '`phone`': '1', '`email`': '1', '`sign`': '1','`event`': '1'},
    {'`realname`': '2000', '`phone`': '1', '`email`': '1', '`sign`': '1','`event`': '1'}
    ]
}
def init_data():
    db = DB()
    for table,data in datas.items():
        # del_data()
        for d in data:
            db.insert(table, d)
    db.close()

def del_data():
    db=DB()
    for table,data in datas.items():
        for d in data:
            db.delete(table, d)
    db.close()
if __name__ == '__main__':
    init_data()
    del_data()