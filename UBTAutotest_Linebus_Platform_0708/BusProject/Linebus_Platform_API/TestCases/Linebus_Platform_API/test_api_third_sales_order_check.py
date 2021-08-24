# -*- coding:utf-8 -*-
# @Time     :2019/7/23 9:42
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_third_sales_order_check.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_third_sales_order_check")


@ddt
class TestApiThirdSalesOrderCheck(unittest.TestCase):

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

        # 获取cid
        cls.search_category = operation_mysql(
            "select * from bus_goodscenter.gc_category where name = 'LineBus';"
        )
        setattr(CD, "cid", cls.search_category[0]["id"])
        # 获取sku_id
        # data_format = "%" + "wytest_" + str(CD.next_seven_day) + "%"
        data_format = "%" + "wytest_" + "%"
        cls.search_schedule = operation_mysql(
            "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
                CD.tid) + "\' and name like '%s' order by id desc ;" % data_format
        )
        cls.log.info("获取的线路查询结果为：" + str(cls.search_schedule))
        setattr(CD, "schedule_id", cls.search_schedule[0]["id"])
        setattr(CD, "goods_id", cls.search_schedule[0]["goods_id"])
        setattr(CD, "goods_price", cls.search_schedule[0]["price"])
        cls.search_goods_title = operation_mysql(
            "select * from bus_goodscenter.gc_goods_instance_linebus where id=\'" + str(CD.goods_id) + "\';"
        )
        setattr(CD, "goods_title", cls.search_goods_title[0]["name"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_order_check(self, datas):
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
