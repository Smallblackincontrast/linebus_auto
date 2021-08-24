# -*- coding:utf-8 -*-
# @Time     :2019/7/25 10:10
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_ticket_reschedule.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_ticket_reschedule")


@ddt
class TestAPITicketReschedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()

        # 制造订单
        order = order_produce()
        setattr(CD, "order_id", order[0])
        setattr(CD, "sessionid", order[2])
        setattr(CD, "accesstoken", order[1])

        # 查询票
        ticket_data = operation_mysql(
            "select* from bus_linebus_engine.lb_ticket where order_id = \'" + CD.order_id + "\';")
        setattr(CD, "ticket_id", str(ticket_data[0]["id"]))

        # 查询payment
        payment_data = operation_mysql(
            "select * from bus_paymentcenter.pc_payment where link_code = \'" + CD.order_id + "\';")
        setattr(CD, "payment_id", str(payment_data[0]["id"]))
        setattr(CD, "paytoken", payment_data[0]["pay_token"])

        # 无票的订单id
        noticket_order_data = operation_mysql(
            "select * from bus_salecenter.sc_order where tenant_id = \'" + CD.tid + "\' and "
                                                                                    "id not in (select order_id from bus_linebus_engine.lb_ticket)")
        setattr(CD, "noticket_order_id", noticket_order_data[0]["id"])

        # 查询已作废的票
        void_ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where status = 6 and tid = \'" + CD.tid + "\';")
        setattr(CD, "void_ticket_id", void_ticket_data[-1]["id"])

        # 查询残疾人票
        wheelchair_ticket_data = operation_mysql(
            "select * from bus_linebus_engine.lb_ticket where passenger_need_wheelchair = 1 and status = 0")
        setattr(CD, "wheelchair_ticket_id", wheelchair_ticket_data[-1]["id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_api_ticket_reschedule(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = self.re.param_re(datas['header'])
        datas['param'] = self.re.param_re(datas['parameter'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        res = self.api.api_request(datas['method'], datas['url'], eval(datas['header']), eval(datas['param']))
        self.log.info("the actual result :{0}".format(res.json()))
        try:
            if datas["id"] == 5:
                self.update_maintain = self.api.api_request(
                    "post", "http://47.94.8.135:8500/maintainConfig/updateStatus", {"tid": CD.tid},
                    {
                        "id": 292222970103861760,
                        "maintainStatus": True,
                        "title": "General Service Maintenance",
                        "topicName": "service.maintain.status.topic"
                    }
                )
            if datas["id"] == 6:
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
            if datas["id"] == 8:
                goods_sku_data = operation_mysql(
                    "select * from bus_goodscenter.gc_goods_sku where id = \'" + str(CD.schedule_id) + "\';")
                setattr(CD, "goods_sku_version", goods_sku_data[0]["version"])

                self.update_stock = self.api.api_request("post",
                                                         "http://47.94.8.135:9100/route/update/" + str(CD.schedule_id) +
                                                         r'/stock?capacity=0&locked=0&sold=0&available=0&unlimited=false&isPacking=false&version='
                                                         + str(CD.goods_sku_version), {"tid": CD.tid}, None)
            if datas["id"] == 9:
                self.update_stock = self.api.api_request("post",
                                                         "http://47.94.8.135:9100/route/update/" + str(CD.schedule_id) +
                                                         r'/stock?capacity=56&locked=0&sold=10&available=46&unlimited=true&isPacking=false&version='
                                                         + str(CD.goods_sku_version + 1), {"tid": CD.tid}, None)

            self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['status']['code']))
            self.assertEqual(str(eval(datas['expected'])['msg']), str(res.json()['status']['msg']))

            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], datas['id'] + 1, str(res.json()['status']), Result)
