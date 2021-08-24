# -*- coding:utf-8 -*-
# @Time     :2019/4/8 10:12
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :Commondata.py
# @software :PyCharm

import time
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql
from BusProject.Linebus_Platform_API.common import DataPaths
from faker import Faker
import hashlib
import datetime
import os
import  random


class CommonData:
    # 当前时间戳
    current_time = str(int(time.time()))

    # 当前日期+1(MM/dd/yyyy)
    date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    # 当前日期时间戳
    current_date = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) * 1000
    print(current_date)
    # 七天后时间戳
    next_seven_day = (datetime.date.today() + datetime.timedelta(days=4)).strftime("%m/%d/%Y")
    next_seven_date = int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=2)),
                                                    '%Y-%m-%d'))) * 1000
    print(next_seven_date)

    # 出发时间
    array = time.strptime('2019-06-10 00:00:00', "%Y-%m-%d %H:%M:%S")
    timestamp = str(int(time.mktime(array)) * 1000)
    print(timestamp)

    # 接口的url
    url = "http://47.94.8.135:9101"

    # 用来测试的租户id
    tid = "322755215541408256"

    # 渠道id
    channel_id = "322761231290049024"
    driver_channnel_id = None

    # admin操作人id
    operatorid = "322756449295929856"
    operatorname = "qaadmin"

    # 出发城市id（默认Boston）
    city_departure_id = "244865177449665024"

    # 到达城市id（默认NewYork）
    city_arrival_id = "173855417259004416"

    # 从数据库获取票务平台后台的usernam,password
    # bsp_user = operation_mysql("select * from bus_bsp.bsp_user where tenant_id = \'" + tid + "\';")
    bsp_user_username = None
    bsp_user_password = None

    # 获取票务平台后台的operatortoken
    # operator_login = ApiRequests().api_request('post', url + r'/admin/login', None,
    # {"username": bsp_user_username, "password": bsp_user_password})
    operatortoken = None

    # website用户的account,password
    user_account = "+8615011111111"
    user_password = "a123456"
    user_email = "ruanzhe@riverroad.cn"

    # website使用userid
    userid = "322791664815547392"
    account_id = None

    # 获取sessionid,access
    # res_login = ApiRequests().api_request('post', url + r'/api/auth/login', {"tid": tid},
    #                                       {"account": user_account, "password": user_password,
    #                                        "client": "1"})
    # sessionid = res_login.json()["result"]["sessionId"]
    # accesstoken = res_login.json()["result"]["authCode"]

    sessionid = None
    accesstoken = None

    # 城市id
    cityId = None

    # 类目id
    cid = None

    # 用来存放goodsId
    goods_id = None

    # 商品价格
    goods_price = None

    # 商品名称
    goods_title = None

    # sku id
    skuId = None

    # sku日期
    scheduleDate = None

    # 发车时间
    timeDeparture = None

    # 出发站点id
    station_departure_id = None

    # 到达站点id
    station_arrival_id = None

    # 子线路code
    subBusLineCode = None

    # 超时订单id
    outtime_order_id = None

    # 订单总价格
    totalAmount = None

    # 支付总价格
    payAmount = None

    # 票号
    ticket_id = None

    # CN国家id
    country = operation_mysql("select * from bus_bsp.bsp_dictionary_item where value = 'CN' ;")
    country_code_id = country[0]["id"]
    country_code_name = country[0]["name"]

    # 邮件、短信发送方式配置id
    e_ticket_id = None

    # app相关name和version
    app_name = None
    ver_no = None

    # 设备device的deviceid
    device_deviceid = None

    # 设备device
    device_id = None

    # 被打包的sku id
    packed_sku_id = None

    # 线路id
    bus_line_id = None

    # 短信模板相关信息
    sms_tempalte_id = None
    sms_template_name = None
    sms_template_content = None
    sms_template_type = None
    sms_template_scene = None

    # 邮件的文件路径
    mail_file_path = DataPaths.Mail_File_Path
    # 邮件上传的file文件
    mail_file = None
    # 邮件上传后模板路径
    mail_template_url = None
    # 邮件模板code
    mail_template_code = None
    # 邮件模板id
    mail_template_id = None

    # 租户动态信息数据
    facebook_pixel_id = r"UA-128064891-2"
    google_analytics_id = r"UA-128064891-2"

    # 租户时区
    time_zone = "173855417259004416"

    # popup图片路径
    popup_file_path = DataPaths.PopUp_File_path
    # 上传的popup文件
    popup_file = None
    # popup保存时所需的content
    popup_content = None
    # 上传文件在服务器的名称
    popup_file_name = None
    # banner图片路径
    banner_imgurl = None
    # banner服务器文件路径
    banner_filePath = None
    # banner id
    banner_id = None
    # banner文件名
    banner_file_name = None

    # 验证码
    validation_code = None

    # 兑换码附件路径
    groupon_file_path = DataPaths.Groupon_File_path
    # 上传的groupon文件
    groupon_file = None
    # 兑换码文件在服务器路径
    groupon_file_service_path = None

    # 新增租户页面
    tenant_data_menu_id = None

    # 新增的租户静态数据配置id
    dynamic_tenant_config_id = None

    # 租户id
    tenant_id = None

    # dial_back_config_sms路径
    dial_back_config_sms = DataPaths.Dial_Back_Config_sms_path
    dial_back_config_sms_file = None
    # dial_back_config_phone路径
    dial_back_config_phone = DataPaths.Dial_Back_Config_phone_path
    dial_back_config_phone_file = None

    # dial_back_id
    dial_back_config = operation_mysql(
        "select * from  bus_linebus_platform.lb_dial_back_config "
    )
    dial_back_id = dial_back_config[0]["id"]

    # 租户基本信息配置id
    tenant_base_config_id = None

    # 租户配置website
    website = r"wycompany-dev.ubtbus.top"

    # 新增groupon码
    redeem_code = None

    # schedule id
    schedule_id = None

    # 线路id
    subbusline_id = "323498592881332736"
    busline_id = "323497820114375168"
    busline_name = "qatest"
    sub_busline_name = "qatest"

    # 司机id
    driver_id = "323827073032393216"

    # 司机端兑换groupon产生的redeemid
    redeem_id = None

    # 订单id
    order_id = None
    maintain_order_id = None

    # 用户信息id
    userinfo_id = None
    user_card_info_id = None
    user_billing_address_id = None

    # luggage_config_version
    luggage_config_version = None

    # checkin_alert相关参数
    checkin_alert_id = None
    checkin_alert_version = None

    # 车型id
    bus_model_id = None

    # 选座版本
    seat_config_version = None

    # 角色id
    role_id = None

    # App id
    app_id = None

    # 支付token
    paytoken = None

    # 银行交易 id
    transaction_id = None

    # 信用卡支付的id
    credit_card_payment_id = None

    # 票id
    ticket_id = None

    # 票二维码
    ticket_qrcode = None

    # 已验过票的二维码
    checked_ticket_qrcode = None

    # 已验过票的skuid
    checked_ticket_skuId = None

    # 已验过票的id
    checked_ticket_id = None

    # 已作废票的二维码
    void_ticket_qrcode = None

    # 已作废票的skuid
    void_ticket_skuId = None

    # 已作废的票的id
    void_ticket_id = None

    # bsp的用户名/密码/token
    bsp_user = "wycompany"
    bsp_password = "666666"
    bsp_operatortoken = None

    # ticket的票号
    ticket_code = None

    # 支付id
    payment_id = None

    # 无票的orderid
    noticket_order_id = None

    # 残疾人票
    wheelchair_ticket_id = None

    # 库存版本号
    goods_sku_version = None

    # 已改签的票id
    reschedule_ticket_id = None

    # announcement起始、结束时间
    tommorow = (datetime.datetime.now() + datetime.timedelta(days=1, hours=1))
    announcement_startdate = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(current_time)))
    announcement_enddate = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(time.mktime(tommorow.timetuple()))))

    # ticket_operation_log 的id
    ticket_operation_log_id = None

    # giftcard的id
    gift_card_strategy_id = None

    # 未激活钱包的账号/登录参数
    # nowallet_user_account = "+8615693351643"
    # nowallet_sessionid = None
    # nowallet_accesstoken = None

    # gift_card的skuid
    gift_card_skuid = None

    # 钱包充值的订单号
    wallet_reload_orderid = None

    # 钱包id
    wallet_id = None

    # 退票记录id
    ticket_refund_id = None

    # 第三方渠道id
    third_channel_id = "326313154521833984"

    # 第三方渠道seecret_key
    third_channel_secret_key = "196201051"

    # 第三方渠道登录返回的token
    third_token = None

    # 第三方渠道的订单id
    third_order_id = None

    # 不存在名为POS的app的租户
    noapp_tid = "305022698075984384"

    # pos机的订单id
    pos_order_id = None

    # 座位号
    seat_no = random.randint(1,44)
