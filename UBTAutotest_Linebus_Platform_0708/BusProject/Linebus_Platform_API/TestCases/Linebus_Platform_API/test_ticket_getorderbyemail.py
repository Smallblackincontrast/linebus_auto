# -*- coding:utf-8 -*-
# @Time     :2019/7/10 15:22
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_ticket_getorderbyemail.py
# @software :PyCharm
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
import time

testdata = ReadDatas(DataPaths.DatasPath).read_datas("ticket_getorderbyemail")


@ddt
class TestTicketGetorderbyemail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 获取邮件验证码
        email_val = ApiRequests().api_request("post", CD.url + r'/api/auth/sendTickets/emailValidationCode',
                                             {"tid": CD.tid, "channelId": CD.channel_id}, {"email": CD.user_email})
        cls.log.info("获取邮箱验证码接口返回"+str(email_val.json()))
        time.sleep(10)
        # 登录bsp后台系统
        bsp_login = ApiRequests().api_request("post", r'http://47.94.8.135:8012/adminUser/login', None,
                                              {"username": CD.bsp_user, "password": CD.bsp_password})
        cls.log.info("登录bsp后台返回"+str(bsp_login.json()))
        setattr(CD, "bsp_operatortoken", bsp_login.json()["more"]["operatorToken"])

        permission_load = ApiRequests().api_request("get", "http://47.94.8.135:8012/permission/load",
                                                    {"operatorToken": CD.bsp_operatortoken}, None)
        # 获取邮件中的验证码
        mail_log = ApiRequests().api_request('get', r'http://47.94.8.135:8012/noticelog/searchmail',
                                             {"tid": CD.tid, "operatorToken": CD.bsp_operatortoken}, None)
        message = mail_log.json()["result"][0]["messageContent"]
        setattr(CD, "validation_code", message[1707:1713])
        cls.log.info("邮件中验证码为"+str(CD.validation_code))

        # time.sleep(10)

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_ticket_getorderbyemail(self, datas):
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
