# -*- coding:utf-8 -*-
# @Time     :2019/7/18 18:13
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :test_api_wallet_reload_cardpay.py
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

testdata = ReadDatas(DataPaths.DatasPath).read_datas("api_wallet_reload_cardpay")


@ddt
class TestApiWalletReloadCardpay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        cls.user_login = cls.api.api_request("post", CD.url + r"/api/auth/login", {"tid": str(CD.tid)},
                                             {"account": CD.user_account, "password": CD.user_password, "client": "1"})
        setattr(CD, "sessionid", cls.user_login.json()["result"]["sessionId"])
        setattr(CD, "accesstoken", cls.user_login.json()["result"]["authCode"])
        cls.search_sell = cls.api.api_request("get", CD.url + r'/giftCard/search/sell?cardType=1',
                                              {"tid": CD.tid, "channelId": CD.channel_id}, None)
        setattr(CD, "gift_card_skuid", cls.search_sell.json()["result"][0]["skuId"])
        cls.wallet_reload_order = cls.api.api_request("post", CD.url + r'/api/wallet/reload/order',
                                                      {"tid": CD.tid, "channelId": CD.channel_id,
                                                       "operatorId": CD.operatorid, "accessToken": CD.accesstoken,
                                                       "sessionId": CD.sessionid},
                                                      {"count": 1, "skuId": CD.gift_card_skuid})
        setattr(CD, "wallet_reload_orderid", cls.wallet_reload_order.json()["result"]["id"])

    def setUp(self):
        self.log.info("????????????")

    def tearDown(self):
        self.log.info("????????????")

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_api_wallet_reload_cardpay(self, datas):
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
