# -*- coding:utf-8 -*-
# @Time     :2019/4/8 10:34
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :Data_Re.py
# @software :PyCharm
import re
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD


class DataRe:
    def data_re(self, pattern, string, object):
        for i in range(20):
            if re.search(pattern, string):
                res = re.search(pattern, string)
                key = res.group(0)
                value = res.group(1)
                try:
                    MyLogs().info("正在获取动态参数:{0}获取的参数是：{1}".format(key, str(getattr(object, value))))
                    string = string.replace(key, str(getattr(object, value)))
                except Exception as e:
                    MyLogs().error("参数替换失败{0}".format(e))
            else:
                string = string
        return string

    def url_re(self, data):
        url = CD.url + self.data_re('\$\{(.*?)\}', data, CD)
        return url

    def param_re(self, data):
        param = self.data_re('\$\{(.*?)\}', data, CD)
        return param

    def header_re(self, data):
        header = self.data_re('\$\{(.*?)\}', data, CD)
        return header
