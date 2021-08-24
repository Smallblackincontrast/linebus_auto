# -*- coding:utf-8 -*-
# @Time     :2019/7/25 17:28
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_seat_changeseat.py
# @software :PyCharm
# -*- coding:utf-8 -*-
# @Time     :2019/7/25 16:27
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_seat_lockseat.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_seat_changeseat")


@ddt
class TestApiSeatChangeseat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 登录
        user_login = ApiRequests().api_request("post", CD.url + r"/api/auth/login", {"tid": str(CD.tid)},
                                               {"account": CD.user_account, "password": CD.user_password,
                                                "client": "1"})
        setattr(CD, "sessionid", user_login.json()["result"]["sessionId"])
        setattr(CD, "accesstoken", user_login.json()["result"]["authCode"])

        # 制造订单
        # 获取cid
        search_category = operation_mysql("select * from bus_goodscenter.gc_category where name = 'LineBus';")
        setattr(CD, "cid", search_category[0]["id"])
        # 获取sku_id
        data_format = "%" + "bus_auto_" + str(CD.next_seven_day) + "%"
        search_schedule = operation_mysql(
            "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
                CD.tid) + "\' and name like '%s';" % data_format)
        print("获取的线路查询结果为：" + str(search_schedule))
        setattr(CD, "schedule_id", search_schedule[-1]["id"])
        setattr(CD, "goods_id", search_schedule[-1]["goods_id"])
        setattr(CD, "goods_price", search_schedule[-1]["price"])
        search_goods_title = operation_mysql(
            "select * from bus_goodscenter.gc_goods_instance_linebus where id=\'" + str(CD.goods_id) + "\';")
        setattr(CD, "goods_title", search_goods_title[0]["name"])

        # 锁座
        lock_seat = ApiRequests().api_request("post", CD.url + r'/api/seat/lockSeat',
                                              {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid,
                                               "AccessToken": CD.accesstoken},
                                              {"cleanLastSelect": 1, "seatParam": {CD.schedule_id: {"1": [4], "2": []}},
                                               "seatToken": None})
        print(lock_seat.json())
        # 下单
        new_order = ApiRequests().api_request(
            "post", CD.url + r"/api/order",
            {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid, "sessionId": CD.sessionid,
             "accessToken": CD.accesstoken},
            {"cityAndScheduleTimeStamp": [{"cityId": CD.city_arrival_id, "scheduleTimeStamp": CD.current_date}],
             "detailParams": [{"categoryId": CD.cid, "goodsId": CD.goods_id, "goodsPrice": str(CD.goods_price),
                               "goodsTitle": str(CD.goods_title), "num": 1, "skuId": CD.schedule_id,
                               "totalAmount": str(CD.goods_price), "passengerType": 0}], })
        print(new_order.json())
        setattr(CD, "order_id", new_order.json()["result"]["id"])

        search_station = operation_mysql(
            "select * from bus_linebus_engine.lb_bus_station where tid = \'" + CD.tid + "\';"
        )
        setattr(CD, "station_arrival_id", search_station[-1]["id"])
        setattr(CD, "station_departure_id", search_station[-1]["id"])
        # 支付
        order_pay = ApiRequests().api_request(
            "post", CD.url + r"/api/order/pay",
            {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid, "accessToken": CD.accesstoken,
             "sessionId": CD.sessionid},
            {
                "skus": [{
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
                    "stationDepartureId": CD.station_departure_id,
                    "stationArrivalId": CD.station_arrival_id}],
                "paymentParam": {
                    "payToken": "",
                    "payModeList": [{
                        "count": 350, "amount": "35", "type": 1}],
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
                "contactEmail": CD.user_email,
                "contactFirstName": "Thresh",
                "contactLastName": "Django",
                "contactPhone": "+8615011111111",
                "contactCountryCode": "+86",
                "contactPurePhone": "15011111111",
                "youthAgreement": False
            })
        print(order_pay.json())

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_api_seat_changeseat(self, datas):
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
