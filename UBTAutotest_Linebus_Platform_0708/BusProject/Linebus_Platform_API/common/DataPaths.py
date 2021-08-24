# -*- coding:utf-8 -*-
# @Time     :2019/4/4 9:05
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :DataPaths.py
# @software :PyCharm
import os
import time

# 项目路径
ProjectPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
# 日志路径
LogsPath = os.path.join(ProjectPath,
                        'los/Linebus_Platform_API_{0}'.format(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())))
# 测试数据路径
DatasPath = os.path.join(ProjectPath, 'datas/Linebus_Platform_API_Test_data.xlsx')
# 报告路径
ReportPath = os.path.join(ProjectPath, 'report/report.html')
# 配置文件路径
ConfigPath = os.path.join(ProjectPath, 'config/case_con.ini')
# 测试用例路径
CasePath = os.path.join(ProjectPath, 'TestCases')
# mail附件路径
Mail_File_Path = os.path.join(ProjectPath, 'datas/emailconfig.ftl')
# popup附件路径
PopUp_File_path = os.path.join(ProjectPath, 'datas/popup.jpg ')
# groupon文件路径
Groupon_File_path = os.path.join(ProjectPath, 'datas/Groupon.csv')
# dial_back_config配置文件：sms
Dial_Back_Config_sms_path = os.path.join(ProjectPath, 'datas/redoak-sms-dis.xml')
# dial_back_config配置文件：phone
Dial_Back_Config_phone_path = os.path.join(ProjectPath, 'datas/redoak-phone-dis.xml')