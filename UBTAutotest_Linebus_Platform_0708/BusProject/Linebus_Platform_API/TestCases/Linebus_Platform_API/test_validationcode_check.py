#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_validationcode_check.py
# @Author  : Ruanzhe@riverroad.cn
# @Date  : 2019/6/13  17:24
import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.common.read_datas import ReadDatas
from BusProject.Linebus_Platform_API.common import DataPaths
from ddt import ddt, data
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.common.Data_Re import DataRe
from BusProject.Linebus_Platform_API.common.output_log import output
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql

testdata = ReadDatas(DataPaths.DatasPath).read_datas("validationcode_check")


@ddt
class TestValidationCodeCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 登录website，获取sessionid，accesstoken
        cls.res_login = cls.api.api_request(
            'post',
            CD.url + r'/api/auth/login',
            {"tid": str(CD.tid)},
            {"account": CD.user_account, "password": CD.user_password,
             "client": "1"})
        setattr(CD, "sessionid", cls.res_login.json()["result"]["sessionId"])
        setattr(CD, "accesstoken", cls.res_login.json()["result"]["authCode"])
        # 发送验证码
        cls.get_code = cls.api.api_request(
            "post",
            CD.url + r"/validationcode/sendvalidationcode",
            {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid},
            {
                "scene": "LOGIN",
                "serverConfigCode": "LjVtBPvpPt",
                "targetPhone": "+8617863803771",
                "templateContent": r"'[' + #companyName + '] "
                                   r"Your register verification code is: ' + #code + ' (Expires in 30 minutes)'"
            }
        )
        setattr(CD, "validation_code", str(cls.get_code.json()["result"]))

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_validationcode_check(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = self.re.param_re(datas['header'])
        datas['param'] = self.re.param_re(datas['parameter'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        res = self.api.api_request(datas['method'], datas['url'], eval(datas['header']), eval(datas['param']))
        self.log.info("the actual result :{0}".format(res.json()))
        try:
            self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
            self.assertEqual(str(eval(datas['expected'])['msg']), str(res.json()['status']['msg']))
            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], datas['id'] + 1, str(res.json()['status']), Result)
