#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

import time, sys, os
path = os.path.dirname(__file__)
sys.path.append(path+'\\interface')
sys.path.append(path+'\\db_fixture')

from HTMLTestRunner import HTMLTestRunner
import unittest

test_dir = path+'\\interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*QDcase_01.py')
if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = './report/'+now + '_result.html'
    fp=open(filename, 'wb')
    runner = HTMLTestRunner(stream = fp,
        title = 'Guest Manage System Interface Test Report',
        description = 'Implementation Example with:')
    runner.run(discover)
    fp.close()