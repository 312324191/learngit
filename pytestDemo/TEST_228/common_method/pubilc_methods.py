#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'XT'
import os, sys, json

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')

file_path = base_dir + "/db_fixture"
sys.path.append(file_path)

jar_path = base_dir + "/lib"
sys.path.append(jar_path)

log_path = base_dir + "/log"
sys.path.append(log_path)
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= log_path + r'\DUBEG.log',
                filemode='w')
import jpype
import hashlib
import requests
# from random import randint
from time import strftime, sleep
import re

#==== 读取 db_config.ini 文件设置 ====
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

import configparser as cparser
cf = cparser.ConfigParser()
cf.read(file_path)

ip = cf.get("API_url_Edition", "ip")
host = cf.get("API_url_Edition", "host")
Route = cf.get("API_url_Edition", "Route")
Route_P = cf.get("API_url_Edition", "Route_P")
Route_V = cf.get("API_url_Edition", "Route_V")
Route_ZB = cf.get("API_url_Edition", "Route_ZB")
Route_PT = cf.get("API_url_Edition", "Route_PT")
Route_VT = cf.get("API_url_Edition", "Route_VT")
Route_RT = cf.get("API_url_Edition", "Route_RT")

class Url_Class(object):
    """docstring for Url_Class"""
    def __init__(self):
        global ip, host
        self.url = "http://%s:%s/" % (ip, host)
    def url_P(self):
        global Route_P
        return self.url+Route_P
    def url_V(self):
        global Route_V
        return self.url+Route_V
    def url_ZB(self):
        global Route_ZB
        return self.url+Route_ZB    
    def url_More(self):
        global Route
        return self.url+Route
    def url_PT(self):
        global Route_PT
        return self.url+Route_PT
    def url_VT(self):
        global Route_VT
        return self.url+Route_VT
    def url_RT(self):
        global Route_RT
        return self.url+Route_RT

def jar_name(package, package_classname, Es_package=""):
    # python调用java
    global jar_path
    # 要调用的jar
    jarpath = os.path.join(os.path.abspath('.'), jar_path + package)
    # 要调用的jar包的扩张包
    dependency = os.path.join(os.path.abspath('.'), jar_path + Es_package)
    # 获取jvm环境变量地址
    jvmPath = jpype.getDefaultJVMPath()
    try:
        if not jpype.isJVMStarted():
            # 启动jvm虚拟机
            jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" %jarpath,"-Djava.ext.dirs=%s" %dependency)
        # 执行java代码
        # package + 类名
        JClass = jpype.JClass(package_classname)
        # 实例化类
        instance = JClass()
        # 调用类的的方法名称
        jpype.java.lang.System.out.println(instance.sayHello())
    except Exception as e:
        logging.debug("jvm虚拟机报错：%s" % e)
    finally:
        # 关闭jvm虚拟机
        if not jpype.isJVMStarted():
            jpype.shutdownJVM()

def Format(header):
    # 去掉报文中空格，变成json格式
    return str(header).replace(" ", "").replace("'","\"")

def files(head):
    return {"content":(None, head)}

def Authentication(header):
    '''
    获取报文中head 下sign字段 进行MD5加密后需要大写处理 加密后反向放回sign中 
    json排序 整体MD5加密 再放回sign中  
    '''
    # -------汉字处理不了-----
    # 获取报文中sign字段加密反向大写处理放回sign
    signMD5 = header.get("head").get("sign")
    hl = hashlib.md5()
    hl.update(signMD5.encode(encoding='utf-8'))
    signMD5 = hl.hexdigest().upper()
    header["head"]["sign"] = signMD5

    # json排序从小到大 整体MD5加密 大写处理 反向放回sign
    json_header = json.dumps(header,sort_keys=True)
    json_header = str(json.loads(json_header))
    json_header = json_header.replace(" ","").replace("'", "\"")
    # logging.debug("再次传入加密前：%s %s" % (type(json_header), json_header))

    hl = hashlib.md5()
    hl.update(json_header.encode(encoding='utf-8'))
    signMD5_01 = hl.hexdigest().upper()
    header["head"]["sign"] = signMD5_01
    # 处理一下空格与单引号 变成json格式 拼成files需要的格式
    header = Format(header)
    
    return header

def re_json(rsp_data):
    # 正则截取{}中间内容
    rsp_data = str(rsp_data)
    pattern  = re.compile(r"(\{.*\})") 
    rejson = pattern.search(rsp_data)
    return rejson.group()

def req_post(header):
    # 输入请求报文json
    UC = Url_Class()
    url=UC.url_More()
    head = eval(Authentication(header))
    head = files(Format(head))
    logging.debug("请求报文实体：%s " % head)
    rsp = requests.post(url=url, files=head, verify=False)
    rsp_json = rsp.json()
    logging.debug("响应报文实体：%s " % rsp_json)
    return rsp_json

def req_P(url_Route_P, pid, mid, nc, callback):
    # 请求获取 vid：场次id
    payload = {'pid': pid, 'mid': mid, "nc": nc, "callback": callback}
    rsp = requests.get(url=url_Route_P, params=payload)
    # logging.debug("req_P:%s" % rsp.text)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        rsp_0vid = rsp_dict.get("result")[0].get("vid")
        return rsp_0vid
    except Exception as e:
        raise e

def req_V(url_Route_V, rsp_0vid, nc, mid, callback):
    # 获取区域内票价、套票信息
    payload = {'vid': rsp_0vid, 'nc': nc, "mid": mid, "callback": callback}
    rsp = requests.get(url=url_Route_V, params=payload)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        logging.debug("全量票价信息：%s" % rsp_dict)
        status_list = [x.get("status") for x in rsp_dict.get("areas")]
        for i in range(len(status_list)):
            if rsp_dict.get("areas")[i].get("status") == 1:
                # 获取status状态为1的区域ID
                status_id = rsp_dict.get("areas")[i].get("id")
                break
        # 获取区域内票价信息
        prices = rsp_dict.get("prices")
        logging.debug("票价信息:%s" % prices)
        # 获取区域内套票信息
        tp_prices = rsp_dict.get("tplist")
        logging.debug("套票信息:%s" % tp_prices)
        return status_id, prices, tp_prices
    except Exception as e:
        raise e 

def req_ZB(url_Route_ZB, rsp_0vid, status_id, nc, mid, callback, Ptype=0, num=1,price_id=None):
    # 获取座位id 套票座位id 套票编码
    # Ptype：1自由套 2组合套 0普通票 4特殊票
    payload = {'vid': rsp_0vid, 'aid': status_id, "nc": nc, "mid": mid, "callback": callback,\
    "type": "ri", "id": "","sid": rsp_0vid, "rid": status_id}
    rsp = requests.get(url=url_Route_ZB, params=payload)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        status_list = [x.get("on_sale") for x in rsp_dict.get("result")]
        tp_type_message = []
        for i in range(len(status_list)):
            # tp_id ！="0"  暂时默认为套票  createOrderDate 不为空默认为已售
            if Ptype == 0:
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("symbol_name")== "普通票" and rsp_dict.get("result")[i].get("createOrderDate") is None and rsp_dict.get("result")[i].get("tp_id") == "0":
                    # tp_type_message = rsp_dict.get("result")[i]
                    tp_type_message.append(rsp_dict.get("result")[i])
                    break
            elif Ptype==4:
                if rsp_dict.get("result")[i].get("on_sale") == 0 and rsp_dict.get("result")[i].get("symbol_name")!= "普通票"and rsp_dict.get("result")[i].get("createOrderDate") is None:
                    # tp_type_message = rsp_dict.get("result")[i]
                    tp_type_message.append(rsp_dict.get("result")[i])
                    break
            elif Ptype == 2:
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("tp_id") != "0"  and rsp_dict.get("result")[i].get("createOrderDate") is None:
                    # 获取on_sale状态为1的普通区域信息（包括区域id与票价id）
                    # tp_type_message = rsp_dict.get("result")[i]
                    tp_type_message.append(rsp_dict.get("result")[i])
                    break
            elif Ptype == 1:
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("symbol_name")== "普通票" and rsp_dict.get("result")[i].get("createOrderDate") is None and rsp_dict.get("result")[i].get("tp_id") == "0":
                    tp_type_message.append(rsp_dict.get("result")[i])
        # 座位id与票价id
        logging.debug("座位信息：%s"% tp_type_message)
        if Ptype == 0 or Ptype == 4 :
            tp_type_message = tp_type_message[0]
            rsp_zb_id = []
            rsp_zb_id.append(tp_type_message.get("id"))
            rsp_zb_price_id = tp_type_message.get("price_id")
            tp_type_message = tp_type_message.get("id")
            # 固定套根据套票id反向找出所有套票id
            # 票价id
        elif Ptype == 2:
            # rsp_zb_id = tp_type_message.get("id")
            # 固定套根据套票id反向找出所有套票id
            tp_type_message = tp_type_message[0]
            tp_id = tp_type_message.get("tp_id")
            rsp_zb_id = [x for x in rsp_dict.get("result") if x.get("tp_id")==tp_id]
            rsp_zb_id = [x.get("id") for x in rsp_zb_id]
            rsp_zb_price_id = tp_type_message.get("tp_type_id")
            tp_type_message = tp_type_message.get("tp_id")
            # logging.debug("rsp_zb_id%s" % rsp_zb_id)
            # logging.debug("rsp_zb_price_id%s" % rsp_zb_price_id)
            # logging.debug("tp_type_message%s" % tp_type_message)
        elif Ptype == 1:
            data = [tp_type_message[i] for i in range(len(tp_type_message)) if int(tp_type_message[i].get("price_id"))==int(price_id)]
            rsp_zb_id = [data[i].get("id") for i in range(num)]
            rsp_zb_price_id = data[0].get("tp_type_id")
            tp_type_message = data[0].get("tp_id")
        return rsp_zb_id, rsp_zb_price_id, str(tp_type_message)
    except IndexError as e:
        print("没有找到票种信息")
        raise e
    except Exception as e:
        raise e
 
def price_messages(prices, rsp_zb_price_id, Ptype=0):
    # 传入价格信息或套票价格信息、价格id，Ptype：1自由套 2组合套 0普通票 4特殊票
    logging.debug("价格信息:%s" % prices)
    logging.debug("价格id:%s" % rsp_zb_price_id)
    if Ptype == 0 or Ptype == 4:
        for i in prices:
            if int(i.get('id')) == int(rsp_zb_price_id):
                price = i.get("price")
                price_id = i.get("id")
                break
    elif Ptype == 2:
        for i in prices:
            if int(i.get('type_id')) == int(rsp_zb_price_id):
                price = i.get("price")
                price_id = i.get("type_id")
                break
    elif Ptype == 1:
        for i in prices:
            if int(i.get('price_id')) == int(rsp_zb_price_id):
                price = i.get("price")
                price_id = i.get("type_id")
                break
    return price, price_id

def req_PT(url_Route_PT, pid, mid, nc, callback):
    # http://api.lepiaoyun.com/api/seat/pt?pid=524&nc=30&mid=10&callback=jQuery17205782168972633526_1529911935048;
    # 获取座位id 套票座位id 套票编码
    # Ptype：1自由套 2组合套 0普通票 4特殊票
    payload = {'pid': pid, 'nc': nc, "mid": mid, "callback": callback}
    rsp = requests.get(url=url_Route_PT, params=payload)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        rsp_0vid = rsp_dict.get("vid")
        return rsp_0vid
    except Exception as e:
        raise e

def req_VT(url_Route_VT, rsp_0vid, nc, mid, callback):
    # http://api.lepiaoyun.com/api/seat/vt?vid=3246&nc=30&mid=10&callback=jQuery17205782168972633526_1529911935049
    # 获取区域内票价、套票信息
    payload = {'vid': rsp_0vid, 'nc': nc, "mid": mid, "callback": callback}
    rsp = requests.get(url=url_Route_VT, params=payload)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        logging.debug("全量票价信息：%s" % rsp_dict)
        status_list = [x.get("status") for x in rsp_dict.get("areas")]
        for i in range(len(status_list)):
            if rsp_dict.get("areas")[i].get("status") == 1:
                # 获取status状态为1的区域ID
                status_id = rsp_dict.get("areas")[i].get("id")
                break
        # 获取区域内票价信息
        prices = rsp_dict.get("prices")
        logging.debug("票价信息:%s" % prices)
        # 获取区域内套票信息
        tp_prices = rsp_dict.get("tplist")
        logging.debug("套票信息:%s" % tp_prices)
        return status_id, prices, tp_prices
    except Exception as e:
        raise e 

def req_RT(url_Route_RT, rsp_0vid, status_id, nc, mid, callback, Ptype=0, num=1,price_id=None):
    # http://api.lepiaoyun.com/api/seat/rt?vid=3246&aid=13152&nc=30&mid=10&callback=jQuery17205782168972633526_1529911935050
    # 获取座位id 套票座位id 套票编码
    # Ptype：1自由套 2组合套 0普通票 
    payload = {'vid': rsp_0vid, 'aid': status_id, "nc": nc, "mid": mid, "callback": callback,\
    "type": "ri", "id": "","sid": rsp_0vid, "rid": status_id}
    rsp = requests.get(url=url_Route_RT, params=payload)
    try:
        rsp_str = re_json(rsp.text)
        rsp_dict = json.loads(rsp_str)
        status_list = [x.get("on_sale") for x in rsp_dict.get("result")]
        tp_type_message = []
        for i in range(len(status_list)):
            # tp_id ！="0"  暂时默认为套票  createOrderDate 不为空默认为已售
            if Ptype == 0:
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("tp_id") == "0" and rsp_dict.get("result")[i].get("tp") == 0:
                    # tp_type_message = rsp_dict.get("result")[i]
                    tp_type_message.append(rsp_dict.get("result")[i])
                    break
            elif Ptype == 2:
                if rsp_dict.get("result")[i].get("on_sale") == 1 and rsp_dict.get("result")[i].get("tp") == 1:
                    # 获取on_sale状态为1的普通区域信息（包括区域id与票价id）
                    # tp_type_message = rsp_dict.get("result")[i]
                    tp_type_message.append(rsp_dict.get("result")[i])
                    break
            elif Ptype == 1:
                if rsp_dict.get("result")[i].get("on_sale") == 1  and rsp_dict.get("result")[i].get("tp") == 0:
                    tp_type_message.append(rsp_dict.get("result")[i])
        # 座位id与票价id
        logging.debug("座位信息：%s"% tp_type_message)
        if Ptype == 0 or Ptype == 4 :
            tp_type_message = tp_type_message[0]
            rsp_zb_id = []
            rsp_zb_id.append(tp_type_message.get("id"))
            rsp_zb_price_id = tp_type_message.get("price_id")
            tp_type_message = tp_type_message.get("id")
            # 固定套根据套票id反向找出所有套票id
            # 票价id
        elif Ptype == 2:
            # rsp_zb_id = tp_type_message.get("id")
            # 固定套根据套票id反向找出所有套票id
            tp_type_message = tp_type_message[0]
            tp_id = tp_type_message.get("tp_id")
            rsp_zb_id = [x for x in rsp_dict.get("result") if x.get("tp_id")==tp_id]
            rsp_zb_id = [x.get("id") for x in rsp_zb_id]
            rsp_zb_price_id = tp_type_message.get("tp_type_id")
            tp_type_message = tp_type_message.get("tp_id")
            # logging.debug("rsp_zb_id%s" % rsp_zb_id)
            # logging.debug("rsp_zb_price_id%s" % rsp_zb_price_id)
            # logging.debug("tp_type_message%s" % tp_type_message)
        elif Ptype == 1:
            data = [tp_type_message[i] for i in range(len(tp_type_message)) if int(tp_type_message[i].get("price_id"))==int(price_id)]
            rsp_zb_id = [data[i].get("id") for i in range(num)]
            rsp_zb_price_id = data[0].get("tp_type_id")
            tp_type_message = data[0].get("tp_id")
        return rsp_zb_id, rsp_zb_price_id, str(tp_type_message)
    except IndexError as e:
        print("没有找到票种信息")
        raise e
    except Exception as e:
        raise e
if __name__ == '__main__':
    data = {"body":{"orderNo":"P18062500101557790"},"head":{"apiId":"FOST","appId":"10","appUserName":"yleAI","sdkVersion":"2.0.0-beta09","sign":"3922072D4C67E24A67BF6FBAAD9EC1BD","token":"201806251739042018062517390439824"}}
    print(req_post(data))