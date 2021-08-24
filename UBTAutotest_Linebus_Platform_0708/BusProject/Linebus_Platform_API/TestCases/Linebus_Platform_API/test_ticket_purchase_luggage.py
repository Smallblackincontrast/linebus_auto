# -*- coding:utf-8 -*-
# @Time     :2019/7/11 15:38
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_ticket_purchase_luggage.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("ticket_purchase_luggage")


@ddt
class TestTicketPurchaseLuggage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 查询未检票的票
        ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 0 and tid = \'" + CD.tid + "\';")
        setattr(CD, "ticket_id", ticket_data[-1]["id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_ticket_purchase_luggage(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = self.re.param_re(datas['header'])
        datas['param'] = self.re.param_re(datas['parameter'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        res = self.api.api_request(datas['method'], datas['url'], eval(datas['header']), eval(datas['param']))
        self.log.info("the actual result :{0}".format(res.json()))
        if datas["id"] == 3:
            self.update_maintain = self.api.api_request(
                "post", "http://47.94.8.135:8500/maintainConfig/updateStatus", {"tid": CD.tid},
                {
                    "id": 292222970103861760,
                    "maintainStatus": True,
                    "title": "General Service Maintenance",
                    "topicName": "service.maintain.status.topic"
                }
            )
        if datas["id"] == 4:
            self.update_maintain = self.api.api_request(
                "post",
                "http://47.94.8.135:8500/maintainConfig/updateStatus",
                {"tid": CD.tid},
                {
                    "id": 292222970103861760,
                    "maintainStatus": False,
                    "title": "General Service Maintenance",
                    "topicName": "service.maintain.status.topic"
                })
            operation_mysql(
                "update bus_goodscenter.gc_goods_instance_luggage set tid = 322755215541408255 where id = 326385042345939456")
        if datas["id"] == 5:
            operation_mysql(
                "update bus_goodscenter.gc_goods_instance_luggage set tid = 322755215541408256 where id = 326385042345939456")
        try:

            self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
            self.assertEqual(str(eval(datas['expected'])['msg']), str(res.json()['status']['msg']))

            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], int(datas['id']) + 1, str(res.json()['status']), Result)
