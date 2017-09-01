# -*- coding:utf-8 -*-
__author__ = 'XT'
import unittest
import requests
import os, sys, json
parentdir = str(os.path.dirname(os.path.dirname(__file__)))
parentdir =parentdir.replace('\\', '/')
sys.path.append(parentdir+'/db_fixture')
import mysql_assert, test_data
from datetime import *

import configparser as cparser
from requests_toolbelt import MultipartEncoder

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)
url = cf.get("Capability_portal", "url")

class AbilityHomePage(unittest.TestCase):
    def setUp(self):
        self.db = mysql_assert.DB()
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ten_minutes_ago = (datetime.now()-timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        ten_minutes_later = (datetime.now()+timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        sql_max = "select max(ability_id) from gateway.ability"
        ability_id = int(self.db.Select_one(sql_max).get('max(ability_id)'))+1
        self.datas = {
            '`gateway`.`banner`':[
            {'`banner_no`': '81', '`banner_img`': '1', '`banner_url`': 'www.baidu.com', '`status`': '3', '`crt_uid`':'0','`active_time`':ten_minutes_ago,'`active_time`':ten_minutes_ago,'`remark`':'备注','`end_time`':ten_minutes_later}
            ],
            '`gateway`.`tf_f_upgrade_notice`':[
            {'`notice_id`': ability_id, '`notice_state`': '00', '`notice_title`': 'test_01', '`notice_type`':'0','`notece_desc`':'自动化测试数据','`attachment_file_id`':'1', '`start_time`':ten_minutes_ago, '`end_time`':ten_minutes_later, '`crt_uid`':'2', '`create_time`':now_time,'`update_uid`':'1', '`update_uid`':'1'},
            {'`notice_id`': ability_id+1, '`notice_state`': '00', '`notice_title`': 'test_02', '`notice_type`':'1','`notece_desc`':'自动化测试数据','`attachment_file_id`':'1', '`start_time`':ten_minutes_ago, '`end_time`':ten_minutes_later, '`crt_uid`':'2', '`create_time`':now_time,'`update_uid`':'1', '`update_uid`':'1'},
            {'`notice_id`': ability_id+2, '`notice_state`': '00', '`notice_title`': 'test_03', '`notice_type`':'2','`notece_desc`':'自动化测试数据','`attachment_file_id`':'1', '`start_time`':ten_minutes_ago, '`end_time`':ten_minutes_later, '`crt_uid`':'2', '`create_time`':now_time,'`update_uid`':'1', '`update_uid`':'1'},
            {'`notice_id`': ability_id+3, '`notice_state`': '00', '`notice_title`': 'test_04', '`notice_type`':'2','`notece_desc`':'自动化测试数据','`attachment_file_id`':'1', '`start_time`':ten_minutes_ago, '`end_time`':ten_minutes_ago, '`crt_uid`':'2', '`create_time`':now_time,'`update_uid`':'1', '`update_uid`':'1'},
            {'`notice_id`': ability_id+4, '`notice_state`': '00', '`notice_title`': 'test_05', '`notice_type`':'2','`notece_desc`':'自动化测试数据','`attachment_file_id`':'1', '`start_time`':ten_minutes_later, '`end_time`':ten_minutes_later, '`crt_uid`':'2', '`create_time`':now_time,'`update_uid`':'1', '`update_uid`':'1'}
            ],
            '`gateway`.`ability_recommend`':[
            {'`ability_id`': ability_id, '`ability_name`':'自动化测试推荐', '`ability_eng_name`': 'test_01', '`crt_uid`':'0','`deal_time`':now_time},
            ],
            '`gateway`.`ability`':[
            {'`ability_id`': ability_id, '`ability_provider_id`': '00', '`ability_name`': '自动化测试推荐', '`ability_eng_name`':'test_01','`ability_mark`':'test_01','`ability_icon`':'能力icon','`bill_type_id`':'1','`ability_category`':'1','`ability_protocol`':'1','`ability_msg_format`':'4','`status`':'4','`sys_status`':'0','`ability_ver`':'V1.0',
            '`traffic_control`':'12','`traffic_control2`':'12','`describes`':'描述','`wsdl_file_id`':'1','`wsdl_file_id2`':'1','`api_doc_file_id`':'1','`attachment_file_id`':'1','`ablitity_explain_file_id`':'1','`in_param_explain_file_id`':'1','`out_param_explain_file_id`':'1','`crt_time`':ten_minutes_ago,
            '`crt_uid`':'1','`remark`':'备注', '`ability_access_sandbox_pathl`':'ability_access_sandbox_pathl','`ability_access_product_pathl`':'ability_access_product_pathl','`ability_provider_sandbox_url`':'ability_provider_sandbox_url','`sandbox_url_remark`':'sandbox_url_remark','`ability_provider_product_url`':'ability_provider_product_url','`product_url_remark`':'product_url_remark',
            '`operateor_belong`':'1','`update_uid`':'1','`update_time`':now_time,'`ability_path`':'ability_path'},
            {'`ability_id`': ability_id+1, '`ability_provider_id`': '00', '`ability_name`': '自动化测试推荐', '`ability_eng_name`':'test_01','`ability_mark`':'test_01','`ability_icon`':'能力icon','`bill_type_id`':'1','`ability_category`':'1','`ability_protocol`':'1','`ability_msg_format`':'4','`status`':'3','`sys_status`':'0','`ability_ver`':'V1.0',
            '`traffic_control`':'12','`traffic_control2`':'12','`describes`':'描述','`wsdl_file_id`':'1','`wsdl_file_id2`':'1','`api_doc_file_id`':'1','`attachment_file_id`':'1','`ablitity_explain_file_id`':'1','`in_param_explain_file_id`':'1','`out_param_explain_file_id`':'1','`crt_time`':ten_minutes_ago,
            '`crt_uid`':'1','`remark`':'备注', '`ability_access_sandbox_pathl`':'ability_access_sandbox_pathl','`ability_access_product_pathl`':'ability_access_product_pathl','`ability_provider_sandbox_url`':'ability_provider_sandbox_url','`sandbox_url_remark`':'sandbox_url_remark','`ability_provider_product_url`':'ability_provider_product_url','`product_url_remark`':'product_url_remark',
            '`operateor_belong`':'1','`update_uid`':'1','`update_time`':now_time,'`ability_path`':'ability_path'},
            {'`ability_id`': ability_id+2, '`ability_provider_id`': '00', '`ability_name`': '自动化测试推荐', '`ability_eng_name`':'test_01','`ability_mark`':'test_01','`ability_icon`':'能力icon','`bill_type_id`':'1','`ability_category`':'1','`ability_protocol`':'1','`ability_msg_format`':'4','`status`':'2','`sys_status`':'0','`ability_ver`':'V1.0',
            '`traffic_control`':'12','`traffic_control2`':'12','`describes`':'描述','`wsdl_file_id`':'1','`wsdl_file_id2`':'1','`api_doc_file_id`':'1','`attachment_file_id`':'1','`ablitity_explain_file_id`':'1','`in_param_explain_file_id`':'1','`out_param_explain_file_id`':'1','`crt_time`':ten_minutes_ago,
            '`crt_uid`':'1','`remark`':'备注', '`ability_access_sandbox_pathl`':'ability_access_sandbox_pathl','`ability_access_product_pathl`':'ability_access_product_pathl','`ability_provider_sandbox_url`':'ability_provider_sandbox_url','`sandbox_url_remark`':'sandbox_url_remark','`ability_provider_product_url`':'ability_provider_product_url','`product_url_remark`':'product_url_remark',
            '`operateor_belong`':'1','`update_uid`':'1','`update_time`':now_time,'`ability_path`':'ability_path'},
            {'`ability_id`': ability_id+3, '`ability_provider_id`': '00', '`ability_name`': '自动化测试推荐', '`ability_eng_name`':'test_01','`ability_mark`':'test_01','`ability_icon`':'能力icon','`bill_type_id`':'1','`ability_category`':'1','`ability_protocol`':'1','`ability_msg_format`':'4','`status`':'1','`sys_status`':'0','`ability_ver`':'V1.0',
            '`traffic_control`':'12','`traffic_control2`':'12','`describes`':'描述','`wsdl_file_id`':'1','`wsdl_file_id2`':'1','`api_doc_file_id`':'1','`attachment_file_id`':'1','`ablitity_explain_file_id`':'1','`in_param_explain_file_id`':'1','`out_param_explain_file_id`':'1','`crt_time`':ten_minutes_ago,
            '`crt_uid`':'1','`remark`':'备注', '`ability_access_sandbox_pathl`':'ability_access_sandbox_pathl','`ability_access_product_pathl`':'ability_access_product_pathl','`ability_provider_sandbox_url`':'ability_provider_sandbox_url','`sandbox_url_remark`':'sandbox_url_remark','`ability_provider_product_url`':'ability_provider_product_url','`product_url_remark`':'product_url_remark',
            '`operateor_belong`':'1','`update_uid`':'1','`update_time`':now_time,'`ability_path`':'ability_path'}
            ],
            '`gateway`.`ability_package_relation`':[
            {'`ability_package_id`': ability_id, '`ability_rule_id`': '2', '`ability_id`': '81', '`charge_rule_id`':'2','`ability_package_name`':'自动化测试能力包','`describes`':'描述','`crt_uid`':'1','`crt_time`':now_time,'`remark`':'备注','`ability_category`':'3'},
            {'`ability_package_id`': ability_id+1, '`ability_rule_id`': '2', '`ability_id`': '81', '`charge_rule_id`':'2','`ability_package_name`':'自动化测试能力包','`describes`':'描述','`crt_uid`':'1','`crt_time`':now_time,'`remark`':'备注','`ability_category`':'3'}
            ],
            '`gateway`.`ability_package`':[
            {'`ability_package_id`': ability_id, '`ability_package_name`': '自动化测试能力包', 'ability_package_icon': '1', '`subscribe_type`':'2','`status`':'1','`describes`':'描述','`crt_uid`':'1','`crt_time`':now_time,'`remark`':'备注'},
            {'`ability_package_id`': ability_id+1, '`ability_package_name`': '自动化测试能力包', 'ability_package_icon': '1', '`subscribe_type`':'2','`status`':'0','`describes`':'描述','`crt_uid`':'1','`crt_time`':now_time,'`remark`':'备注'}
            ]
        }
        # print datas
        test_data.init_data(self.datas)
        global url
        self.url = url +"/abilityHomePage"
        self.data = {"username":"admin", "name":"xt", "tenantId":"1", "userId":"2", "deptId":"3"}
    def tearDown(self):
        test_data.del_data(self.datas)
        self.db.close()
        print self.res.content

    def test_Normal_01(self):
        """ 未登录访问首页 """
        data = json.dumps(self.data)
        self.res = requests.post(url = self.url, data = data)
        rsp = self.res.json()
        self.assertEqual(rsp.get("respCode"),'0000')
        self.assertEqual(rsp.get("respDesc"),u'操作成功')
        self.assertTrue(rsp.has_key("banners"))
        self.assertTrue(rsp.has_key("notices"))
        self.assertTrue(rsp.has_key("abilityRecommend"))
        self.assertTrue(rsp.has_key("abilityPackage"))
        self.assertTrue(rsp.has_key("baseAbility"))
        self.assertTrue(rsp.has_key("valueAddAbility"))
        self.assertTrue(rsp.has_key("jasper"))
        self.assertTrue(rsp.has_key("beehive"))
        # 轮播图查询。
        sql_01 = "select b.`banner_url`,b.`banner_img`,b.`banner_no` from gateway.banner b where b.`active_time`<=sysdate() and b.end_time>=SYSDATE() limit 3"
        rsp_sql = self.db.Select_All(sql_01)
        num = 0
        for i in rsp.get("banners"):
            self.assertEqual(i.get("bannerUrl"), rsp_sql[num].get("banner_url"))
            self.assertEqual(i.get("bannerImg"), rsp_sql[num].get("banner_img"))
            self.assertEqual(i.get("bannerNo"), rsp_sql[num].get("banner_no"))
            num+=1
        # 公告查询
        sql_02 = "SELECT b.`notice_title`,b.`notice_id`,b.`notece_desc` FROM gateway.tf_f_upgrade_notice b WHERE b.`start_time`<=SYSDATE() AND b.end_time>=SYSDATE() AND  b.`notice_type` IN ('1','2')"
        rsp_sql = self.db.Select_All(sql_02)
        num = 0
        for i in rsp.get("notices"):
            self.assertEqual(i.get("noticeId"), rsp_sql[num].get("notice_id"))
            self.assertEqual(i.get("noticeTitle"), rsp_sql[num].get("notice_title"))
            self.assertEqual(i.get("noteceDesc"), rsp_sql[num].get("notece_desc"))
            num+=1
        # 能力推荐查询
        sql_03 = "SELECT a.`ability_id`,a.`ability_name`,a.`describes` FROM `gateway`.`ability` a, `gateway`.`ability_recommend` b WHERE a.`ability_id`=b.`ability_id` ORDER BY a.`ability_id` DESC LIMIT 4"
        rsp_sql = self.db.Select_All(sql_03)
        # print rsp_sql
        num = 0
        for i in rsp.get("abilityRecommend"):
            self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
            self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
            self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
            num+=1
        # 能力包查询
        sql_04 = "SELECT   a.`ability_id`, a.`ability_name`, a.`describes`  FROM `gateway`.`ability` a WHERE ability_category=2 AND a.`status`=4 LIMIT 5"
        rsp_sql = self.db.Select_All(sql_04)
        # print rsp_sql
        num = 0
        for i in rsp.get("valueAddAbility"):
            self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
            self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
            self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
            num+=1
        # 基础能力查询
        # sql_05 = "SELECT   a.`ability_id`, a.`ability_name`, a.`describes`  FROM `gateway`.`ability` a WHERE ability_category=1 AND a.`status`=4 LIMIT 5"
        # rsp_sql = self.db.Select_All(sql_05)
        # # print rsp_sql
        # num = 0
        # for i in rsp.get("baseAbility"):
        #     self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
        #     self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
        #     self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
        #     num+=1
        # 增值能力查询
        # sql_06 = "SELECT   a.`ability_id`, a.`ability_name`, a.`describes`  FROM `gateway`.`ability` a WHERE ability_category=2 AND a.`status`=4 ORDER BY a.`ability_id` DESC LIMIT 5"
        # rsp_sql = self.db.Select_All(sql_06)
        # # print rsp_sql
        # num = 0
        # for i in rsp.get("valueAddAbility"):
        #     self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
        #     self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
        #     self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
        #     num+=1
        # jasper能力查询
        sql_07 = "SELECT   a.`ability_id`, a.`ability_name`, a.`describes`  FROM `gateway`.`ability` a WHERE ability_category=3 AND a.`status`=4 ORDER BY a.`ability_id` DESC LIMIT 5"
        rsp_sql = self.db.Select_All(sql_07)
        # print rsp_sql
        num = 0
        for i in rsp.get("jasper"):
            self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
            self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
            self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
            num+=1
        # 蜂窝能力查询
        sql_08 = "SELECT   a.`ability_id`, a.`ability_name`, a.`describes`  FROM `gateway`.`ability` a WHERE ability_category=4 AND a.`status`=4 ORDER BY a.`ability_id` DESC LIMIT 5"
        rsp_sql = self.db.Select_All(sql_08)
        # print rsp_sql
        num = 0
        for i in rsp.get("beehive"):
            self.assertEqual(i.get("abilityId"), rsp_sql[num].get("ability_id"))
            self.assertEqual(i.get("abilityName"), rsp_sql[num].get("ability_name"))
            self.assertEqual(i.get("describes"), rsp_sql[num].get("describes"))
            num+=1
if __name__ == '__main__':
    unittest.main()
