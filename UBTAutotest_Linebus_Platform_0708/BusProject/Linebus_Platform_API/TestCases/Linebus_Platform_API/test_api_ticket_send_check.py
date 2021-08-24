# -*- coding:utf-8 -*-
# @Time     :2019/7/24 16:33
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_ticket_send_check.py
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
from urllib.parse import quote
import time

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_ticket_send_check")


@ddt
class TestApiTicketSendCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # # 获取手机验证码
        # phone_val = ApiRequests().api_request("get",
        #                                       CD.url + r'/api/auth/sendvalidationcode?phone=' + quote(CD.user_account),
        #                                       {"tid": CD.tid, "channelId": CD.channel_id}, None)
        # setattr(CD, "validation_code", phone_val.json()["result"])
        ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status=0 and tid = \'" + CD.tid + "\';")
        setattr(CD, "order_id", str(ticket_data[-1]["order_id"]))
        # 获取sku_id
        search_schedule = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where order_id = \'"+CD.order_id+"\';")
        setattr(CD, "schedule_id", search_schedule[-1]["sku_id"])
        # 无票的订单id
        noticket_order_data = operation_mysql(
            "select * from bus_salecenter.sc_order where tenant_id = \'" + CD.tid + "\' and "
                                                                                    "id not in (select order_id from bus_linebus_engine.lb_ticket)")
        setattr(CD, "noticket_order_id", noticket_order_data[0]["id"])
        time.sleep(10)
        # 发送邮箱重置密码验证码
        email_rest = ApiRequests().api_request("post", CD.url + r'/api/auth/sendTickets/emailValidationCode',
                                               {"tid": CD.tid, "channelId": CD.channel_id}, {"email": CD.user_email})

        # 登录bsp后台系统
        bsp_login = ApiRequests().api_request("post", r'http://47.94.8.135:8012/adminUser/login', None,
                                              {"username": CD.bsp_user, "password": CD.bsp_password})
        setattr(CD, "bsp_operatortoken", bsp_login.json()["more"]["operatorToken"])
        permission_load = ApiRequests().api_request("get", "http://47.94.8.135:8012/permission/load",
                                                    {"operatorToken": CD.bsp_operatortoken}, None)
        time.sleep(10)
        # 获取邮件中的验证码
        mail_log = ApiRequests().api_request('get', r'http://47.94.8.135:8012/noticelog/searchmail',
                                             {"tid": CD.tid, "operatorToken": CD.bsp_operatortoken}, None)
        message = mail_log.json()["result"][0]["messageContent"]
        setattr(CD, "validation_code", message[1707:1713])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_api_ticket_send_check(self, datas):
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
