#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'XT'
from time import strftime
import os, sys
import random

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_fixture"

sys.path.append(file_path)

import mysql_db
from oracle_db import BD_oracle_API, BD_oracle_PZ, BD_oracle_TJ

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)

tenthousand = cf.get("Standard_ten_thousand_number", "Section_No")

import logging

class Standard_number(BD_oracle_API):
    """docstring for Verifying_Point"""
    def __init__(self, tenthousand_num=None):
        super(Standard_number, self).__init__()
        if tenthousand_num is None:
            global tenthousand
            self.tenthousand = tenthousand
        else:
            self.tenthousand = tenthousand_num
    def Svc_num(self):
        # logging.debug('This is debug message self.tenthousand : %s' % self.tenthousand)
        sql = "select s.SVC_NUMBER from dbvop.svc_number s\
        where  s.svc_number_status='10' and s.svc_number like '%s%%'\
        and rownum <=1" % self.tenthousand
        # logging.debug('This is debug message sql : %s' % sql)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def Im_Icd(self):
        sql = "select i.imsi,ic.ICCID from dbvop.iccid ic\
        right JOIN dbvop.imsi i on i.ICCID_ID=ic.ICCID_ID and i.imsi_status='20' \
        and i.ten_thousand_segment = '%s' where ic.iccid_status='10'\
        and rownum <=1" % self.tenthousand
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def White_Im_Icd(self):
        sql_imsi = "select imsi from dbvop.imsi i \
        where i.imsi_status='10' and i.ten_thousand_segment='%s'and rownum <=1" % self.tenthousand
        rep_sql_imsi = self.GetDatas_QueryDB(sql_imsi)

        sql_iccid = "select to_char(ICCID) from dbvop.iccid ic where  ic.iccid_status='10' \
        and  usim_type=1 and ic.mvno_business_mark in (select i.MVNO_BUSINESS_MARK \
        from dbvop.imsi i where i.imsi_status='10' \
        and i.ten_thousand_segment='%s') and rownum <=1" % self.tenthousand
        rep_sql_iccid = self.GetDatas_QueryDB(sql_iccid)
        return rep_sql_imsi[0][0], rep_sql_iccid[0][0]

class Verifying_Point(BD_oracle_API):
    """docstring for Verifying_Point"""
    def __init__(self, timestamp):
        super(Verifying_Point, self).__init__()
        # timestamp  'YYYY-MM-DD hh24:mi:ss'
        self.timestamp = timestamp
    def Service_Order(self, mvno_service_order_no):
        # 根据流水号查出service_order_id用于其他表查询
        sql = "select s.service_order_id,s.mvno_user_id,s.bss_service_order_no,s.service_order_status,\
        s.service_order_proc_status,to_char(s.service_order_lanch_time,'YYYY-MM-DD hh24:mi:ss' ),\
        to_char(s.service_order_accept_time,'YYYY-MM-DD hh24:mi:ss'), s.service_class_code,s.user_type \
        from dbvop.service_order s where mvno_service_order_no = '%s'" % mvno_service_order_no
        rep_sql = self.GetDatas_QueryDB(sql)
        # print rep_sql
        if len(rep_sql) != 0:
            self.service_order_id = rep_sql[0][0]
            self.mvno_user_id =  rep_sql[0][1]
        return rep_sql

    def order_service_inst(self):
        # 依赖于Service_Order传下来的self.service_order_id
        sql = "select SERVICE_INST, ACTION_TYPE, to_char(SERVICE_ORDER_LANCH_TIME,'YYYY-MM-DD hh24:mi:ss' )\
        from dbvop.order_service_inst osi \
        where osi.service_order_id='%s' order by SERVICE_INST " % (self.service_order_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def bss_order_service_inst(self):
        sql = "select s.property_key,s.prop_action_type,s.property_value, SERVICE_INST, ACTION_TYPE, to_char(SERVICE_ORDER_LANCH_TIME,'YYYY-MM-DD hh24:mi:ss' ) \
        from dbvop.bss_order_service_inst s \
        where s.service_order_id='%s'" % self.service_order_id
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def order_prod_subscribe(self):
        sql = "select b.product_id,b.prod_action_type,b.mvno_business_mark, to_char(SERVICE_ORDER_LANCH_TIME,'YYYY-MM-DD hh24:mi:ss' )  \
        from dbvop.order_prod_subscribe b where b.service_order_id='%s' " % (self.service_order_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def order_discnt_subscribe(self):
        sql = "select DISCNT_ACTION_TYPE, to_char(SERVICE_ORDER_LANCH_TIME,'YYYY-MM-DD hh24:mi:ss' ), DISCNT_ID\
        from dbvop.order_discnt_subscribe a \
        where  a.service_order_id='%s' order by DISCNT_ID" % (self.service_order_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def service_order_back(self):
        sql = "select s.service_order_push_status,s.feedback_result,\
        to_char(s.bss_svc_order_cplt_time,'yyyymmdd hh24miss') \
        from dbvop.service_order_back s \
        where s.service_order_id='%s'" % (self.service_order_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def service_inst_subscribe(self):
        sql = "select to_char(s.order_time,'yyyymmdd hh24miss'),s.service_inst_status,\
        s.service_class_code,s.last_mvno_service_order_no,SERVICE_INST \
        from dbvop.service_inst_subscribe s \
        where s.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def bss_inst_subscribe(self):
        sql = "select b.property_key,b.property_value,SERVICE_INST,to_char(order_time,'yyyymmdd hh24miss') \
        from dbvop.bss_inst_subscribe b \
        where b.mvno_user_id='%s' " % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def prod_subscribe(self):
        sql = "select s.product_id,to_char(s.order_time,'yyyymmdd hh24miss'),\
        s.last_mvno_service_order_no,s.mvno_business_mark \
        from dbvop.prod_subscribe s where s.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def discnt_subscribe(self):
        sql = "select DISCNT_ID, PROD_PACKAGE_ID from dbvop.discnt_subscribe where prod_subscribe_id=\
        (select PROD_SUBSCRIBE_ID from dbvop.prod_subscribe where mvno_user_id='%s' )\
        order by DISCNT_ID" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def life_Imsi(self):
        sql = "select l.imsi,to_char(l.eff_date,'yyyymmdd hh24miss'),\
        l.eff_flag,l.mvno_business_mark,to_char(EXP_DATE,'yyyymmdd hh24miss') \
        from dbvop.life_imsi l where l.user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql

    def Info_User(self):
        sql = "select to_char(i.stop_date,'YYYYMMDD HH24MISS'),\
        to_char(i.create_date,'yyyymmdd hh24miss'),VALID_FLAG,USER_STATUS,user_type\
        from dbvop.info_user i where i.user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def Life_User_Product(self):
        sql = "select EFF_FLAG, to_char(EFF_DATE,'YYYYMMDD HH24MISS') ,\
        to_char(EXP_DATE,'YYYYMMDD HH24MISS'), to_char(CREATE_DATE,'YYYYMMDD HH24MISS')\
        from dbvop.Life_User_Product l \
        where l.user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def LIFE_USER_PRODUCT_DISCT(self):
        sql = "select EFF_FLAG, to_char(EFF_DATE,'YYYYMMDD HH24MISS') ,\
        to_char(EXP_DATE,'YYYYMMDD HH24MISS'), to_char(CREATE_DATE,'YYYYMMDD HH24MISS')\
        from dbvop.LIFE_USER_PRODUCT_DISCT s \
        where s.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def I_Mvno_User_A(self):
        sql = "select * from dbvop.i_mvno_user_a i\
        where i.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def q_mvno_user_a(self):
        sql = "select Count(1) from dbvop.q_mvno_user_a v \
        where v.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def q_mvno_user_b(self):
        sql = "select Count(1) from dbvop.q_mvno_user_b v \
        where v.mvno_user_id='%s' " % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def t_mvno_user(self):
        sql = "select Count(1) from dbvop.t_mvno_user v \
        where v.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def t_mvno_user_a(self):
        sql = "select Count(1) from dbvop.t_mvno_user_a v \
        where v.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def t_mvno_user_b(self):
        sql = "select Count(1) from dbvop.t_mvno_user_b v \
        where v.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def life_mvno_user(self):
        sql = "select Count(1) from dbvop.life_mvno_user v \
        where v.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def imsi(self, imsi):
        sql = "select i.imsi_status from dbvop.imsi i where i.imsi='%s'" % (ims)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def life_user(self, imsi):
        sql = "select l.user_status,l.user_type,l.valid_flag,l.service_class_code,\
        to_char(l.eff_date,'yyyymmdd hh24miss'),to_char(l.exp_date,'YYYYMMDD') \
        from dbvop.life_user l where l.mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def BSS_order_no_mvno_mapping(self, bss_service_order_no):
        sql = "select to_char(b.service_order_lanch_time,'YYYY-MM-DD hh24:mi:ss'),\
        b.mvno_business_mark,b.bss_service_order_no_state \
        from dbvop.BSS_order_no_mvno_mapping b \
        where b.bss_service_order_no='%s'" % (bss_service_order_no)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def mvno_user(self):
        sql = "select to_char(DEAL_TIME,'yyyymmdd hh24miss'), MVNO_USER_TYPE, MVNO_USER_STATUS\
        from dbvop.mvno_user where mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def PAY_USER_REL(self):
        sql = "select EFF_FLAG,to_char(EFF_DATE,'YYYYMMDD HH24MISS'),to_char(EXP_DATE,'YYYYMMDD HH24MISS')\
        from dbvop.PAY_USER_REL where user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
    def Life_User_Type(self):
        sql = "select MVNO_USER_TYPE,to_char(BEGIN_TIME,'YYYYMMDD HH24MISS'),to_char(END_TIME,'YYYYMMDD HH24MISS')\
        from dbvop.LIFE_USER_TYPE where mvno_user_id='%s'" % (self.mvno_user_id)
        rep_sql = self.GetDatas_QueryDB(sql)
        return rep_sql
if __name__ == '__main__':
    # vp = Verifying_Point('YYYY-MM-DD hh24:mi:ss')
    # print vp.Service_Order('123123123123')
    # vp.close()

    Sn = Standard_number()
    print Sn.Svc_num()
    print Sn.Im_Icd()
    print Sn.White_Im_Icd()
    Sn.close()