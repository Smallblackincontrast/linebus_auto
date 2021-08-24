# -*- coding:utf-8 -*-
# @Time     :2019/7/10 10:19
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_ticket_auto_checkin.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("ticket_auto_checkin")


@ddt
class TestTicketAutoCheckin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 查询未检票的票
        ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 0 and tid = \'" + CD.tid + "\';")
        setattr(CD, "ticket_qrcode", ticket_data[0]["qrcode"])
        setattr(CD, "skuId", ticket_data[0]["sku_id"])
        # 查询已检票的票
        checked_ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 1 and tid = \'" + CD.tid + "\';")
        setattr(CD, "checked_ticket_qrcode", checked_ticket_data[-1]["qrcode"])
        setattr(CD, "checked_ticket_skuId", checked_ticket_data[-1]["sku_id"])
        # 查询已作废的票
        void_ticket_data =  operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 6 and tid = \'" + CD.tid + "\';")
        setattr(CD, "void_ticket_qrcode", void_ticket_data[-1]["qrcode"])
        setattr(CD, "void_ticket_skuId", void_ticket_data[-1]["sku_id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_ticket_auto_checkin(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = self.re.param_re(datas['header'])
        datas['param'] = self.re.param_re(datas['parameter'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        res = self.api.api_request(datas['method'], datas['url'], eval(datas['header']), eval(datas['param']))
        self.log.info("the actual result :{0}".format(res.json()))
        try:
            if datas["id"] == 5:
                self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
            else:
                self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
                self.assertEqual(str(eval(datas['expected'])['msg']), str(res.json()['status']['msg']))

            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], datas['id'] + 1, str(res.json()['status']), Result)
