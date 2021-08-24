# -*- coding:utf-8 -*-
# @Time     :2019/7/9 15:04
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_busfraudapi_trans_void.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("busfraudapi_trans_void")


@ddt
class TestBusfraudapiTransVoid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        # 管理员登录
        cls.admin_login = cls.api.api_request("post", CD.url + r'/admin/platform/login', None,
                                              {"username": "qaadmin", "password": "123456"})
        setattr(CD, "operatortoken", cls.admin_login.json()["more"]["operatorToken"])
        # 加载管理员权限
        cls.permission_load = cls.api.api_request("post", CD.url + r'/admin/permission/load',
                                                  {"tid": CD.tid, "channelId": CD.channel_id,
                                                   "operatorId": CD.operatorid}, None)
        # 查询transaction列表
        cls.transaction = cls.api.api_request("post", CD.url + r'/transaction/creditcard/payrecordpage',
                                              {"tid": CD.tid, "channelId": CD.channel_id, "operatorId": CD.operatorid,
                                               "operatorToken": CD.operatortoken},
                                              {"busfraud":True,"pageNo": 0, "pageSize": 20, "cardNum": "", "paypalAccount": "",
                                               "tenantId": CD.tid, "transactionId": "", "authCode": ""})
        setattr(CD, "credit_card_payment_id", cls.transaction.json()["result"][0]["id"])

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_credit_card_payment_void(self, datas):
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
