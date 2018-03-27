#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import cx_Oracle
import os
import time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 解决oracle中文乱码

from time import ctime

usename,password,ip_port_servername = ('dbvop', 'dbvop', '10.161.50.87:1530/TDB')

logPath = os.path.abspath(os.curdir) + "/error.log"

def QueryOperationDB(sql):  
    connection = cx_Oracle.connect(usename, password, '10.161.50.88:1530/TDB') 
    try:
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryOperationDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def QueryDB(sql):  
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
    	
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()

def GetDatas_QueryDB(sql):
    connection = cx_Oracle.connect(usename, password, ip_port_servername) 
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception,e:
        with open(logPath,"a") as obj:
            obj.writelines(__name__ + "    GetDatas_QueryDB     "+str(e)+"    %s    "%ctime()+os.linesep)
    finally:
        connection.close()



def main(str_svc_number):
	svc_number = str_svc_number	
	iccidList = []

	maxIccid_id = int(QueryDB("SELECT max(iccid_id) FROM iccid")) + 1
	cardApplyItemId = QueryDB("SELECT CARD_APPLY_ITEM_ID FROM test_svc_number WHERE svc_number LIKE '%s' and rownum = 1" % svc_number)
	# usim_mark_apply_item_id =QueryOperationDB("select USIM_MAKE_APPLY_ITEM_ID from card_apply_detail where card_apply_id in (select CARD_APPLY_ID from card_apply  where usim_make_apply_no='%s'" % cardApplyItemId))
	usim_mark_apply_item_id = 'A001'
	business_id,business_mark,prov_code,eparchy_code = GetDatas_QueryDB("select MVNO_BUSINESS_ID,MVNO_BUSINESS_MARK,PROV_CODE,EPARCHY_CODE from svc_number where THOUSAND_SVC_SEG like '%s' and rownum = 1" % svc_number )[0]
	# print business_id,business_mark,prov_code,eparchy_code

	for eachTuple in GetDatas_QueryDB("SELECT iccid FROM test_svc_number WHERE svc_number LIKE '%s' "  % svc_number):
		iccidList.append(eachTuple[0]+'0') 


	connection = cx_Oracle.connect(usename, password, ip_port_servername) 
	try:
		cursor = connection.cursor()
		Inset_ST  = time.time()
		for eachIccid,index in zip(iccidList,range(1,len(iccidList)+1)):
			imsi =QueryDB("select imsi from test_svc_number where iccid ='%s'" % eachIccid[:-1])
			Insert_sql = '''INSERT INTO ICCID (ICCID_ID,MVNO_BUSINESS_ID,MVNO_USER_ID,ICCID,USIM_MAKE_APPLY_NO,USIM_MAKE_APPLY_ITEM_ID,MVNO_BUSINESS_MARK,PROV_CODE,EPARCHY_CODE,AVAILABLE_TIME,ENABLE_TIME,END_TIME,IMSI,MSIN,PUK1,PUK2,PIN1,PIN2,AMD1,KEY,A4,OP,TERMINATE_ACT,ICCID_STATUS,USIM_TYPE,KI,OLD_KEY) 
			VALUES (%d,%d,null,'%s','%s','%s','%s','%s','%s',to_timestamp('12-5月 -17 09.07.38.000000000 上午','DD-MON-RR HH.MI.SSXFF AM'),null,null,'%s',null,'60822926','60168338','1234','52581282','CBE38872','MIIBlwYJKoZIhvcNAQcDoIIBiDCCAYQCAQAxggEQMIIBDAIBADB3MHAxCzAJBgNV
					BAYTAkNOMQ4wDAYDVQQIDAVqaWxpbjESMBAGA1UEBwwJY2hhbmdjaHVuMQwwCgYD
					VQQKDANDTkMxDjAMBgNVBAsMBUNOQ0NBMR8wHQYDVQQDDBZDSElOQSBORVRDT00g
					Q0xBU1MzIENBAgM03a4wCwYJKoZIhvcNAQEBBIGAVJALwTnwSTLzUtCluGzpu9eL
					8One0bTZiz5WCBgdN6+0IM7j3sgKBKyLwY/d3M3HZ2sf5ELo+B6X/NUqTaHbCj+7
					cu5LJHwBD9FVKINwyl15p3HNFOrpg+avkL5iG28Sw3KgnrL0zpAj4l4BH748OERG
					DOzTLljM5AqKdeGwH/QwawYJKoZIhvcNAQcBMBQGCCqGSIb3DQMHBAhqTcs54lK+
					A4BIIlEhDS4CS+TZVKbNk2v9IpokpSGoyBqCA7A07UZvQOnJqByM3Zs7tl/G/YNi
					CZ1NawEWI939TIL8JqZ3gmm1YwqZOfv8Xhkz','01','01',null,'10','0','4CD49D73DE1D41674BA962254311EE12','MIIBlwYJKoZIhvcNAQcDoIIBiDCCAYQCAQAxggEQMIIBDAIBADB3MHAxCzAJBgNV
					BAYTAkNOMQ4wDAYDVQQIDAVqaWxpbjESMBAGA1UEBwwJY2hhbmdjaHVuMQwwCgYD
					VQQKDANDTkMxDjAMBgNVBAsMBUNOQ0NBMR8wHQYDVQQDDBZDSElOQSBORVRDT00g
					Q0xBU1MzIENBAgMrxjwwCwYJKoZIhvcNAQEBBIGAVZHZY7pevYEdobzxWvHwgoeB
					337Ru9wP+skdYokot2BZ/jdQ00V1O+OBQQtx5KqAFNOlQaTbLbH223R263ZRR7sE
					cFMcBYsKXd3gyJLRyeuzDSclN4fXbvtUUTXwa5ozU7ppHtO+CO5kjK90lGK3ZlAV
					65IgtjxEk+Nyi/o9ycUwawYJKoZIhvcNAQcBMBQGCCqGSIb3DQMHBAh4rJmiocZf
					w4BII/bD85x/VvwXB6CLY4oAGHo2Hy+BtoctyF0wQyOFq3FqcPa7lbMEQiLQc7FM
					mW2mAtBCJu6++Nd88sB6kIZkrtR9wFHiDRXy')''' % (maxIccid_id,int(business_id),eachIccid,cardApplyItemId,usim_mark_apply_item_id,business_mark,prov_code,eparchy_code,imsi)
			
			cursor.execute(Insert_sql)

			Update_sql = '''UPDATE imsi SET IMSI_STATUS='20', ICCID_ID=%d 
			WHERE imsi = '%s'
			''' % (maxIccid_id,imsi)
			cursor.execute(Update_sql)

			maxIccid_id += 1
			if index % 50 == 0:
				connection.commit()  # 每100笔事务，提交一次
		cursor.close()
		connection.commit() # 剩余记录最终提交
		Insert_ET = time.time()
		print 'Inset Time: %.2f sec' % (Insert_ET - Inset_ST)
		print "Finished."
	except Exception,e:
		print e
	finally:
		connection.close()

if __name__ == '__main__':
	main('1712587%')
