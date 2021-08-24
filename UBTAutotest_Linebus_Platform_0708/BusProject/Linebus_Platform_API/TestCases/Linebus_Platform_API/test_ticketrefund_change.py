# -*- coding:utf-8 -*-
# @Time     :2019/7/22 14:32
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_ticketrefund_change.py
# @software :PyCharm
import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.common.read_datas import ReadDatas
from BusProject.Linebus_Platform_API.common import DataPaths
from ddt import ddt, data
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.order_produce import order_produce
from BusProject.Linebus_Platform_API.common.Data_Re import DataRe
from BusProject.Linebus_Platform_API.common.output_log import output
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql
from urllib.parse import quote

testdata = ReadDatas(DataPaths.DatasPath).read_datas("ticketrefund_change")


@ddt
class TestTicketrefundChange(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 制造订单
        order = order_produce()
        setattr(CD, "order_id", order[0])
        ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 0 and order_id = \'" + CD.order_id + "\';")
        setattr(CD, "ticket_id", ticket_data[-1]["id"])
        setattr(CD, "ticket_code", ticket_data[-1]["code"])
        cls.ticketrefund_save = cls.api.api_request("post", CD.url + "/ticketRefund/save/v2",
                                                    {"tid": CD.tid, "channelId": CD.channel_id,
                                                     "operatorId": CD.operatorid},
                                                    {"ticketIds": CD.ticket_id, "ticketCodes": CD.ticket_code,
                                                     "orderId": CD.order_id, "fee": "35.00", "payType": 9,
                                                     "reason": "autotest_wang", "state": 0, "refundServiceCharge": 0,
                                                     "tid": CD.tid, "applyPersonName": "ying wang"})
        setattr(CD, "ticket_refund_id", cls.ticketrefund_save.json()["result"]["id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_ticketrefund_change(self, datas):
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
