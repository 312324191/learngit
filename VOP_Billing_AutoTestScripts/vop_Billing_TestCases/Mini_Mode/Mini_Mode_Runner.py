#! /usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'Simon'

import os
import sys
sys.path.append(os.path.abspath('%s/../..' % sys.path[0]))
import inspect
import unittest
from VOP_Billing_AutoTestScripts.common import HTMLTestRunner
from testRegisterAccount import testRegisterAccount

if __name__ == '__main__':

    suite = unittest.TestSuite()
    testClassList = [testRegisterAccount]

    for eachClass in testClassList:
        ins_class = inspect.getmembers(eachClass,predicate=inspect.ismethod)
        ClassName = ([x[0] for x in ins_class if x[0].find('test') != -1])
        for eachName in ClassName:
            suite.addTest(eachClass(eachName))

    cwd = os.getcwd()
    filePath = os.path.dirname(cwd) + '/results/service_result.html'
    try:
        fp = file(filePath, 'w')

        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                               title=u'VOP_API_Demo 测试报告',
                                               description=u'用例执行情况：')

        result = runner.run(suite)

        if (result.failure_count or result.error_count):
            print "cases_failure_count" % result.failure_count
            print 'cases_error_count' % result.error_count

    except IOError, e:
        print e