#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_order_pay_status.py
# @Author  : Ruanzhe@riverroad.cn
# @Date  : 2019/7/1  17:30
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("order_pay_status")


@ddt
class TestOrderPayStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        cls.search_order = operation_mysql(
            "select * from bus_salecenter.sc_order where tenant_id=\'" + str(CD.tid) + "\' and state=2;"
        )
        setattr(CD, "outtime_order_id", cls.search_order[-1]["id"])
        cls.user_login = cls.api.api_request(
            "post",
            CD.url + r"/api/auth/login",
            {"tid": str(CD.tid)},
            {
                "account": CD.user_account,
                "password": CD.user_password,
                "client": "1"
            }
        )
        setattr(CD, "sessionid", cls.user_login.json()["result"]["sessionId"])
        setattr(CD, "accesstoken", cls.user_login.json()["result"]["authCode"])
        # 获取cid
        cls.search_category = operation_mysql(
            "select * from bus_goodscenter.gc_category where name = 'LineBus';"
        )
        setattr(CD, "cid", cls.search_category[0]["id"])
        # 获取sku_id
        data_format = "%" + "qatest_" + str(CD.next_seven_day) + "%"
        cls.search_schedule = operation_mysql(
            "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
                CD.tid) + "\' and name like '%s';" % data_format
        )
        cls.log.info("获取的线路查询结果为：" + str(cls.search_schedule))
        setattr(CD, "schedule_id", cls.search_schedule[-1]["id"])
        setattr(CD, "goods_id", cls.search_schedule[-1]["goods_id"])
        setattr(CD, "goods_price", cls.search_schedule[-1]["price"])
        cls.search_goods_title = operation_mysql(
            "select * from bus_goodscenter.gc_goods_instance_linebus where id=\'" + str(CD.goods_id) + "\';"
        )
        setattr(CD, "goods_title", cls.search_goods_title[0]["name"])
        cls.new_order = cls.api.api_request(
            "post",
            CD.url + r"/api/order",
            {
                "tid": str(CD.tid),
                "channelId": CD.channel_id,
                "operatorId": CD.userid,
                "accessToken": CD.accesstoken,
                "sessionId": CD.sessionid
            },
            {
                "cityAndScheduleTimeStamp": [{
                    "cityId": CD.city_arrival_id,
                    "scheduleTimeStamp": CD.current_date
                }],
                "detailParams": [{
                    "categoryId": CD.cid,
                    "goodsId": CD.goods_id,
                    "goodsPrice": str(CD.goods_price),
                    "goodsTitle": str(CD.goods_title),
                    "num": 1,
                    "skuId": CD.schedule_id,
                    "totalAmount": str(CD.goods_price),
                    "passengerType": 0
                }],
            }
        )
        cls.log.info(cls.new_order.json())
        setattr(CD, "order_id", cls.new_order.json()["result"]["id"])
        cls.search_station = operation_mysql(
            "select * from bus_linebus_engine.lb_bus_station where tid = \'" + CD.tid + "\';"
        )
        setattr(CD, "station_arrival_id", cls.search_station[-1]["id"])
        setattr(CD, "station_departure_id", cls.search_station[-1]["id"])

        cls.order_pay = cls.api.api_request(
            "post",
            CD.url + r"/api/order/pay",
            {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid, "accessToken": CD.accesstoken,
             "sessionId": CD.sessionid},
            {"skus": [{
                "adultPassengerParams": [{
                    "firstName": "asfsdf",
                    "lastName": "sdgdfgd",
                    "needWheelchair": False}],
                "infantPassengerParams": [],
                "childPassengerParams": [],
                "elderPassengerParams": [],
                "id": CD.schedule_id,
                "subBusLineCode": "qatest01",
                "subBuslineName": "qatest",
                "stationDepartureId": str(CD.station_departure_id),
                "stationArrivalId": str(CD.station_arrival_id)}],
                "paymentParam": {
                    "payToken": str(CD.paytoken),
                    "payModeList": [{"count": 350, "amount": "35", "type": 1}],
                    "creditCardInfo": {
                        "cardNum": "4012888818888",
                        "cardSecurity": "900",
                        "cardMonth": "09",
                        "cardYear": "25",
                        "cardFirstName": "Thresh",
                        "cardLastName": "Django",
                        "cardPhone": "+8617863803770",
                        "cardPurePhone": "17863803770",
                        "cardCountryCode": "+86",
                        "cardStreet": "yinhedasha",
                        "cardZipcode": "250101",
                        "cardCity": "Jinan",
                        "cardState": "JInan",
                        "cardCountry": "CN"}},
                "orderId": CD.order_id,
                "contactEmail": "15011111111@autotest.com",
                "contactFirstName": "Thresh",
                "contactLastName": "Django",
                "contactPhone": "+8615011111111",
                "contactCountryCode": "+86",
                "contactPurePhone": "15011111111",
                "youthAgreement": False})
        cls.log.info("支付信息为：" + str(cls.order_pay.json()))

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_order_pay_status(self, datas):
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
