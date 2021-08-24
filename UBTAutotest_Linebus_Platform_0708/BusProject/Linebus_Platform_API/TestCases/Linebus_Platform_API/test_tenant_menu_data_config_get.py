#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_tenant_menu_data_config_get.py
# @Author  : Ruanzhe@riverroad.cn
# @Date  : 2019/6/17  14:17
import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.common.read_datas import ReadDatas
from BusProject.Linebus_Platform_API.common import DataPaths
from ddt import ddt, data
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.common.Data_Re import DataRe
from BusProject.Linebus_Platform_API.common.output_log import output

testdata = ReadDatas(DataPaths.DatasPath).read_datas("tenant_menu_data_config_get")


@ddt
class TestTenantMenuDataConfigGet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()
        cls.new_tenant_menu = cls.api.api_request(
            "post",
            CD.url + r"/tenantmenudataconfig/addnew/v2",
            {"tid": str(CD.tid),
             "channelId": CD.channel_id,
             "operatorId": CD.operatorid
             },
            {
                "address": "rztest",
                "menuName": "rztest",
                "sort": 0,
                "type": 2
            }
        )
        setattr(CD, "tenant_data_menu_id", cls.new_tenant_menu.json()['result']['id'])
        cls.log.info("新增的租户menuid为：" + str(CD.tenant_data_menu_id))

    def setUp(self):
        self.log.info("开始测试")

    def tearDown(self):
        self.log.info("结束测试")

    @classmethod
    def tearDownClass(cls):
        cls.del_tenant_menu = cls.api.api_request(
            "get",
            CD.url + r"/tenantmenudataconfig/del?id=" + str(CD.tenant_data_menu_id),
            {"tid": str(CD.tid),
             "channelId": CD.channel_id,
             "operatorId": CD.operatorid
             },
            {}
        )
        cls.log.info("删除租户menu成功！")

    @data(*testdata)
    def test_tenant_menu_data_config_get(self, datas):
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
