# -*- coding:utf-8 -*-
# @Time     :2019/4/8 14:10
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :suite_case.py
# @software :PyCharm
import unittest
from BusProject.Linebus_Platform_API.common import DataPaths
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs


class SuiteCase:

    def suitecase(self, button, caselist):
        suite = unittest.TestSuite()
        if button.upper() == 'ON':
            discover = unittest.defaultTestLoader.discover(DataPaths.CasePath, pattern='test_*.py', top_level_dir=None)
            try:
                suite.addTests(discover)
            except Exception as e:
                MyLogs().error("收集用例失败:{0}".format(e))

        else:
            if isinstance(caselist, (list, tuple)):
                for case in caselist:
                    discover = unittest.defaultTestLoader.discover(DataPaths.CasePath, pattern='test_' + case + '.py',
                                                                   top_level_dir=None)
                    try:
                        suite.addTest(discover)
                    except Exception as e:
                        MyLogs().error("收集用例失败{0}".format(e))

        return suite
