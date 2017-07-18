#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Simon'

import common_optMysql
import base64
import gzip
from StringIO import StringIO
from xml.etree import ElementTree

def getSubProdInfos(trans_ido):
	resList = []
	SubProdInfoDist={}
	xmlString = common_optMysql.QueryDB("SELECT `req_content` FROM  `esblogdb`.`tlog_req` WHERE `trans_ido` = '%s' AND svc_name = 'VOPForOrderProcessForSer'" % trans_ido)
	decodeString = base64.b64decode(xmlString[(xmlString.find("ORDER_CONT>")+11):xmlString.find("</ns24:ORDER_CONT>")])
	buff = StringIO(decodeString)
	f = gzip.GzipFile(fileobj=buff)
	data = f.read()
	root = ElementTree.fromstring(data)
	for i in root[0][2][0][1]:
		SubProdInfoDist["ProdId"] = i.find('ProdId').text
		SubProdInfoDist["ActType"] = i.find('ActType').text
		resList.append(SubProdInfoDist) 
		SubProdInfoDist = {}
	return resList

if __name__ == '__main__':
	print getSubProdInfos('yMGbzh6lsPH9AtcdoeFmI2fQ3rkXDR')
	