import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from ddt import ddt
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.order_produce import order_produce
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql

# 登录
user_login = ApiRequests().api_request(
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
print(CD.accesstoken)

# 制造订单
# 获取cid
search_category = operation_mysql(
    "select * from bus_goodscenter.gc_category where name = 'LineBus';"
)
setattr(CD, "cid", search_category[0]["id"])
# 获取sku_id_
data_format = "%" + "bus_auto_sub_" + str(CD.next_seven_day) + "%"
search_schedule = operation_mysql(
    "select * from bus_goodscenter.gc_goods_sku where tid = \'" + str(
        CD.tid) + "\' and name like '%s';" % data_format
)
print("获取的线路查询结果为：" + str(search_schedule))
setattr(CD, "schedule_id", search_schedule[-1]["id"])
setattr(CD, "goods_id", search_schedule[-1]["goods_id"])
setattr(CD, "goods_price", search_schedule[-1]["price"])

# 获取线路

search_sku= operation_mysql(
    "select * from bus_goodscenter.gc_goods_sku_packing where goods_sku_id = \'"+str(CD.schedule_id)+"\';")

setattr(CD,"packed_sku_id", search_schedule[-1]["id"])
print(CD.packed_sku_id)


search_goods_title = operation_mysql(
    "select * from bus_goodscenter.gc_goods_instance_linebus where id=\'" + str(CD.goods_id) + "\';"
)
setattr(CD, "goods_title", search_goods_title[0]["name"])
print(CD.goods_title)

# 锁座
lock_seat = ApiRequests().api_request("post", CD.url + r'/api/seat/lockSeat',
                                      {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid,
                                       "AccessToken": CD.accesstoken},
                                      {"cleanLastSelect": 1, "seatParam": {CD.schedule_id: {"1": [8], "2": []}},
                                       "seatToken": None})
print(lock_seat.json())
# # 座位和库存
# # seat_stock = ApiRequests().api_request("post", CD.url + r'/api/pre/check/seatandstock',
# #                                        {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid,
# #                                        "AccessToken": CD.accesstoken},
# #                                        {"skuId": CD.schedule_id, "packagedSkuId": CD.packed_sku_id,
# #                                         "wheelChairNum": 0, "normalNum": 1})
# # print(seat_stock.json())
# #
# # # 库存
# #
# # stok = ApiRequests().api_request("get", CD.url + r'/api/pre/check/left/stock?skuId='+str(CD.schedule_id),
# #                                  {"tid": str(CD.tid), "channelId": CD.channel_id, "operatorId": CD.userid,
# #                                   "AccessToken": CD.accesstoken}, None)
# # print(stok.json())





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
                "firstName": "ying",
                "lastName": "wang",
                "needWheelchair": False}],
            "infantPassengerParams": [],
            "childPassengerParams": [],
            "elderPassengerParams": [],
            "id": CD.schedule_id,
            "subBusLineCode": "bus_auto",
            "subBuslineName": "bus_auto_sub",
            "stationDepartureId": CD.station_departure_id,
            "stationArrivalId": CD.station_arrival_id}],
        "paymentParam": {
            "payToken": "",
            "payModeList": [{
                "count": 200, "amount": "20", "type": 1}],
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
print({
    "skus": [{
        "adultPassengerParams": [{
            "firstName": "ying",
            "lastName": "wang",
            "needWheelchair": False}],
        "infantPassengerParams": [],
        "childPassengerParams": [],
        "elderPassengerParams": [],
        "id": str(CD.schedule_id),
        "subBusLineCode": "bus_auto",
        "subBuslineName": "bus_auto_sub",
        "stationDepartureId": CD.station_departure_id,
        "stationArrivalId": CD.station_arrival_id}],
    "paymentParam": {
        "payToken": "",
        "payModeList": [{
            "count": 200, "amount": "20", "type": 1}],
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
print("支付口返回" + str(order_pay.json()))
