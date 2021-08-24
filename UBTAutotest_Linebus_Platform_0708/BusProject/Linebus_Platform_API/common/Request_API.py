# -*- coding:utf-8 -*-
# @Time     :2019/4/4 9:03
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :Request_API.py
# @software :PyCharm

import requests
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs


class ApiRequests:

    def __init__(self):
        self.log = MyLogs()

    def api_request(self, http_method, api_url, api_header, param, file=None):
        if http_method.upper() == "POST":
            try:
                self.log.info("正在进行post请求")
                res = requests.post(api_url, json=param,headers=api_header,files=file)
            except BaseException as e:
                self.log.error("post请求出现异常")
                raise e
        elif http_method.upper() == "GET":
            try:
                self.log.info("正在进行get请求")
                res = requests.get(api_url, json=param,headers=api_header)
            except BaseException as e:
                self.log.error("get请求出现异常")
                raise e
        else:
            self.log.error("请求方式不正确")
        return res


