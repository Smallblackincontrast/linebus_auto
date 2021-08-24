# -*- coding:utf-8 -*-
# @Time     :2019/7/19 15:16
# @Author   :Tester_Wang
# @Email    :wangying@riverroad.com
# @File     :order_produce.py
# @software :PyCharm
import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from ddt import ddt
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql

log = MyLogs()
# read_data = ReadDatas(DataPaths.DatasPath)
# re = DataRe()
api = ApiRequests()


def order_produce():
    order_list = []
    # 登录
    user_login = api.api_request(
        "post",
        CD.url + r"/api/auth/login",
        {"tid": str(CD.tid)},
        {
            "account": CD.user_account,
            "password": CD.user_password,
            "client": "1"
        }
    )
    setattr(CD, "sessionid", user_login.json()["result"]["sessionId"])
    setattr(CD, "accesstoken", user_login.json()["result"]["authCode"])

    # 获取cid
    search_category = operation_mysql(
        "select * from bus_goodscenter.gc_category where name = 'LineBus';"
    )
    setattr(CD, "cid", search_category[0]["id"])
    # 获取sku_id
    data_format = "%" + "qatest_" + str(CD.next_seven_day) + "%"
    search_schedule = operation_mysql(
        "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
            CD.tid) + "\' and name like '%s';" % data_format
    )
    log.info("获取的线路查询结果为：" + str(search_schedule))
    setattr(CD, "schedule_id", search_schedule[-1]["id"])
    setattr(CD, "goods_id", search_schedule[-1]["goods_id"])
    setattr(CD, "goods_price", search_schedule[-1]["price"])
    search_goods_title = operation_mysql(
        "select * from bus_goodscenter.gc_goods_instance_linebus where id=\'" + str(CD.goods_id) + "\';"
    )
    setattr(CD, "goods_title", search_goods_title[0]["name"])
    # 下单
    new_order = api.api_request(
        "post", CD.url + r"/api/order",
        {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid, "sessionId": CD.sessionid,
         "accessToken": CD.accesstoken},
        {"cityAndScheduleTimeStamp": [{"cityId": CD.city_arrival_id, "scheduleTimeStamp": CD.current_date}],
         "detailParams": [{"categoryId": CD.cid, "goodsId": CD.goods_id, "goodsPrice": str(CD.goods_price),
                           "goodsTitle": str(CD.goods_title), "num": 1, "skuId": CD.schedule_id,
                           "totalAmount": str(CD.goods_price), "passengerType": 0}], })
    print({"cityAndScheduleTimeStamp": [{"cityId": CD.city_arrival_id, "scheduleTimeStamp": CD.current_date}],
           "detailParams": [{"categoryId": CD.cid, "goodsId": CD.goods_id, "goodsPrice": str(CD.goods_price),
                             "goodsTitle": str(CD.goods_title), "num": 1, "skuId": CD.schedule_id,
                             "totalAmount": str(CD.goods_price), "passengerType": 0}], })
    log.info(new_order.json())

    setattr(CD, "order_id", new_order.json()["result"]["id"])


    search_station = operation_mysql(
        "select * from bus_linebus_engine.lb_bus_station where tid = \'" + CD.tid + "\';"
    )
    setattr(CD, "station_arrival_id", search_station[-1]["id"])
    setattr(CD, "station_departure_id", search_station[-1]["id"])
    # 支付
    order_pay = api.api_request(
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
    log.info(order_pay.json())

    order_list.append(str(CD.order_id))
    order_list.append(str(CD.accesstoken))
    order_list.append(str(CD.sessionid))

    if int(order_pay.json()["status"]["code"]) == 0:
        log.info("订单制造成功！订单号为：" + CD.order_id)
    else:
        log.info("订单制造失败！")

    return order_list


if __name__ == '__main__':
    print(order_produce())
