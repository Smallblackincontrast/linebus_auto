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

        # 获取sku_id
        data_format = "%" + "bus_auto_" + str(CD.next_seven_day) + "%"
        search_schedule = operation_mysql(
            "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
                CD.tid) + "\' and name like '%s';" % data_format)
        print("获取的线路查询结果为：" + str(search_schedule))
        setattr(CD, "schedule_id", search_schedule[-1]["id"])

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
