# -*- coding:utf-8 -*-
# @Time     :2019/4/23 9:49
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :output_log.py
# @software :PyCharm
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs


def output(title, url, header, param, expected):
    MyLogs().info("测试标题是:{0}".format(title))
    MyLogs().info("测试的地址是:{0}".format(url))
    MyLogs().info("测试的header是:{0}".format(header))
    MyLogs().info("测试的参数是:{0}".format(param))
    MyLogs().info("预期结果是:{0}".format(expected))
