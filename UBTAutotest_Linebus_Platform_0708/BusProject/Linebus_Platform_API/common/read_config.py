
# -*- coding:utf-8 -*-
# @Time     :2019/4/8 14:07
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :read_config.py
# @software :PyCharm
import configparser
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs


class Read_Config:

    def read_config(self, filename, section, option):
        cf = configparser.ConfigParser()
        try:
            cf.read(filename)
        except Exception as e:
            MyLogs().error("打开配置文件异常：{0}".format(e))
        else:
            try:
                res = cf.get(section, option)
            except Exception as e:
                MyLogs().error("读取配置文件失败{0}".format(e))
        return res
