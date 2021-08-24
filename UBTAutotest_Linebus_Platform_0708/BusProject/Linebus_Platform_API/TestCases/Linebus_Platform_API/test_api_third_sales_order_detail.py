# -*- coding:utf-8 -*-
# @Time     :2019/7/23 10:22
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_third_sales_order_detail.py
# @software :PyCharm
import unittest
import csv
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.common.read_datas import ReadDatas
from BusProject.Linebus_Platform_API.common import DataPaths
from ddt import ddt, data
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.common.Data_Re import DataRe
from BusProject.Linebus_Platform_API.common.output_log import output
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_third_sales_order_detail")


@ddt
class TestApiThirdSalesOrderDetail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        cls.third_login = cls.api.api_request(
            "post",
            CD.url + r"/api/third/sales/login",
            {"tid": str(CD.tid), "channelId": CD.third_channel_id},
            {"secretKey": CD.third_channel_secret_key})
        setattr(CD, "third_token", cls.third_login.json()["result"])
        third_order_data = operation_mysql(
            "SELECT * FROM bus_salecenter.sc_order WHERE tenant_id = \'" + CD.tid + "\' AND channel_id = \'" + CD.third_channel_id + "\'; ")
        setattr(CD, "third_order_id", third_order_data[0]["id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_api_third_sales_order_detail(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = self.re.param_re(datas['header'])
        datas['param'] = self.re.param_re(datas['parameter'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        res = self.api.api_request(datas['method'], datas['url'], eval(datas['header']), eval(datas['param']))
        self.log.info("the actual result :{0}".format(res.json()))
        if datas['title'] == "创建订单":
            setattr(CD, "order_id", res.json()["result"]["detailsDtos"][0]["orderId"])
        try:
            self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
            self.assertEqual(str(eval(datas['expected'])['msg']), str(res.json()['status']['msg']))
            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], datas['id'] + 1, str(res.json()['status']), Result)
