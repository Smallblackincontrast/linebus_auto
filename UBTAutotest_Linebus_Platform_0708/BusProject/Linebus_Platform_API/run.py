# -*- coding:utf-8 -*-
# @Time     :2019/4/8 13:17
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :run.py
# @software :PyCharm

from BusProject.Linebus_Platform_API import HTMLTestRunnerNew
from BusProject.Linebus_Platform_API.common import DataPaths
from BusProject.Linebus_Platform_API.common.suite_case import SuiteCase
from BusProject.Linebus_Platform_API.common.read_config import Read_Config
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs

with open(DataPaths.ReportPath, 'wb+') as file:
    button = Read_Config().read_config(DataPaths.ConfigPath, 'CASE', 'button')
    caselist = eval(Read_Config().read_config(DataPaths.ConfigPath, 'CASE', 'caselist'))
    suite = SuiteCase().suitecase(button, caselist)
    runner = HTMLTestRunnerNew.HTMLTestRunner(file, verbosity=2, title="Linebus_Platform_API_Test", description="2019/6/10",
                                              tester='Tester_qa')
    try:
        runner.run(suite)
    except Exception as e:
        MyLogs().error("执行用例失败:{0}".format(e))
