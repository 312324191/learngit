#! /usr/bin/env python
# -*- coding:utf-8 -*-
import sys 
import datetime
import time
import os

sys.path.append(os.path.abspath('%s/../..' % sys.path[0]))


from common import common_tools,common_optOracle_billing

now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #获取系统当前时间
now_time = int(time.time())
now_time = now_time + 300
addTime = time.strftime('%Y%m%d%H%M%S',time.localtime(now_time))

# 语音： 本地拨打本地
svc_number =  '17159140062' # sys.args[0]

uid,imsi = common_tools.getUid_IMSI(svc_number)

defult_HuaDan = "20011004    143     23607858958    0100000GJYY0099089800201705090332124SZD.00.m.gz   2         1000000072                     xxx m 10020000000000    1019317041440061                  18810861883                                                 17041440061                 2017110622060520171106213641121       460090147800002                                             0535 21072 09535                                4321                                                                                   61418702220                     21                   0                     0   0 0                                                                                                                                                        0 0                                                                              "
frontString = defult_HuaDan[:150] + svc_number
lastString = defult_HuaDan[161:]
change_org_number_String = frontString + lastString  # 替换主叫号码

frontString = change_org_number_String[:184] + str(int(svc_number)+1)
lastString = change_org_number_String[195:]
change_trim_number_String = frontString + lastString # 替换被叫号码
print change_trim_number_String

frontString = change_trim_number_String[:244] + svc_number
lastString = change_trim_number_String[255:]
change_self_number_String = frontString + lastString # 替换计费号码

frontString = change_self_number_String[:272] + addTime + addTime
lastString = change_self_number_String[300:]
change_start_end_time_String = frontString + lastString #替换话始话闭时间

frontString = change_start_end_time_String[:310] + imsi
lastString = change_start_end_time_String[325:]
change_imsi_String = frontString + lastString # 替换imsi

# print change_imsi_String
nowTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
file_name = '93001800700000000GJYY0099089811201711060332124SZD.C0'
file_name = file_name.replace('20171106033212',nowTime)
file_name = nowTime + file_name[14:] 

ipb_sql = "select a.real_balance from billing_mode.info_pay_balance  a where pay_id = '%s' and a.product_id = 'PE_0112'" % uid
beforRealBalance = common_optOracle_billing.QueryDB(ipb_sql)

parent_path = os.path.dirname(sys.path[0])
with file(parent_path + '/files_in/'+file_name,'w') as fobj: # '/app/application_mode/data_in/1/MBVC/1/in/' +
	fobj.write(change_imsi_String)

time.sleep(10)


afterRealBalance= common_optOracle_billing.QueryDB(ipb_sql)

assert(3 == (beforRealBalance - afterRealBalance)) # 断言扣减账本语音资源量3分钟